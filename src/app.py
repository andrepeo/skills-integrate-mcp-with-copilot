"""
High School Management System API

A super simple FastAPI application that allows students to view and sign up
for extracurricular activities at Mergington High School.
"""

from fastapi import FastAPI, HTTPException
from fastapi.staticfiles import StaticFiles
from fastapi.responses import RedirectResponse
import os
from pathlib import Path
# Encryption imports
from cryptography.fernet import Fernet

app = FastAPI(title="Mergington High School API",
              description="API for viewing and signing up for extracurricular activities")

# --- Encryption Setup ---
# In production, store this key securely!
ENCRYPTION_KEY = os.environ.get("HSMS_ENCRYPTION_KEY") or Fernet.generate_key()
fernet = Fernet(ENCRYPTION_KEY)

# Utility functions for encryption/decryption
def encrypt_email(email: str) -> str:
    return fernet.encrypt(email.encode()).decode()

def decrypt_email(token: str) -> str:
    return fernet.decrypt(token.encode()).decode()

# Mount the static files directory
current_dir = Path(__file__).parent
app.mount("/static", StaticFiles(directory=os.path.join(Path(__file__).parent,
          "static")), name="static")

# In-memory activity database
activities = {
    "Chess Club": {
        "description": "Learn strategies and compete in chess tournaments",
        "schedule": "Fridays, 3:30 PM - 5:00 PM",
        "max_participants": 12,
        "participants": [encrypt_email("michael@mergington.edu"), encrypt_email("daniel@mergington.edu")]
    },
    "Programming Class": {
        "description": "Learn programming fundamentals and build software projects",
        "schedule": "Tuesdays and Thursdays, 3:30 PM - 4:30 PM",
        "max_participants": 20,
        "participants": [encrypt_email("emma@mergington.edu"), encrypt_email("sophia@mergington.edu")]
    },
    "Gym Class": {
        "description": "Physical education and sports activities",
        "schedule": "Mondays, Wednesdays, Fridays, 2:00 PM - 3:00 PM",
        "max_participants": 30,
        "participants": [encrypt_email("john@mergington.edu"), encrypt_email("olivia@mergington.edu")]
    },
    "Soccer Team": {
        "description": "Join the school soccer team and compete in matches",
        "schedule": "Tuesdays and Thursdays, 4:00 PM - 5:30 PM",
        "max_participants": 22,
        "participants": [encrypt_email("liam@mergington.edu"), encrypt_email("noah@mergington.edu")]
    },
    "Basketball Team": {
        "description": "Practice and play basketball with the school team",
        "schedule": "Wednesdays and Fridays, 3:30 PM - 5:00 PM",
        "max_participants": 15,
        "participants": [encrypt_email("ava@mergington.edu"), encrypt_email("mia@mergington.edu")]
    },
    "Art Club": {
        "description": "Explore your creativity through painting and drawing",
        "schedule": "Thursdays, 3:30 PM - 5:00 PM",
        "max_participants": 15,
        "participants": [encrypt_email("amelia@mergington.edu"), encrypt_email("harper@mergington.edu")]
    },
    "Drama Club": {
        "description": "Act, direct, and produce plays and performances",
        "schedule": "Mondays and Wednesdays, 4:00 PM - 5:30 PM",
        "max_participants": 20,
        "participants": [encrypt_email("ella@mergington.edu"), encrypt_email("scarlett@mergington.edu")]
    },
    "Math Club": {
        "description": "Solve challenging problems and participate in math competitions",
        "schedule": "Tuesdays, 3:30 PM - 4:30 PM",
        "max_participants": 10,
        "participants": [encrypt_email("james@mergington.edu"), encrypt_email("benjamin@mergington.edu")]
    },
    "Debate Team": {
        "description": "Develop public speaking and argumentation skills",
        "schedule": "Fridays, 4:00 PM - 5:30 PM",
        "max_participants": 12,
        "participants": [encrypt_email("charlotte@mergington.edu"), encrypt_email("henry@mergington.edu")]
    }
}


@app.get("/")
def root():
    return RedirectResponse(url="/static/index.html")


@app.get("/activities")
def get_activities():
    # Return activities with decrypted participant emails
    decrypted_activities = {}
    for name, info in activities.items():
        decrypted_info = info.copy()
        decrypted_info["participants"] = [decrypt_email(e) for e in info["participants"]]
        decrypted_activities[name] = decrypted_info
    return decrypted_activities


@app.post("/activities/{activity_name}/signup")
def signup_for_activity(activity_name: str, email: str):
    """
    Sign up a student for an activity
    Biometric authentication placeholder:
    # TODO: Integrate biometric authentication here (e.g., fingerprint, face recognition)
    """
    # Validate activity exists
    if activity_name not in activities:
        raise HTTPException(status_code=404, detail="Activity not found")

    # Get the specific activity
    activity = activities[activity_name]

    # Encrypt email for comparison
    encrypted_email = encrypt_email(email)

    # Validate student is not already signed up
    if encrypted_email in activity["participants"]:
        raise HTTPException(
            status_code=400,
            detail="Student is already signed up"
        )

    # Add student (encrypted)
    activity["participants"].append(encrypted_email)
    return {"message": f"Signed up {email} for {activity_name}"}


@app.delete("/activities/{activity_name}/unregister")
def unregister_from_activity(activity_name: str, email: str):
    """
    Unregister a student from an activity
    Biometric authentication placeholder:
    # TODO: Integrate biometric authentication here (e.g., fingerprint, face recognition)
    """
    # Validate activity exists
    if activity_name not in activities:
        raise HTTPException(status_code=404, detail="Activity not found")

    # Get the specific activity
    activity = activities[activity_name]

    encrypted_email = encrypt_email(email)

    # Validate student is signed up
    if encrypted_email not in activity["participants"]:
        raise HTTPException(
            status_code=400,
            detail="Student is not signed up for this activity"
        )

    # Remove student (encrypted)
    activity["participants"].remove(encrypted_email)
    return {"message": f"Unregistered {email} from {activity_name}"}
