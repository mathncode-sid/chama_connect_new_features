# Mock data store
from datetime import datetime

chama = {
    "name": "Group 15",
    "balance": 12500,
    "members": {
        "John": {"amount": 3500, "date_joined": "2024-01-15"},
        "Mary": {"amount": 4000, "date_joined": "2024-02-10"},
        "Sidney": {"amount": 5000, "date_joined": "2024-01-20"}
    }
}

contributions = [
    {"member": "John", "amount": 1000, "date": "2024-03-01"},
    {"member": "Mary", "amount": 1500, "date": "2024-03-02"},
    {"member": "Sidney", "amount": 2000, "date": "2024-03-03"}
]

# Session management for USSD
sessions = {}