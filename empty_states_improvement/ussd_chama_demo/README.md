# ChamaConnect USSD Simulator

A complete USSD (Unstructured Supplementary Service Data) simulator for demonstrating group management features without requiring actual USSD gateway APIs.

## 🎯 Features

### Backend Features
- **Session Management**: Unique session IDs for each USSD user
- **Menu-Driven Navigation**: Hierarchical USSD menu structure with CON/END responses
- **State Management**: Tracks user inputs across multiple prompts
- **Mock Data**: Pre-populated group data with member contributions

### Frontend Features
- **Realistic Phone UI**: Mimics traditional USSD experience on mobile phones
- **Interactive Simulator**: Real-time USSD interaction with visual feedback
- **Live Statistics**: Dashboard showing group balance, member count, and status
- **Session History**: Track all interactions during a USSD session
- **Responsive Design**: Works on desktop, tablet, and mobile devices

## 📋 USSD Menu Structure

```
Main Menu
├── 1. View Balance → Display current group balance
├── 2. Contribute → Multi-step contribution process
│   ├── Enter amount
│   └── Enter name
├── 3. View Members → List all members and their contributions
├── 4. My Contributions → Check personal contribution total
│   └── Enter your name
└── 5. Recent Activity → View last 3 contributions
```

## 🚀 Quick Start

### Prerequisites
- Python 3.7+
- pip (Python package manager)

### Installation

1. **Navigate to the project directory**:
   ```bash
   cd ussd_chama_demo
   ```

2. **Install dependencies**:
   ```bash
   pip install -r requirements.txt
   ```

3. **Run the application**:
   ```bash
   python app.py
   ```

4. **Open your browser**:
   - Navigate to: `http://localhost:5000`
   - You should see the ChamaConnect USSD Simulator interface

## 💻 Usage Guide

### Web Interface (Frontend)

1. **Start a Session**:
   - Click "Start USSD Session"
   - Enter a phone number (or use default)
   - Mobile phone UI appears with main menu

2. **Navigate Menus**:
   - Enter menu choice (1-5) and click "Send"
   - Follow prompts for multi-step operations
   - View responses in real-time

3. **Examples**:
   - **View Balance**: Enter `1` → Shows group balance
   - **Contribute**: 
     - Enter `2` → Prompted for amount
     - Enter amount (e.g., `500`) → Prompted for name
     - Enter name (e.g., `John`) → Contribution recorded
   - **View Members**: Enter `3` → Lists all members
   - **My Contribution**: 
     - Enter `4` → Prompted for name
     - Enter name → Shows total contribution

4. **Session Controls**:
   - **Send**: Submit your choice/input
   - **End Session**: Terminate current USSD session
   - **Reset**: Clear everything and start fresh

### REST API (Backend)

#### Start USSD Session
```bash
POST /api/ussd/start
Content-Type: application/json

{
    "phoneNumber": "254700000000"
}

Response:
{
    "sessionId": "uuid-string",
    "message": "Welcome to ChamaConnect\n1. View Balance\n...",
    "status": "CON"
}
```

#### Send USSD Input
```bash
POST /api/ussd/send
Content-Type: application/json

{
    "sessionId": "uuid-string",
    "choice": "1"
}

Response:
{
    "message": "Chama Group Balance: Ksh 12500",
    "status": "END",
    "sessionId": "..."
}
```

#### Get Status
```bash
GET /api/status

Response:
{
    "groupName": "Group 15",
    "balance": 12500,
    "memberCount": 3,
    "members": [
        "John: Ksh 3500",
        "Mary: Ksh 4000",
        "Sidney: Ksh 5000"
    ]
}
```

#### Original USSD Endpoint
```bash
POST /ussd
Form Data:
- sessionId: session-id
- phoneNumber: 254700000000
- text: 1*500*John

Response:
END Contribution of Ksh 500 recorded successfully. Thank you, John!
```

## 📁 Project Structure

```
ussd_chama_demo/
├── app.py                 # Main Flask application
├── services.py            # Business logic and data operations
├── data.py               # Mock data storage
├── requirements.txt      # Python dependencies
├── templates/
│   └── index.html        # USSD simulator frontend
└── static/
    ├── style.css         # UI styling
    └── script.js         # Frontend interactivity
```

## 🔧 Customization Guide

### Add New Features

1. **Add Menu Option** in `app.py`:
   ```python
   elif inputs[0] == "6":  # New option
       response = "CON New Feature\n"
       response += "1. Sub-option 1\n"
       response += "2. Sub-option 2"
   ```

2. **Add Service Function** in `services.py`:
   ```python
   def new_feature():
       # Your logic here
       return result
   ```

3. **Update Mock Data** in `data.py`:
   ```python
   chama["newField"] = "value"
   ```

### Modify Mock Data

Edit `data.py` to change:
- Group name
- Initial balance
- Members and their contributions
- Historical transaction data

## 🎨 UI Customization

### Change Colors
Edit `static/style.css` - Update CSS variables:
```css
:root {
    --primary-color: #2ecc71;      /* Green */
    --secondary-color: #3498db;    /* Blue */
    --phone-screen: #00ff00;       /* USSD Green */
}
```

### Modify Phone Theme
Change phone display styling in CSS:
- `.phone-header`: Top bar
- `.screen-display`: Main display area
- `.button-group`: Input buttons

## 🧪 Testing

### Manual Testing Scenarios

1. **New User Session**:
   - Start → View Balance → End

2. **Multi-step Flow**:
   - Start → Contribute → Enter amount → Enter name → Verify

3. **Error Handling**:
   - Invalid amount → Should show error
   - Invalid choice → Should show error message

4. **Session Management**:
   - Multiple simultaneous sessions (use different sessions)

## 📱 USSD Status Codes

- **CON** (Continue): Menu awaiting user input - display message and keep session open
- **END**: Final response - end the session immediately

## 🔐 Security Notes

⚠️ **This is a simulator for demonstration purposes only**:
- All data is stored in memory (not persistent)
- No authentication implemented
- Not suitable for production use
- Phone numbers are not validated

For production USSD:
- Use actual USSD gateway (AfricastalKing, Pesalink, etc.)
- Implement proper authentication
- Use persistent database
- Add encryption and security measures
- Implement rate limiting

## 📊 What's Included

✅ Complete USSD backend simulation
✅ Realistic phone UI frontend
✅ REST API for testing
✅ Mock data with group information
✅ Session management
✅ Multi-step user flows
✅ Error handling
✅ Responsive design
✅ Interactive history tracking

## 🚀 Demo Flow

Perfect for showing stakeholders:
1. Open web interface
2. Start USSD session with demo phone number
3. Navigate through menu options
4. Show contribution process with validation
5. Display member information
6. Show real-time balance updates

## 🛠️ Troubleshooting

### Port Already in Use
```bash
# Change port in app.py
app.run(port=5001, debug=True)
```

### Module Not Found
```bash
pip install flask flask-cors
```

### CORS Issues
Already configured with `flask_cors`

### JavaScript Errors
Check browser console (F12) for errors

## 📈 Future Enhancements

- Loan request feature
- Loan repayment tracking
- Member withdrawal requests
- Group announcement system
- SMS notifications simulation
- Multi-language support
- Admin dashboard
- Transaction export to CSV
- Database persistence (SQLite/PostgreSQL)

## 📞 Support

For questions or issues:
1. Check the troubleshooting section
2. Review API documentation
3. Examine server logs (terminal output)
4. Test with simple scenarios first

## 📝 License

This is a demonstration project for ChamaConnect. Modify freely for your needs.

---

**Version**: 1.0  
**Last Updated**: April 2024  
**Built with**: Flask, JavaScript, HTML5, CSS3
