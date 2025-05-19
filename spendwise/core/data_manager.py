
import json
import os
from collections import defaultdict
from PyQt5.QtCore import QDate, QStandardPaths, QSettings, Qt, QCoreApplication
from spendwise.core.transaction import Transaction 

class DataManager:
    def __init__(self, settings, translator): 
        self._transactions = []
        self._income_categories = [
            "category_salary", "category_freelance", "category_investment",
            "category_gift", "category_other_income"
        ]
        self._expense_categories = [
            "category_food", "category_transport", "category_housing",
            "category_utilities", "category_healthcare", "category_entertainment",
            "category_education", "category_shopping", "category_other_expense"
        ]

        self.settings = settings
        self.translator = translator 

        self._user_currency_symbol = self.settings.value("user_currency_symbol", None, type=str)

        app_name = QCoreApplication.applicationName()
        if not app_name: 
            app_name = "SpendWise" 
        org_name = QCoreApplication.organizationName()
        if not org_name:
            org_name = "SpendWiseOrg"

        data_path_base = QStandardPaths.writableLocation(QStandardPaths.AppLocalDataLocation)
        if not data_path_base: 
            data_path_base = os.path.join(os.path.expanduser("~"), ".local", "share")

        self.data_dir = os.path.join(data_path_base, org_name, app_name)
        os.makedirs(self.data_dir, exist_ok=True)
        self.data_file = os.path.join(self.data_dir, "spendwise_data.json")

        self._load_data()

    def _load_data(self):
        if not os.path.exists(self.data_file):
            self._transactions = [] 
            return

        try:
            with open(self.data_file, 'r', encoding='utf-8') as f:
                data = json.load(f)

            self._transactions = []
            for t_data in data.get("transactions", []):
                try:
                    date_obj = QDate.fromString(t_data["date"], "yyyy-MM-dd")
                    if not date_obj.isValid(): 
                        date_obj = QDate.fromString(t_data["date"], Qt.ISODate)

                    if not date_obj.isValid(): 
                        print(f"Warning: Could not parse date '{t_data['date']}' for transaction ID {t_data.get('id')}. Skipping.")
                        continue

                    self._transactions.append(Transaction(
                        id=t_data["id"],
                        date=date_obj,
                        description=t_data["description"],
                        type=t_data["type"],
                        amount=float(t_data["amount"]),
                        category=t_data["category"]
                    ))
                except KeyError as e:
                    print(f"Warning: Missing key {e} in transaction data: {t_data}. Skipping.")
                except ValueError as e:
                    print(f"Warning: Value error parsing transaction data ({e}): {t_data}. Skipping.")
        except (json.JSONDecodeError, FileNotFoundError, IOError) as e:
            print(f"Error loading data from {self.data_file}: {e}. Starting with empty data.")
            self._transactions = []

    def _save_data(self):
        transactions_to_save = []
        for t in self._transactions:
            transactions_to_save.append({
                "id": t.id,
                "date": t.date.toString("yyyy-MM-dd"), 
                "description": t.description,
                "type": t.type,
                "amount": t.amount,
                "category": t.category
            })

        data_to_save = {
            "transactions": transactions_to_save,
        }
        try:
            with open(self.data_file, 'w', encoding='utf-8') as f:
                json.dump(data_to_save, f, indent=4, ensure_ascii=False)
        except IOError as e:
            print(f"Error saving data to {self.data_file}: {e}")


    def _add_dummy_data(self):
        import uuid
        dummy_data = [
            Transaction(str(uuid.uuid4()), QDate.currentDate().addDays(-15), "Groceries and Produce", "expense", 50.75, "category_food"),
            Transaction(str(uuid.uuid4()), QDate.currentDate().addDays(-10), "Monthly Salary", "income", 2500.00, "category_salary"),
        ]
        self._transactions.extend(dummy_data)
        self._save_data() 

    def get_all_category_keys(self, type_filter=None):
        if type_filter == "income":
            return self._income_categories[:]
        elif type_filter == "expense":
            return self._expense_categories[:]
        else: 
            return sorted(list(set(self._income_categories + self._expense_categories)))

    def add_transaction(self, transaction):
        self._transactions.append(transaction)
        self._save_data()

    def edit_transaction(self, transaction_id, updated_transaction_data):
        for i, t in enumerate(self._transactions):
            if t.id == transaction_id:
                self._transactions[i] = updated_transaction_data
                self._save_data()
                return True
        return False

    def delete_transaction(self, transaction_id):
        self._transactions = [t for t in self._transactions if t.id != transaction_id]
        self._save_data()

    def get_transaction_by_id(self, transaction_id):
        for t in self._transactions:
            if t.id == transaction_id:
                return t
        return None

    def get_transactions(self, filters=None):
        current_transactions = list(self._transactions) 

        if not filters or all(
            (key_ not in filters or filters[key_] is None or (key_ == 'category' and filters[key_] == 'all'))
            for key_ in ["start_date", "end_date", "category"]
        ):
             return current_transactions

        start_date = filters.get("start_date")
        end_date = filters.get("end_date")
        category_key = filters.get("category") 

        if start_date:
            current_transactions = [
                t for t in current_transactions if t.date >= start_date
            ]
        if end_date:
            current_transactions = [
                t for t in current_transactions if t.date <= end_date
            ]
        if category_key and category_key != "all": 
            current_transactions = [
                t for t in current_transactions if t.category == category_key
            ]
        return current_transactions

    def get_balance(self): 
        total_income = sum(t.amount for t in self._transactions if t.type == "income")
        total_expenses = sum(t.amount for t in self._transactions if t.type == "expense")
        return total_income - total_expenses

    def get_expenses_by_category(self, transactions_list=None): 
        source_transactions = transactions_list if transactions_list is not None else self._transactions

        expenses_by_cat = defaultdict(float)
        for t in source_transactions:
            if t.type == "expense":
                expenses_by_cat[t.category] += t.amount
        return dict(expenses_by_cat)

    def get_user_currency_symbol(self):
        return self._user_currency_symbol

    def set_user_currency_symbol(self, symbol):
        self._user_currency_symbol = symbol
        self.settings.setValue("user_currency_symbol", symbol)
        QCoreApplication.instance().currency_changed.emit()

    def get_display_currency_symbol(self):
        if self._user_currency_symbol:
            return self._user_currency_symbol
        return self.translator.translate("currency_symbol") 
