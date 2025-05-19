
import uuid
import base64
import os # For checking logo path in show_about_dialog
from PyQt5.QtWidgets import (
    QMainWindow, QAction, QTableView, QVBoxLayout, QHBoxLayout, QWidget,
    QToolBar, QLabel, QComboBox, QDateEdit, QPushButton, QMessageBox,
    QAbstractItemView, QHeaderView, QMenu, QApplication, QSplitter, QGroupBox,
    QStyle, QActionGroup, QSizePolicy, QInputDialog, QLineEdit
)
from PyQt5.QtCore import Qt, QDate, QAbstractTableModel, QVariant, pyqtSignal, QModelIndex, QSortFilterProxyModel, QSettings, QPropertyAnimation, QEasingCurve, QSize
from PyQt5.QtGui import QIcon, QPixmap, QPainter # QPainter for fallback logo

from spendwise.widgets.transaction_dialog import TransactionDialog
from spendwise.widgets.statistics_dialog import StatisticsDialog
from spendwise.widgets.about_dialog import AboutDialog
from spendwise.widgets.chart_widget import SpendChartWidget
from spendwise.core.transaction import Transaction
from resources import images

class TransactionTableModel(QAbstractTableModel):
    def __init__(self, data, headers, parent=None):
        super().__init__(parent)
        self._data = data
        self._headers = headers
        self.translator = QApplication.instance().translator
        self.data_manager = QApplication.instance().data_manager

    def rowCount(self, parent=QModelIndex()):
        return len(self._data)

    def columnCount(self, parent=QModelIndex()):
        return len(self._headers)

    def data(self, index, role=Qt.DisplayRole):
        if not index.isValid():
            return QVariant()

        transaction = self._data[index.row()]
        column_key = self._headers[index.column()] 

        if role == Qt.DisplayRole:
            if column_key == "date":
                return transaction.date.toString(self.translator.translate("date_format_short", "yyyy-MM-dd"))
            elif column_key == "description":
                return transaction.description
            elif column_key == "type":
                return self.translator.translate(transaction.type) 
            elif column_key == "amount":
                currency_symbol = self.data_manager.get_display_currency_symbol()
                if QApplication.instance().layoutDirection() == Qt.RightToLeft:
                     return f"{transaction.amount:.2f} {currency_symbol}"
                return f"{currency_symbol}{transaction.amount:.2f}" # No space for typical LTR
            elif column_key == "category":
                return self.translator.translate(transaction.category) 
        elif role == Qt.TextAlignmentRole:
            if column_key == "amount":
                return Qt.AlignRight | Qt.AlignVCenter
        return QVariant()

    def headerData(self, section, orientation, role=Qt.DisplayRole):
        if role == Qt.DisplayRole and orientation == Qt.Horizontal:
            return self.translator.translate(self._headers[section])
        return QVariant()

    def refresh_data(self, new_data):
        self.beginResetModel()
        self._data = new_data
        self.endResetModel()

    def get_transaction_id(self, row_index):
        if 0 <= row_index < len(self._data):
            return self._data[row_index].id
        return None

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.data_manager = QApplication.instance().data_manager
        self.translator = QApplication.instance().translator
        self.theme_manager = QApplication.instance().theme_manager
        self.settings = QSettings("SpendWiseOrg", "SpendWise")


        self.setMinimumSize(800, 600) 

        self._init_ui()
        self.apply_filters() 
        self.retranslate_ui_and_components() 
        self.setWindowOpacity(0.0) 

    def show_animated(self):
        self.show() 
        if not hasattr(self, 'opacity_animation_main') or not self.opacity_animation_main:
            self.opacity_animation_main = QPropertyAnimation(self, b"windowOpacity")
            self.opacity_animation_main.setDuration(400) 
            self.opacity_animation_main.setStartValue(0.0)
            self.opacity_animation_main.setEndValue(1.0)
            self.opacity_animation_main.setEasingCurve(QEasingCurve.InOutQuad)

        if self.opacity_animation_main.state() != QPropertyAnimation.Running:
             self.opacity_animation_main.start()


    def _init_ui(self):
        self.main_widget = QWidget()
        self.setCentralWidget(self.main_widget)
        main_v_layout = QVBoxLayout(self.main_widget) 

        self._create_menu_bar()
        self._create_tool_bar()

        self.filter_groupbox = QGroupBox() 
        filter_h_layout = QHBoxLayout(self.filter_groupbox) 

        self.start_date_edit = QDateEdit(QDate.currentDate().addMonths(-1))
        self.start_date_edit.setCalendarPopup(True)
        self.end_date_edit = QDateEdit(QDate.currentDate())
        self.end_date_edit.setCalendarPopup(True)

        self.category_filter_combo = QComboBox()

        self.filter_button = QPushButton() 
        self.filter_button.setIcon(self.style().standardIcon(QStyle.SP_DialogApplyButton))
        self.filter_button.clicked.connect(self.apply_filters)
        self.filter_button.setObjectName("FilterButton") 

        self.start_date_label = QLabel() 
        self.end_date_label = QLabel() 
        self.category_filter_label = QLabel() 

        filter_h_layout.addWidget(self.start_date_label)
        filter_h_layout.addWidget(self.start_date_edit)
        filter_h_layout.addWidget(self.end_date_label)
        filter_h_layout.addWidget(self.end_date_edit)
        filter_h_layout.addWidget(self.category_filter_label)
        filter_h_layout.addWidget(self.category_filter_combo)
        filter_h_layout.addStretch(1) 
        filter_h_layout.addWidget(self.filter_button)
        main_v_layout.addWidget(self.filter_groupbox)

        self.content_splitter = QSplitter(Qt.Vertical) 

        self.chart_widget_container = QGroupBox() 
        self.chart_widget_container.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Preferred)
        chart_layout = QVBoxLayout(self.chart_widget_container)
        self.spend_chart = SpendChartWidget(self.data_manager, self.translator)
        chart_layout.addWidget(self.spend_chart)
        self.content_splitter.addWidget(self.chart_widget_container)

        self.table_view = QTableView()
        self.table_view.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)
        self.table_view.setSelectionBehavior(QAbstractItemView.SelectRows)
        self.table_view.setSelectionMode(QAbstractItemView.SingleSelection)
        self.table_view.setEditTriggers(QAbstractItemView.NoEditTriggers) 
        self.table_view.horizontalHeader().setSectionResizeMode(QHeaderView.Stretch) 
        self.table_view.setAlternatingRowColors(True)
        self.table_view.setSortingEnabled(True)

        self.table_header_keys = ["date", "description", "type", "amount", "category"]
        self.transaction_model = TransactionTableModel([], self.table_header_keys)
        self.proxy_model = QSortFilterProxyModel()
        self.proxy_model.setSourceModel(self.transaction_model)
        self.table_view.setModel(self.proxy_model)
        self.table_view.sortByColumn(0, Qt.DescendingOrder) 
        self.content_splitter.addWidget(self.table_view)

        initial_height = self.sizeHint().height() if self.height() < 100 else self.height() 
        if initial_height < 300: initial_height = 600 
        self.content_splitter.setSizes([int(initial_height * 0.4), int(initial_height * 0.6)])

        main_v_layout.addWidget(self.content_splitter, 1) 

        summary_layout = QHBoxLayout()
        self.balance_label = QLabel() 
        font = self.balance_label.font()
        font.setPointSize(font.pointSize() + 2) 
        font.setBold(True)
        self.balance_label.setFont(font)
        summary_layout.addStretch()
        summary_layout.addWidget(self.balance_label)
        main_v_layout.addLayout(summary_layout)

        self.statusBar().showMessage(self.translator.translate("status_ready"))

        self._populate_category_filter()

    def _create_menu_bar(self):
        menu_bar = self.menuBar()

        self.file_menu = menu_bar.addMenu("") 
        self.add_action_menu = QAction(self.style().standardIcon(QStyle.SP_FileDialogNewFolder), "", self)
        self.add_action_menu.triggered.connect(self.add_transaction)
        self.exit_action = QAction(self.style().standardIcon(QStyle.SP_DialogCloseButton), "", self)
        self.exit_action.triggered.connect(self.close)
        self.file_menu.addAction(self.add_action_menu)
        self.file_menu.addSeparator()
        self.file_menu.addAction(self.exit_action)

        self.edit_menu = menu_bar.addMenu("") 
        self.edit_action_menu = QAction(self.style().standardIcon(QStyle.SP_FileDialogDetailedView), "", self)
        self.edit_action_menu.triggered.connect(self.edit_transaction)
        self.delete_action_menu = QAction(self.style().standardIcon(QStyle.SP_TrashIcon), "", self)
        self.delete_action_menu.triggered.connect(self.delete_transaction)

        self.edit_menu.addAction(self.edit_action_menu)
        self.edit_menu.addAction(self.delete_action_menu)

        self.view_menu = menu_bar.addMenu("") 
        self.stats_action = QAction(self.style().standardIcon(QStyle.SP_FileDialogInfoView), "", self) 
        self.stats_action.triggered.connect(self.show_statistics)
        self.view_menu.addAction(self.stats_action)

        self.settings_menu = menu_bar.addMenu("") 
        self.language_menu = self.settings_menu.addMenu("") 
        self.lang_group = QActionGroup(self) 
        self.lang_group.setExclusive(True)

        self.en_lang_action = QAction("English", self, checkable=True)
        self.en_lang_action.triggered.connect(lambda: self.change_language("en"))
        self.language_menu.addAction(self.en_lang_action)
        self.lang_group.addAction(self.en_lang_action)

        self.ar_lang_action = QAction("العربية", self, checkable=True) 
        self.ar_lang_action.triggered.connect(lambda: self.change_language("ar"))
        self.language_menu.addAction(self.ar_lang_action)
        self.lang_group.addAction(self.ar_lang_action)

        self.theme_menu = self.settings_menu.addMenu("") 
        self.theme_group = QActionGroup(self) 
        self.theme_group.setExclusive(True)

        self.light_theme_action = QAction("", self, checkable=True) 
        self.light_theme_action.triggered.connect(lambda: self.change_theme("light"))
        self.theme_menu.addAction(self.light_theme_action)
        self.theme_group.addAction(self.light_theme_action)

        self.dark_theme_action = QAction("", self, checkable=True) 
        self.dark_theme_action.triggered.connect(lambda: self.change_theme("dark"))
        self.theme_menu.addAction(self.dark_theme_action)
        self.theme_group.addAction(self.dark_theme_action)

        self.currency_action = QAction("", self) # Text set in retranslate
        self.currency_action.triggered.connect(self.change_currency_settings)
        self.settings_menu.addAction(self.currency_action)


        self.help_menu = menu_bar.addMenu("") 
        self.about_action = QAction(self.style().standardIcon(QStyle.SP_MessageBoxInformation), "", self)
        self.about_action.triggered.connect(self.show_about_dialog)
        self.help_menu.addAction(self.about_action)

        if self.translator.current_language == "en": self.en_lang_action.setChecked(True)
        elif self.translator.current_language == "ar": self.ar_lang_action.setChecked(True)
        if self.theme_manager.current_theme == "light": self.light_theme_action.setChecked(True)
        elif self.theme_manager.current_theme == "dark": self.dark_theme_action.setChecked(True)

    def _create_tool_bar(self):
        tool_bar = QToolBar("Main Toolbar")
        tool_bar.setIconSize(QSize(22, 22)) 
        tool_bar.setMovable(False) 
        self.addToolBar(Qt.TopToolBarArea, tool_bar) 

        self.add_action_toolbar = tool_bar.addAction(self.style().standardIcon(QStyle.SP_FileDialogNewFolder), "") 
        self.add_action_toolbar.triggered.connect(self.add_transaction)

        self.edit_action_toolbar = tool_bar.addAction(self.style().standardIcon(QStyle.SP_FileDialogDetailedView), "") 
        self.edit_action_toolbar.triggered.connect(self.edit_transaction)

        self.delete_action_toolbar = tool_bar.addAction(self.style().standardIcon(QStyle.SP_TrashIcon), "") 
        self.delete_action_toolbar.triggered.connect(self.delete_transaction)

        tool_bar.addSeparator()

        self.refresh_action_toolbar = tool_bar.addAction(self.style().standardIcon(QStyle.SP_BrowserReload), "")
        self.refresh_action_toolbar.triggered.connect(self.apply_filters)


    def _populate_category_filter(self):
        current_category_key_data = self.category_filter_combo.currentData()
        self.category_filter_combo.clear()
        self.category_filter_combo.addItem(self.translator.translate("all_categories"), "all")

        income_cat_keys = self.data_manager.get_all_category_keys("income")
        expense_cat_keys = self.data_manager.get_all_category_keys("expense")

        all_keys = sorted(list(set(income_cat_keys + expense_cat_keys)))
        for key in all_keys:
            self.category_filter_combo.addItem(self.translator.translate(key), key)

        idx = self.category_filter_combo.findData(current_category_key_data)
        if idx != -1: self.category_filter_combo.setCurrentIndex(idx)
        elif self.category_filter_combo.count() > 0: self.category_filter_combo.setCurrentIndex(0)

    def retranslate_ui_and_components(self):
        self.setWindowTitle(self.translator.translate("app_title"))

        self.file_menu.setTitle(self.translator.translate("menu_file"))
        self.add_action_menu.setText(self.translator.translate("add_transaction"))
        self.exit_action.setText(self.translator.translate("menu_exit"))

        self.edit_menu.setTitle(self.translator.translate("menu_edit"))
        self.edit_action_menu.setText(self.translator.translate("edit_transaction"))
        self.delete_action_menu.setText(self.translator.translate("delete_transaction"))

        self.view_menu.setTitle(self.translator.translate("menu_view"))
        self.stats_action.setText(self.translator.translate("view_detailed_statistics"))

        self.settings_menu.setTitle(self.translator.translate("menu_settings"))
        self.language_menu.setTitle(self.translator.translate("language"))
        self.theme_menu.setTitle(self.translator.translate("theme"))
        self.light_theme_action.setText(self.translator.translate("light_mode"))
        self.dark_theme_action.setText(self.translator.translate("dark_mode"))
        self.currency_action.setText(self.translator.translate("currency_settings_menu", "Currency..."))

        self.help_menu.setTitle(self.translator.translate("menu_help"))
        self.about_action.setText(self.translator.translate("menu_about"))

        self.add_action_toolbar.setToolTip(self.translator.translate("add_transaction"))
        self.edit_action_toolbar.setToolTip(self.translator.translate("edit_transaction"))
        self.delete_action_toolbar.setToolTip(self.translator.translate("delete_transaction"))
        self.refresh_action_toolbar.setToolTip(self.translator.translate("refresh_data"))

        self.filter_groupbox.setTitle(self.translator.translate("filter_records_title"))
        self.start_date_label.setText(self.translator.translate("start_date"))
        self.end_date_label.setText(self.translator.translate("end_date"))
        self.category_filter_label.setText(self.translator.translate("category"))
        self.filter_button.setText(self.translator.translate("apply_filter_button"))

        self.chart_widget_container.setTitle(self.translator.translate("expense_summary_chart_title"))

        self._populate_category_filter() 
        self.transaction_model.headerDataChanged.emit(Qt.Horizontal, 0, self.transaction_model.columnCount() -1)

        if self.transaction_model.rowCount() > 0:
             self.transaction_model.layoutChanged.emit() 

        self.update_balance_summary()
        self.spend_chart.update_chart(self.current_filters if hasattr(self, 'current_filters') else None)
        self.statusBar().showMessage(self.translator.translate("status_ready"))


    def load_transactions(self, filters=None):
        transactions = self.data_manager.get_transactions(filters)
        self.transaction_model.refresh_data(transactions)

    def update_balance_summary(self):
        balance = self.data_manager.get_balance() 
        currency_symbol = self.data_manager.get_display_currency_symbol()

        text = f"{self.translator.translate('balance')}: {currency_symbol}{balance:.2f}"
        if QApplication.instance().layoutDirection() == Qt.RightToLeft:
            text = f"{self.translator.translate('balance')}: {balance:.2f} {currency_symbol}"
        self.balance_label.setText(text)

    def add_transaction(self):
        dialog = TransactionDialog(self.translator, self.data_manager, parent=self)
        if dialog.exec_():
            data = dialog.get_data()
            new_id = str(uuid.uuid4())
            transaction = Transaction(
                id=new_id, date=data["date"], description=data["description"],
                type=data["type"], amount=data["amount"], category=data["category"]
            )
            self.data_manager.add_transaction(transaction)
            self.apply_filters() 

    def edit_transaction(self):
        selected_indexes = self.table_view.selectionModel().selectedRows()
        if not selected_indexes:
            QMessageBox.information(self, self.translator.translate("edit_transaction"), 
                                self.translator.translate("select_transaction_to_edit"))
            return

        source_index = self.proxy_model.mapToSource(selected_indexes[0])
        transaction_id = self.transaction_model.get_transaction_id(source_index.row())

        if transaction_id:
            transaction = self.data_manager.get_transaction_by_id(transaction_id)
            if transaction:
                dialog = TransactionDialog(self.translator, self.data_manager, transaction_to_edit=transaction, parent=self)
                if dialog.exec_():
                    updated_data = dialog.get_data()
                    updated_transaction = Transaction(
                        id=transaction.id, date=updated_data["date"], description=updated_data["description"],
                        type=updated_data["type"], amount=updated_data["amount"], category=updated_data["category"]
                    )
                    self.data_manager.edit_transaction(transaction.id, updated_transaction)
                    self.apply_filters()

    def delete_transaction(self):
        selected_indexes = self.table_view.selectionModel().selectedRows()
        if not selected_indexes:
            QMessageBox.information(self, self.translator.translate("delete_transaction"), 
                                self.translator.translate("select_transaction_to_delete"))
            return

        reply = QMessageBox.question(self, self.translator.translate("delete_transaction"),
                                     self.translator.translate("confirm_delete_transaction_modern"), 
                                     QMessageBox.Yes | QMessageBox.No, QMessageBox.No)

        if reply == QMessageBox.Yes:
            source_index = self.proxy_model.mapToSource(selected_indexes[0])
            transaction_id = self.transaction_model.get_transaction_id(source_index.row())
            if transaction_id:
                self.data_manager.delete_transaction(transaction_id)
                self.apply_filters()

    def apply_filters(self):
        start_date = self.start_date_edit.date()
        end_date = self.end_date_edit.date()
        category_key = self.category_filter_combo.currentData()

        self.current_filters = { 
            "start_date": start_date, "end_date": end_date,
            "category": category_key if category_key != "all" else None
        }
        self.load_transactions(self.current_filters) 
        self.update_balance_summary() 
        self.spend_chart.update_chart(self.current_filters) 

    def change_language(self, lang_code):
        self.settings.setValue("language", lang_code)
        self.translator.set_language(lang_code) 
        if lang_code == "en": self.en_lang_action.setChecked(True)
        elif lang_code == "ar": self.ar_lang_action.setChecked(True)

    def change_theme(self, theme_name):
        self.settings.setValue("theme", theme_name)
        self.theme_manager.apply_theme(QApplication.instance(), theme_name)
        if theme_name == "light": self.light_theme_action.setChecked(True)
        elif theme_name == "dark": self.dark_theme_action.setChecked(True)
        self.spend_chart.update_chart_theme() 

    def change_currency_settings(self):
        currencies = {
            self.translator.translate("currency_default_option", "Default (from language)"): None,
            "USD ($)": "$",
            "EUR (€)": "€",
            "GBP (£)": "£",
            "JPY (¥)": "¥",
            "INR (₹)": "₹",
            "SAR (ر.س)": "ر.س",
            self.translator.translate("currency_custom_option", "Custom..."): "CUSTOM"
        }
        currency_display_names = list(currencies.keys())

        current_user_symbol = self.data_manager.get_user_currency_symbol()
        current_selection_index = 0 
        if current_user_symbol is not None:
            found = False
            for i, (display_name, symbol_val) in enumerate(currencies.items()):
                if symbol_val == current_user_symbol:
                    current_selection_index = i
                    found = True
                    break
            if not found and current_user_symbol: 
                try: 
                    current_selection_index = currency_display_names.index(self.translator.translate("currency_custom_option", "Custom..."))
                except ValueError: 
                    pass 

        item, ok = QInputDialog.getItem(self, 
                                        self.translator.translate("currency_settings_title", "Currency Settings"),
                                        self.translator.translate("currency_select_prompt", "Select currency:"),
                                        currency_display_names, current_selection_index, False)

        if ok and item:
            selected_symbol_value = currencies[item]

            if selected_symbol_value == "CUSTOM":
                custom_symbol_text = current_user_symbol if current_user_symbol and current_user_symbol not in currencies.values() else ""
                custom_symbol, ok_custom = QInputDialog.getText(self,
                                                               self.translator.translate("custom_currency_title", "Custom Currency"),
                                                               self.translator.translate("custom_currency_prompt", "Enter currency symbol (e.g., CAD):"),
                                                               QLineEdit.Normal,
                                                               custom_symbol_text)
                if ok_custom and custom_symbol.strip():
                    self.data_manager.set_user_currency_symbol(custom_symbol.strip())
                elif ok_custom and not custom_symbol.strip(): 
                    self.data_manager.set_user_currency_symbol(None) 
            else:
                self.data_manager.set_user_currency_symbol(selected_symbol_value)

    def on_currency_changed(self):
        self.update_balance_summary()
        self.transaction_model.layoutChanged.emit() 
        self.spend_chart.update_chart(self.current_filters if hasattr(self, 'current_filters') else None)
        self.statusBar().showMessage(self.translator.translate("currency_updated_status", "Currency settings updated."))

    def show_about_dialog(self):
        logo_path = images.get_logo_path() 
        logo_pixmap = QPixmap()
        if logo_path and os.path.exists(logo_path): 
            if not logo_pixmap.load(logo_path):
                print(f"Warning: Failed to load logo for About dialog from {logo_path}. Using fallback.")
                logo_pixmap = QPixmap(64,64)
                logo_pixmap.fill(Qt.lightGray)
        else:
            print(f"Warning: Logo for About dialog not found at {logo_path}. Using fallback.")
            logo_pixmap = QPixmap(64,64)
            logo_pixmap.fill(Qt.darkGray)

        dialog = AboutDialog(self.translator, logo_pixmap, parent=self)
        dialog.exec_()

    def show_statistics(self): 
        stats_dialog = StatisticsDialog(self.data_manager, self.translator, self)
        stats_dialog.exec_()

    def closeEvent(self, event):
        super().closeEvent(event)

    def resizeEvent(self, event):
        super().resizeEvent(event)
