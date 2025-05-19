
from PyQt5.QtWidgets import (
    QDialog, QVBoxLayout, QTableWidget, QTableWidgetItem,
    QDialogButtonBox, QLabel, QHeaderView, QApplication, QAbstractItemView
)
from PyQt5.QtCore import Qt

class StatisticsDialog(QDialog):
    def __init__(self, data_manager, translator, parent=None):
        super().__init__(parent)
        self.data_manager = data_manager
        self.translator = translator
        self.setMinimumWidth(500)

        self._init_ui()
        self.retranslate_ui() 
        QApplication.instance().currency_changed.connect(self.retranslate_ui)
        QApplication.instance().translator.language_changed.connect(self.retranslate_ui)


    def _init_ui(self):
        layout = QVBoxLayout(self)

        self.title_label = QLabel() 
        title_font = self.title_label.font()
        title_font.setPointSize(14) 
        self.title_label.setFont(title_font)
        self.title_label.setAlignment(Qt.AlignCenter)
        self.title_label.setObjectName("DialogTitleLabel") 
        layout.addWidget(self.title_label)

        self.stats_table = QTableWidget()
        self.stats_table.setColumnCount(2)
        self.stats_table.horizontalHeader().setSectionResizeMode(QHeaderView.Stretch)
        self.stats_table.setEditTriggers(QTableWidget.NoEditTriggers) 
        self.stats_table.setSelectionBehavior(QAbstractItemView.SelectRows)
        self.stats_table.setSelectionMode(QAbstractItemView.SingleSelection)
        self.stats_table.setAlternatingRowColors(True)
        layout.addWidget(self.stats_table)

        self.button_box = QDialogButtonBox(QDialogButtonBox.Ok)
        self.button_box.accepted.connect(self.accept)
        layout.addWidget(self.button_box)

        self.resize(550, 450)

    def _load_statistics(self):
        self.stats_table.setRowCount(0) 

        all_transactions = self.data_manager.get_transactions() 
        expenses_by_category = self.data_manager.get_expenses_by_category(all_transactions)

        currency_symbol = self.data_manager.get_display_currency_symbol()

        self.stats_table.setRowCount(len(expenses_by_category))

        row = 0
        for category_key, total_amount in expenses_by_category.items():
            category_name_item = QTableWidgetItem(self.translator.translate(category_key))

            amount_text = f"{currency_symbol}{total_amount:.2f}"
            if QApplication.instance().layoutDirection() == Qt.RightToLeft:
                amount_text = f"{total_amount:.2f} {currency_symbol}"
            amount_item = QTableWidgetItem(amount_text)

            amount_item.setTextAlignment(Qt.AlignRight | Qt.AlignVCenter)

            self.stats_table.setItem(row, 0, category_name_item)
            self.stats_table.setItem(row, 1, amount_item)
            row += 1

        self.stats_table.sortItems(1, Qt.DescendingOrder) 

    def retranslate_ui(self): 
        self.setWindowTitle(self.translator.translate("statistics_title_detailed", "Detailed Statistics"))
        self.title_label.setText(self.translator.translate("expenses_by_category_title_detailed", "Expenses by Category (All Time)"))

        header1_text = self.translator.translate("category")
        header2_text = self.translator.translate("total_expenses")
        self.stats_table.setHorizontalHeaderLabels([header1_text, header2_text])

        ok_button = self.button_box.button(QDialogButtonBox.Ok)
        if ok_button:
            ok_button.setText(self.translator.translate("ok_button"))

        self._load_statistics() 

    def closeEvent(self, event):
        try:
            QApplication.instance().currency_changed.disconnect(self.retranslate_ui)
            QApplication.instance().translator.language_changed.disconnect(self.retranslate_ui)
        except TypeError:
            pass
        super().closeEvent(event)
