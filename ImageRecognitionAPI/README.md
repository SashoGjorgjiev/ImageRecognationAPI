# ImageRecognationAPI
# Image Recognition API

![Python](https://img.shields.io/badge/Python-3.8%2B-blue)
![Flask](https://img.shields.io/badge/Flask-2.0%2B-green)
![SendGrid](https://img.shields.io/badge/SendGrid-API-orange)

The **Image Recognition API** is a powerful tool that uses a pre-trained deep learning model to identify objects, scenes, and more in images. It’s built with **Flask** and integrates with **SendGrid** for email notifications. Whether you're building an e-commerce platform, a social media app, or an educational tool, this API can help you automate image analysis and enhance user experience.

---

## Features

- **Accurate Predictions**: Identify objects, scenes, and more with high accuracy using a pre-trained MobileNetV2 model.
- **Easy Integration**: Simple RESTful API endpoints for seamless integration into your applications.
- **Email Notifications**: Send confirmation emails to users using SendGrid.
- **Scalable**: Designed to handle thousands of requests per second.
- **Privacy-First**: Includes a privacy policy to ensure user data is protected.

---

## How It Works

1. **Upload an Image**: Users upload an image to the API.
2. **Analyze the Image**: The API processes the image using a deep learning model.
3. **Return Predictions**: The API returns the top predictions with confidence scores.
4. **Send Confirmation**: Optionally, send a confirmation email to the user.

---

## Getting Started

### Prerequisites

- Python 3.8+
- Flask
- TensorFlow
- SendGrid API Key

### Installation

1. Clone the repository:
   ```bash
   https://github.com/SashoGjorgjiev/ImageRecognationAPI.git
   
Install the dependencies:

bash
Copy
pip install -r requirements.txt
Set up environment variables:

Create a .env file in the project root.

Add your SendGrid API key:

Copy
SENDGRID_API_KEY=your_sendgrid_api_key
Run the Flask app:

bash
Copy
python app.py
Open your browser and go to http://127.0.0.1:5000/.

API Endpoints
1. Recognize an Image
URL: /recognize

Method: POST

Request Body:

file: Image file to upload.

Response:

json
Copy
{
  "predictions": [
    {"label": "tabby", "confidence": "40.5%"},
    {"label": "tiger_cat", "confidence": "19.5%"},
    {"label": "Egyptian_cat", "confidence": "10.7%"}
  ],
  "top_prediction": {
    "label": "tabby",
    "confidence": "40.5%"
  }
}
2. Sign Up
URL: /signup

Method: POST

Request Body:

email: User's email address.

Response:

json
Copy
{
  "success": true,
  "message": "Thank you for signing up! Check your email for confirmation."
}
