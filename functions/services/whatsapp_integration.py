import os
import requests
from flask import jsonify

WHATSAPP_TOKEN = 'EAAMpORPeebYBO288cv1GJjes4l42d8TTmzGsH2JduD09j55ZCEio1t7IHZBVhjD3w0wWxFXfhPSAAEZB4vNc8hiZAtnq9DjA6v02E8STrvoHdQqLVDRfPOBHZCQjnd48GQEiDZBBxBKpheY6hcYTU0sN5RuZAQuPxuRZBrTGJiuxKfXi9n1HVWEukd7BQdjLFZBd7PtZAl0tZA38FlIBHvJ'
WHATSAPP_PHONE_ID = '463155706880767'
WHATSAPP_VERSION = 'v20.0'
WHATSAPP_API_URL = f"https://graph.facebook.com/{WHATSAPP_VERSION}/{WHATSAPP_PHONE_ID}/messages"

def send_whatsapp_message(message, number):
    try:
        headers = {
            "Authorization": f"Bearer {WHATSAPP_TOKEN}",
            "Content-Type": "application/json"
        }
        payload = {
            "messaging_product": "whatsapp",
            "to": number,
            "type": "text",
            "text": {
                "body": message
            }
        }

        response = requests.post(WHATSAPP_API_URL, headers=headers, json=payload)

        response.raise_for_status()

        
        return jsonify({"message": "Mensaje enviado"}), 200

    except Exception as e:
        return jsonify({"error": str(e)}), 400

