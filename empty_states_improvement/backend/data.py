# Mock data for empty states demo
from datetime import datetime, timedelta
import random

# Empty state templates
EMPTY_STATES = {
    "no_chamas": {
        "title": "No Chamas Yet",
        "description": "You haven't created any chama groups yet. Create your first one to start saving with your community!",
        "icon": "🌍",
        "cta": "Create Your First Chama",
        "secondary_cta": "Learn More",
        "illustration": "empty_chama"
    },
    "no_contributions": {
        "title": "No Contributions Yet",
        "description": "Your chama hasn't received any contributions. Members can contribute via USSD (*384*51#) or the mobile app.",
        "icon": "💰",
        "cta": "Share USSD Code",
        "secondary_cta": "Invite Members",
        "illustration": "empty_contributions",
        "hint": "Members: Send contributions using your phone shortcode"
    },
    "no_members": {
        "title": "No Members Yet",
        "description": "Your chama is waiting for members. Invite your friends and family to join your savings group.",
        "icon": "👥",
        "cta": "Invite Members",
        "secondary_cta": "Send SMS Invite",
        "illustration": "empty_members",
        "hint": "You are the only member right now"
    },
    "no_loans": {
        "title": "No Loan Requests",
        "description": "No active loan requests. Members can request loans once the chama is active.",
        "icon": "📋",
        "cta": "View Loan Policies",
        "secondary_cta": "Create Loan Product",
        "illustration": "empty_loans"
    },
    "no_payouts": {
        "title": "No Payouts Yet",
        "description": "Payouts will begin according to your chama's rotation schedule. First payout coming soon!",
        "icon": "📅",
        "cta": "View Schedule",
        "secondary_cta": "Edit Preferences",
        "illustration": "empty_payouts",
        "hint": "Next payout in 15 days"
    },
    "no_transactions": {
        "title": "No Transaction History",
        "description": "All your chama transactions will appear here. Start with your first contribution!",
        "icon": "📊",
        "cta": "Make Contribution",
        "secondary_cta": "Download Report",
        "illustration": "empty_transactions"
    }
}

# Sample suggestions for empty states
ACTIONABLE_SUGGESTIONS = {
    "first_chama": [
        "Start small with 3-5 trusted friends",
        "Keep contribution amounts realistic",
        "Set monthly or weekly schedule",
        "Choose rotating payout for fairness"
    ],
    "no_contributions": [
        "Share USSD code: *384*51#",
        "Send SMS reminders to members",
        "Set up auto-reminders",
        "Track who hasn't contributed yet"
    ],
    "onboarding": [
        "Complete your profile",
        "Add profile picture",
        "Set up M-Pesa confirmation",
        "Enable notifications"
    ]
}

# Loading states
LOADING_STATES = {
    "loading_chamas": {
        "message": "Loading your chamas...",
        "animation": "pulse"
    },
    "loading_contributions": {
        "message": "Fetching contributions...",
        "animation": "pulse"
    },
    "loading_members": {
        "message": "Getting member list...",
        "animation": "pulse"
    }
}

# Skeleton loaders
def get_skeleton_loader(type_):
    """Get skeleton loader HTML for different data types"""
    skeletons = {
        "card": """
            <div class="skeleton-card">
                <div class="skeleton-header"></div>
                <div class="skeleton-content">
                    <div class="skeleton-line" style="width: 80%;"></div>
                    <div class="skeleton-line" style="width: 60%;"></div>
                    <div class="skeleton-line" style="width: 70%;"></div>
                </div>
            </div>
        """,
        "table": """
            <div class="skeleton-table">
                <div class="skeleton-row">
                    <div class="skeleton-cell" style="width: 20%;"></div>
                    <div class="skeleton-cell" style="width: 30%;"></div>
                    <div class="skeleton-cell" style="width: 25%;"></div>
                    <div class="skeleton-cell" style="width: 25%;"></div>
                </div>
                <div class="skeleton-row">
                    <div class="skeleton-cell" style="width: 20%;"></div>
                    <div class="skeleton-cell" style="width: 30%;"></div>
                    <div class="skeleton-cell" style="width: 25%;"></div>
                    <div class="skeleton-cell" style="width: 25%;"></div>
                </div>
            </div>
        """,
        "list": """
            <div class="skeleton-list">
                <div class="skeleton-item"></div>
                <div class="skeleton-item"></div>
                <div class="skeleton-item"></div>
            </div>
        """
    }
    return skeletons.get(type_, skeletons["card"])
