from data import chama, contributions, sessions
from datetime import datetime
import uuid

def get_balance():
    return chama["balance"]

def get_members():
    return list(chama["members"].keys())

def get_member_contribution(member_name):
    if member_name in chama["members"]:
        return chama["members"][member_name]["amount"]
    return 0

def add_contribution(name, amount):
    chama["balance"] += amount
    if name not in chama["members"]:
        chama["members"][name] = {"amount": 0, "date_joined": datetime.now().strftime("%Y-%m-%d")}
    
    chama["members"][name]["amount"] += amount
    contributions.append({
        "member": name,
        "amount": amount,
        "date": datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    })
    return True

def get_member_details(member_name):
    if member_name in chama["members"]:
        return chama["members"][member_name]
    return None

def get_all_members_with_contributions():
    result = []
    for member, details in chama["members"].items():
        result.append(f"{member}: Ksh {details['amount']}")
    return result

def get_recent_contributions(limit=5):
    recent = contributions[-limit:]
    result = []
    for contrib in recent:
        result.append(f"{contrib['member']}: Ksh {contrib['amount']}")
    return result

def create_session(phone_number):
    """Create a new session for a user"""
    session_id = str(uuid.uuid4())
    sessions[session_id] = {
        "phone_number": phone_number,
        "created_at": datetime.now(),
        "state": "menu",
        "inputs": []
    }
    return session_id

def get_session(session_id):
    """Get or create a session"""
    if session_id not in sessions:
        return None
    return sessions[session_id]