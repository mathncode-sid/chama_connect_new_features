from flask import Flask, request, Response, jsonify, render_template, send_from_directory
from flask_cors import CORS
from services import (
    get_balance, get_members, add_contribution, get_member_contribution,
    get_all_members_with_contributions, get_recent_contributions,
    create_session, get_session, get_member_details
)
from data import chama
import os
import json

app = Flask(__name__, static_folder='static', template_folder='templates')
CORS(app)

# ==================== USSD BACKEND API ====================
@app.route('/ussd', methods=['POST'])
def ussd():
    """Main USSD endpoint - handles menu navigation"""
    session_id = request.form.get('sessionId')
    phone_number = request.form.get('phoneNumber')
    text = request.form.get('text', '')

    # Split user input
    inputs = text.split("*") if text else []

    response = ""

    # MAIN MENU
    if text == "":
        response = "CON Welcome to ChamaConnect\n"
        response += "1. View Balance\n"
        response += "2. Contribute\n"
        response += "3. View Members\n"
        response += "4. My Contributions\n"
        response += "5. Recent Activity"

    # VIEW BALANCE
    elif inputs[0] == "1":
        balance = get_balance()
        response = f"END Chama Group Balance: Ksh {balance}"

    # CONTRIBUTE - STEP 1
    elif inputs[0] == "2" and len(inputs) == 1:
        response = "CON Enter amount to contribute:"

    # CONTRIBUTE - STEP 2 (Amount entered)
    elif inputs[0] == "2" and len(inputs) == 2:
        try:
            amount = int(inputs[1])
            if amount < 100:
                response = "END Minimum contribution is Ksh 100"
            else:
                response = "CON Enter your name:"
        except:
            response = "END Invalid amount"

    # CONTRIBUTE - STEP 3 (Name entered)
    elif inputs[0] == "2" and len(inputs) == 3:
        try:
            amount = int(inputs[1])
            name = inputs[2]
            add_contribution(name, amount)
            response = f"END Contribution of Ksh {amount} recorded successfully. Thank you, {name}!"
        except:
            response = "END Error processing contribution"

    # VIEW MEMBERS
    elif inputs[0] == "3":
        members = get_all_members_with_contributions()
        member_list = "\n".join(members)
        response = f"END Members:\n{member_list}"

    # MY CONTRIBUTIONS
    elif inputs[0] == "4" and len(inputs) == 1:
        response = "CON Enter your name:"

    # MY CONTRIBUTIONS - STEP 2
    elif inputs[0] == "4" and len(inputs) == 2:
        name = inputs[1]
        amount = get_member_contribution(name)
        if amount > 0:
            response = f"END Your total contribution: Ksh {amount}"
        else:
            response = f"END No contributions found for {name}"

    # RECENT ACTIVITY
    elif inputs[0] == "5":
        recent = get_recent_contributions(3)
        activity_list = "\n".join(recent)
        response = f"END Recent Contributions:\n{activity_list}"

    else:
        response = "END Invalid choice. Please try again."

    return Response(response, mimetype="text/plain")


# ==================== WEB FRONTEND API ====================
@app.route('/')
def index():
    """Serve the USSD simulator frontend"""
    return render_template('index.html')


@app.route('/api/ussd/start', methods=['POST'])
def start_ussd():
    """Start a new USSD session"""
    data = request.json
    phone_number = data.get('phoneNumber', '254700000000')
    
    session_id = create_session(phone_number)
    
    # Get initial menu
    response = "Welcome to ChamaConnect\n"
    response += "1. View Balance\n"
    response += "2. Contribute\n"
    response += "3. View Members\n"
    response += "4. My Contributions\n"
    response += "5. Recent Activity"
    
    return jsonify({
        "sessionId": session_id,
        "message": response,
        "status": "CON"
    })


@app.route('/api/ussd/send', methods=['POST'])
def send_ussd():
    """Send input and continue USSD flow"""
    data = request.json
    session_id = data.get('sessionId')
    choice = data.get('choice', '')
    
    session = get_session(session_id)
    if not session:
        return jsonify({"error": "Invalid session"}), 400
    
    # Handle the USSD logic
    response = process_ussd_input(session, choice)
    
    return jsonify(response)


def process_ussd_input(session, user_input):
    """Process USSD input and return response"""
    # Build text from inputs
    session["inputs"].append(user_input)
    text = "*".join(session["inputs"]) if session["inputs"] and user_input else ""
    
    # Use the same logic as POST endpoint
    inputs = text.split("*") if text else []
    
    # MAIN MENU
    if not session["inputs"] or (len(session["inputs"]) == 1 and user_input == "0"):
        session["inputs"] = []
        message = "Welcome to ChamaConnect\n"
        message += "1. View Balance\n"
        message += "2. Contribute\n"
        message += "3. View Members\n"
        message += "4. My Contributions\n"
        message += "5. Recent Activity"
        return {"message": message, "status": "CON", "sessionId": session}
    
    # VIEW BALANCE
    if inputs[0] == "1":
        balance = get_balance()
        session["inputs"] = []
        return {"message": f"Chama Group Balance: Ksh {balance}", "status": "END", "sessionId": session}
    
    # CONTRIBUTE
    elif inputs[0] == "2":
        if len(inputs) == 1:
            return {"message": "Enter amount to contribute:", "status": "CON", "sessionId": session}
        elif len(inputs) == 2:
            try:
                amount = int(inputs[1])
                if amount < 100:
                    session["inputs"] = []
                    return {"message": "Minimum contribution is Ksh 100", "status": "END", "sessionId": session}
                return {"message": "Enter your name:", "status": "CON", "sessionId": session}
            except:
                session["inputs"] = []
                return {"message": "Invalid amount", "status": "END", "sessionId": session}
        elif len(inputs) == 3:
            try:
                amount = int(inputs[1])
                name = inputs[2]
                add_contribution(name, amount)
                session["inputs"] = []
                return {"message": f"Contribution of Ksh {amount} recorded successfully. Thank you, {name}!", "status": "END", "sessionId": session}
            except:
                session["inputs"] = []
                return {"message": "Error processing contribution", "status": "END", "sessionId": session}
    
    # VIEW MEMBERS
    elif inputs[0] == "3":
        members = get_all_members_with_contributions()
        member_list = "\n".join(members)
        session["inputs"] = []
        return {"message": f"Members:\n{member_list}", "status": "END", "sessionId": session}
    
    # MY CONTRIBUTIONS
    elif inputs[0] == "4":
        if len(inputs) == 1:
            return {"message": "Enter your name:", "status": "CON", "sessionId": session}
        elif len(inputs) == 2:
            name = inputs[1]
            amount = get_member_contribution(name)
            session["inputs"] = []
            if amount > 0:
                return {"message": f"Your total contribution: Ksh {amount}", "status": "END", "sessionId": session}
            else:
                return {"message": f"No contributions found for {name}", "status": "END", "sessionId": session}
    
    # RECENT ACTIVITY
    elif inputs[0] == "5":
        recent = get_recent_contributions(3)
        activity_list = "\n".join(recent)
        session["inputs"] = []
        return {"message": f"Recent Contributions:\n{activity_list}", "status": "END", "sessionId": session}
    
    else:
        session["inputs"] = []
        return {"message": "Invalid choice. Please try again.", "status": "END", "sessionId": session}


@app.route('/api/status', methods=['GET'])
def status():
    """Get chama group status"""
    return jsonify({
        "groupName": chama["name"],
        "balance": get_balance(),
        "memberCount": len(get_members()),
        "members": get_all_members_with_contributions()
    })


if __name__ == '__main__':
    app.run(port=5000, debug=True)