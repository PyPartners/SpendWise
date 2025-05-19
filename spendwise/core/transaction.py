
from dataclasses import dataclass
from PyQt5.QtCore import QDate

@dataclass
class Transaction:
    id: str 
    date: QDate
    description: str
    type: str 
    amount: float
    category: str
