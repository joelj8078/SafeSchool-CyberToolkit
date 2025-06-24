import random
from datetime import datetime

# Sample data
CATEGORIES = {
    "Login Scam": {
        "froms": ["support@secure-login.net", "account@verifier-alert.com"],
        "subjects": [
            "Unusual sign-in activity detected",
            "Action Required: Verify your account",
            "Your password has been compromised!"
        ],
        "bodies": [
            "We detected a login attempt from an unrecognized device. Please verify immediately.",
            "Your account will be locked in 24 hours if not verified.",
            "Click the link below to reset your password and secure your account."
        ],
        "links": ["http://secure-login.net/verify", "http://login-checker.com/reset"]
    },
    "Prize Scam": {
        "froms": ["lottery@luckydraw-global.net", "promo@amz-rewards.co"],
        "subjects": [
            "Congratulations! You’ve won a $500 Amazon gift card",
            "You are the lucky winner of this week’s jackpot!",
            "Claim your prize now before it expires"
        ],
        "bodies": [
            "You were randomly selected for this amazing giveaway. Don’t miss out!",
            "Please confirm your details to receive the prize.",
            "No purchase necessary. But you must act now!"
        ],
        "links": ["http://luckydraw-global.net/secure-claim", "http://amz-rewards.co/win"]
    },
    "Fake Invoice": {
        "froms": ["billing@office365-support.org", "finance@quickbooksbill.net"],
        "subjects": [
            "Invoice #928471 due today",
            "Billing Reminder: Payment Required",
            "Last Warning: Overdue Invoice"
        ],
        "bodies": [
            "Your subscription invoice is overdue. Please make the payment now.",
            "Click to view and complete your pending invoice before services are paused.",
            "Your access will be restricted until payment is received."
        ],
        "links": ["http://office365-support.org/pay", "http://quickbooksbill.net/invoice"]
    },
    "Tech Support Scam": {
        "froms": ["support@windows-secure.com", "alert@techcare247.org"],
        "subjects": [
            "Critical System Alert: Virus Detected!",
            "Your computer is at risk!",
            "Immediate action required – Security breach"
        ],
        "bodies": [
            "We detected malware on your PC. Contact support immediately.",
            "Call our toll-free number now to fix this issue and avoid data loss.",
            "Don’t ignore this warning. Your personal info is in danger."
        ],
        "links": ["http://windows-secure.com/support", "http://techcare247.org/help"]
    },
    "Fake Update": {
        "froms": ["noreply@systemupdate-service.com", "update@criticalpatch.net"],
        "subjects": [
            "Install Critical Browser Security Update Now",
            "Update Required: Flash Player",
            "Your system is outdated – urgent patch needed"
        ],
        "bodies": [
            "Download the latest update now to protect your system.",
            "Failure to install may lead to vulnerabilities.",
            "Secure your browser and system with one click."
        ],
        "links": ["http://systemupdate-service.com/download", "http://criticalpatch.net/update"]
    }
}

def generate_phishing_email():
    category = random.choice(list(CATEGORIES.keys()))
    data = CATEGORIES[category]

    phishing_email = {
        "category": category,
        "from": random.choice(data["froms"]),
        "subject": random.choice(data["subjects"]),
        "body": random.choice(data["bodies"]),
        "link": random.choice(data["links"]),
        "generated_at": datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    }

    return phishing_email

# CLI Test
if __name__ == "__main__":
    email = generate_phishing_email()
    print("📧 Phishing Email Simulation")
    print("------------------------------")
    print(f"🗂️  Category: {email['category']}")
    print(f"🧑‍💻 From: {email['from']}")
    print(f"📨 Subject: {email['subject']}\n")
    print(f"📄 Body:\n{email['body']}\n")
    print(f"🔗 Link: {email['link']}")
    print(f"⏱️ Generated on: {email['generated_at']}")
