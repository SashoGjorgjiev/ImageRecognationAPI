from flask import Flask, render_template, request, jsonify
from tensorflow.keras.applications.mobilenet_v2 import MobileNetV2, preprocess_input, decode_predictions
from PIL import Image
from flask_limiter import Limiter
from flask_limiter.util import get_remote_address
from sendgrid import SendGridAPIClient
from sendgrid.helpers.mail import Mail
from dotenv import load_dotenv
import numpy as np
import re
import sqlite3  # Import SQLite
import os

# Load environment variables from .env file
load_dotenv()
# Initialize Flask app
app = Flask(__name__)

SENDGRID_API_KEY = os.getenv("SENDGRID_API_KEY")

# SQLite database file
DATABASE = "signups.db"

# Create the database and table if they don't exist
def init_db():
    with sqlite3.connect(DATABASE) as conn:
        conn.execute("""
            CREATE TABLE IF NOT EXISTS signups (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                email TEXT NOT NULL UNIQUE,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            )
        """)

# Initialize the database
init_db()

# Helper function to validate emails
def is_valid_email(email):
    pattern = r"^[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+$"
    return re.match(pattern, email) is not None

# Serve the landing page
@app.route("/")
def home():
    return render_template("index.html")

# Handle sign-ups
from sendgrid import SendGridAPIClient
from sendgrid.helpers.mail import Mail

# SendGrid API key
SENDGRID_API_KEY = os.getenv("SENDGRID_API_KEY")

def send_confirmation_email(email):
    message = Mail(
        from_email="your_email@example.com",
        to_emails=email,
        subject="Welcome to Image Recognition API!",
        html_content="<strong>Thank you for signing up!</strong>"
    )
    try:
        sg = SendGridAPIClient(SENDGRID_API_KEY)
        response = sg.send(message)
        print(f"Email sent to {email}. Status code: {response.status_code}")
    except Exception as e:
        print(f"Error sending email: {e}")

limiter = Limiter(
    app=app,
    key_func=get_remote_address,
    default_limits=["100 per day", "10 per hour"]
)
# Update the signup route
@app.route("/signup", methods=["POST"])
@limiter.limit("5 per minute")
def signup():
    email = request.form.get("email")

    if not email:
        return jsonify({"success": False, "message": "Email is required."})

    if not is_valid_email(email):
        return jsonify({"success": False, "message": "Please enter a valid email address."})

    # Save the email to the database
    try:
        with sqlite3.connect(DATABASE) as conn:
            conn.execute("INSERT INTO signups (email) VALUES (?)", (email,))
        
        # Send confirmation email
        send_confirmation_email(email)
        
        return jsonify({"success": True, "message": "Thank you for signing up! Check your email for confirmation."})
    except sqlite3.IntegrityError:
        return jsonify({"success": False, "message": "This email is already registered."})

# Serve the image upload page
@app.route("/upload")
def upload():
    return render_template("upload.html")

@app.route("/privacy")
def privacy():
    return render_template("privacy.html")
# API endpoint for image recognition
@app.route("/recognize", methods=["POST"])
def recognize_image():
    # Check if an image was uploaded
    if "file" not in request.files:
        return jsonify({"error": "No file uploaded"}), 400

    # Load the image
    file = request.files["file"]
    image = Image.open(file).convert("RGB")
    image = image.resize((224, 224))  # Resize image to fit the model

    # Preprocess the image
    image_array = np.array(image)
    image_array = np.expand_dims(image_array, axis=0)
    image_array = preprocess_input(image_array)

    # Make a prediction
    predictions = model.predict(image_array)
    decoded_predictions = decode_predictions(predictions, top=3)[0]  # Get top 3 predictions

    # Format the results
    results = []
    for _, label, probability in decoded_predictions:
        results.append({"label": label, "probability": float(probability)})

    # Return the results as JSON
    return jsonify({"predictions": results})

# Run the app
if __name__ == "__main__":
    app.run(debug=True)