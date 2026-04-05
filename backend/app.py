from flask import Flask, render_template, jsonify, request
from flask_cors import CORS
from data import EMPTY_STATES, ACTIONABLE_SUGGESTIONS, LOADING_STATES, get_skeleton_loader
import json

app = Flask(__name__, static_folder='../frontend/static', template_folder='../frontend/templates')
CORS(app)

# ==================== EMPTY STATES API ====================

@app.route('/')
def index():
    """Serve empty states demo page"""
    return render_template('index.html')

@app.route('/api/empty-states')
def get_empty_states():
    """Get all empty state templates"""
    return jsonify({
        "states": EMPTY_STATES,
        "count": len(EMPTY_STATES)
    })

@app.route('/api/empty-states/<state_type>')
def get_empty_state(state_type):
    """Get specific empty state"""
    state = EMPTY_STATES.get(state_type)
    if not state:
        return jsonify({"error": "State not found"}), 404
    
    return jsonify({
        "type": state_type,
        "state": state,
        "suggestions": ACTIONABLE_SUGGESTIONS.get(state_type, [])
    })

@app.route('/api/loading-state/<state_type>')
def get_loading_state(state_type):
    """Get loading state animation"""
    state = LOADING_STATES.get(state_type, LOADING_STATES["loading_chamas"])
    
    return jsonify({
        "type": state_type,
        "message": state["message"],
        "animation": state["animation"]
    })

@app.route('/api/skeleton/<skeleton_type>')
def get_skeleton(skeleton_type):
    """Get skeleton loader HTML"""
    html = get_skeleton_loader(skeleton_type)
    
    return jsonify({
        "type": skeleton_type,
        "html": html
    })

@app.route('/api/demo/chamas')
def demo_chamas():
    """Get demo chamas - can return empty"""
    show_empty = request.args.get('empty', 'true').lower() == 'true'
    
    if show_empty:
        return jsonify({
            "chamas": [],
            "empty_state": EMPTY_STATES["no_chamas"]
        })
    else:
        # Return sample data
        return jsonify({
            "chamas": [
                {
                    "id": "1",
                    "name": "Mama Pambazuko Savers",
                    "members": 5,
                    "balance": 25000,
                    "type": "monthly_savings"
                }
            ],
            "empty_state": None
        })

@app.route('/api/demo/contributions')
def demo_contributions():
    """Get demo contributions - can return empty"""
    show_empty = request.args.get('empty', 'true').lower() == 'true'
    
    if show_empty:
        return jsonify({
            "contributions": [],
            "empty_state": EMPTY_STATES["no_contributions"]
        })
    else:
        return jsonify({
            "contributions": [
                {"member": "John", "amount": 500, "date": "2024-04-01"},
                {"member": "Jane", "amount": 500, "date": "2024-04-01"}
            ],
            "empty_state": None
        })

@app.route('/api/illustration/<illustration_type>')
def get_illustration(illustration_type):
    """Get SVG illustration for empty state"""
    illustrations = {
        "empty_chama": '''
            <svg viewBox="0 0 200 200" xmlns="http://www.w3.org/2000/svg">
                <circle cx="100" cy="80" r="30" fill="#e5e7eb" opacity="0.3"/>
                <path d="M 60 120 Q 60 160 100 160 Q 140 160 140 120" stroke="#e5e7eb" stroke-width="2" fill="none" opacity="0.3"/>
                <circle cx="100" cy="100" r="50" fill="none" stroke="#e5e7eb" stroke-width="2" opacity="0.2" stroke-dasharray="5,5"/>
            </svg>
        ''',
        "empty_contributions": '''
            <svg viewBox="0 0 200 200" xmlns="http://www.w3.org/2000/svg">
                <rect x="40" y="60" width="120" height="80" rx="5" fill="none" stroke="#e5e7eb" stroke-width="2" opacity="0.3"/>
                <line x1="50" y1="90" x2="150" y2="90" stroke="#e5e7eb" stroke-width="1" opacity="0.3"/>
                <line x1="50" y1="110" x2="150" y2="110" stroke="#e5e7eb" stroke-width="1" opacity="0.3"/>
                <line x1="50" y1="130" x2="150" y2="130" stroke="#e5e7eb" stroke-width="1" opacity="0.3"/>
                <text x="100" y="100" text-anchor="middle" fill="#e5e7eb" opacity="0.3">+</text>
            </svg>
        ''',
        "empty_members": '''
            <svg viewBox="0 0 200 200" xmlns="http://www.w3.org/2000/svg">
                <circle cx="100" cy="60" r="20" fill="none" stroke="#e5e7eb" stroke-width="2" opacity="0.3"/>
                <path d="M 70 100 L 70 140 L 130 140 L 130 100 Q 100 85 70 100" stroke="#e5e7eb" stroke-width="2" fill="none" opacity="0.3"/>
                <circle cx="70" cy="140" r="8" fill="none" stroke="#e5e7eb" stroke-width="2" opacity="0.2"/>
                <circle cx="130" cy="140" r="8" fill="none" stroke="#e5e7eb" stroke-width="2" opacity="0.2"/>
            </svg>
        '''
    }
    
    return jsonify({
        "type": illustration_type,
        "svg": illustrations.get(illustration_type, "")
    })

@app.route('/api/action-items/<scenario>')
def get_action_items(scenario):
    """Get actionable suggestions for specific scenario"""
    items = ACTIONABLE_SUGGESTIONS.get(scenario, [])
    
    return jsonify({
        "scenario": scenario,
        "items": items,
        "count": len(items)
    })


if __name__ == '__main__':
    app.run(port=5002, debug=True)
