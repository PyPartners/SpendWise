
from PyQt5.QtWidgets import (
    QDialog, QVBoxLayout, QFormLayout, QLineEdit, QComboBox,
    QDoubleSpinBox, QDateEdit, QDialogButtonBox, QLabel, QApplication, QMessageBox,
    QPushButton, QStyle
)
from PyQt5.QtCore import QDate, Qt, QTimer
from PyQt5.QtGui import QIcon, QPalette, QColor

class TransactionDialog(QDialog):
    def __init__(self, translator, data_manager, transaction_to_edit=None, parent=None):
        super().__init__(parent)
        self.translator = translator
        self.data_manager = data_manager
        self.transaction_to_edit = transaction_to_edit

        self.setWindowTitle(self.translator.translate("add_transaction_title"))
        if self.transaction_to_edit:
            self.setWindowTitle(self.translator.translate("edit_transaction_title"))

        self.setMinimumWidth(400)
        self._init_ui()

        if self.transaction_to_edit:
            self._populate_fields()
        else: 
            if self.type_combo.currentIndex() >= 0:
                 self._on_type_changed(self.type_combo.currentIndex())
            elif self.type_combo.count() > 0:
                 self.type_combo.setCurrentIndex(0)

        self.retranslate_ui_texts() 
        QApplication.instance().currency_changed.connect(self.retranslate_ui_texts)
        QApplication.instance().translator.language_changed.connect(self.retranslate_ui_texts)


    def _init_ui(self):
        main_layout = QVBoxLayout(self)
        form_layout = QFormLayout()
        form_layout.setRowWrapPolicy(QFormLayout.WrapAllRows) 
        form_layout.setLabelAlignment(Qt.AlignLeft) 

        self.date_label = QLabel()
        self.date_edit = QDateEdit(QDate.currentDate())
        self.date_edit.setCalendarPopup(True)
        form_layout.addRow(self.date_label, self.date_edit)

        self.description_label = QLabel()
        self.description_edit = QLineEdit()
        form_layout.addRow(self.description_label, self.description_edit)

        self.type_label = QLabel()
        self.type_combo = QComboBox()
        self.type_combo.currentIndexChanged.connect(self._on_type_changed)
        form_layout.addRow(self.type_label, self.type_combo)

        self.amount_label = QLabel()
        self.amount_spinbox = QDoubleSpinBox()
        self.amount_spinbox.setRange(0.00, 1000000000.00) 
        self.amount_spinbox.setDecimals(2)
        self.amount_spinbox.setGroupSeparatorShown(True) 
        form_layout.addRow(self.amount_label, self.amount_spinbox)

        self.category_label = QLabel()
        self.category_combo = QComboBox()
        form_layout.addRow(self.category_label, self.category_combo)

        main_layout.addLayout(form_layout)

        self.button_box = QDialogButtonBox()
        self.ok_button = self.button_box.addButton(QDialogButtonBox.Ok)
        self.cancel_button = self.button_box.addButton(QDialogButtonBox.Cancel)

        self.ok_button.setIcon(self.style().standardIcon(QStyle.SP_DialogOkButton))
        self.cancel_button.setIcon(self.style().standardIcon(QStyle.SP_DialogCancelButton))

        self.ok_button.clicked.connect(self.accept_dialog) 
        self.cancel_button.clicked.connect(self.reject)
        main_layout.addWidget(self.button_box)

        self._populate_type_combo() 

    def _populate_type_combo(self):
        current_data = self.type_combo.currentData()
        self.type_combo.blockSignals(True)
        self.type_combo.clear()
        self.type_combo.addItem(self.translator.translate("income"), "income")
        self.type_combo.addItem(self.translator.translate("expense"), "expense")

        idx = self.type_combo.findData(current_data)
        if idx != -1: self.type_combo.setCurrentIndex(idx)
        elif self.type_combo.count() > 0: self.type_combo.setCurrentIndex(0)

        self.type_combo.blockSignals(False)
        if self.type_combo.currentIndex() >= 0:
            self._on_type_changed(self.type_combo.currentIndex())


    def _on_type_changed(self, index):
        if index < 0: return 
        selected_type_data = self.type_combo.itemData(index)
        if selected_type_data:
            self._populate_category_combo(selected_type_data)

    def _populate_category_combo(self, current_type_data):
        current_category_selection_data = self.category_combo.currentData()
        self.category_combo.clear()

        if not current_type_data: return

        category_keys = self.data_manager.get_all_category_keys(current_type_data)
        if not category_keys:
             default_key_name = f"default_{current_type_data}_category_key" 
             display_name_key = self.translator.translate(default_key_name, f"uncategorized_{current_type_data}") 
             self.category_combo.addItem(self.translator.translate(display_name_key), display_name_key) 
        else:
            for key in category_keys:
                self.category_combo.addItem(self.translator.translate(key), key)

        idx = self.category_combo.findData(current_category_selection_data)
        if idx != -1: self.category_combo.setCurrentIndex(idx)
        elif self.category_combo.count() > 0: self.category_combo.setCurrentIndex(0)


    def _populate_fields(self):
        if self.transaction_to_edit:
            self.date_edit.setDate(self.transaction_to_edit.date)
            self.description_edit.setText(self.transaction_to_edit.description)

            type_index = self.type_combo.findData(self.transaction_to_edit.type)
            if type_index != -1:
                self.type_combo.setCurrentIndex(type_index) 

            QTimer.singleShot(0, self._select_edit_category)

            self.amount_spinbox.setValue(self.transaction_to_edit.amount)

    def _select_edit_category(self): 
        if self.transaction_to_edit:
            category_index = self.category_combo.findData(self.transaction_to_edit.category)
            if category_index != -1:
                self.category_combo.setCurrentIndex(category_index)
            elif self.category_combo.count() > 0 : 
                self.category_combo.setCurrentIndex(0)


    def get_data(self):
        return {
            "date": self.date_edit.date(),
            "description": self.description_edit.text().strip(),
            "type": self.type_combo.currentData(),
            "amount": self.amount_spinbox.value(),
            "category": self.category_combo.currentData()
        }

    def _validate_input(self, field, message_key, error_message_default):
        QMessageBox.warning(self, self.translator.translate("input_error_title"), 
                            self.translator.translate(message_key, error_message_default))
        if field:
            field.setFocus()
        return False


    def accept_dialog(self): 
        desc = self.description_edit.text().strip()
        if not desc:
            return self._validate_input(self.description_edit, "description_empty_error", "Description cannot be empty.")

        if self.amount_spinbox.value() <= 0:
             return self._validate_input(self.amount_spinbox, "amount_invalid_error", "Amount must be greater than zero.")

        if not self.category_combo.currentData() or self.category_combo.currentIndex() < 0:
             return self._validate_input(self.category_combo, "category_empty_error", "Please select a category.")

        super().accept()

    def retranslate_ui_texts(self): 
        if self.transaction_to_edit:
            self.setWindowTitle(self.translator.translate("edit_transaction_title"))
        else:
            self.setWindowTitle(self.translator.translate("add_transaction_title"))

        self.date_label.setText(self.translator.translate("date_label", "Date:"))
        self.date_edit.setDisplayFormat(self.translator.translate("date_format_long", "MMMM d, yyyy"))

        self.description_label.setText(self.translator.translate("description_label", "Description:"))
        self.description_edit.setPlaceholderText(self.translator.translate("description_placeholder", "e.g., Groceries, Salary"))

        self.type_label.setText(self.translator.translate("type_label", "Type:"))
        self.amount_label.setText(self.translator.translate("amount_label", "Amount:"))
        self.category_label.setText(self.translator.translate("category_label", "Category:"))

        active_currency_symbol = self.data_manager.get_display_currency_symbol()
        prefix_to_set = ""
        suffix_to_set = ""
        if QApplication.instance().layoutDirection() == Qt.RightToLeft:
            suffix_to_set = " " + active_currency_symbol 
        else:
            prefix_to_set = active_currency_symbol + " "

        self.amount_spinbox.setPrefix(prefix_to_set)
        self.amount_spinbox.setSuffix(suffix_to_set)

        self._populate_type_combo() 

        self.ok_button.setText(self.translator.translate("ok_button"))
        self.cancel_button.setText(self.translator.translate("cancel_button"))

    def closeEvent(self, event):
        try:
            QApplication.instance().currency_changed.disconnect(self.retranslate_ui_texts)
            QApplication.instance().translator.language_changed.disconnect(self.retranslate_ui_texts)
        except TypeError:
            pass 
        super().closeEvent(event)
