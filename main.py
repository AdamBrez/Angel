from flask import Flask, request
from google import genai
from google.genai import types
import requests
import json
import os

# from config import CONFIG_PAGE_ACCESS_TOKEN, CONFIG_VERIFY_TOKEN
from commands import pick_command, verify_command_img, verify_command_text
from random import randint

app = Flask(__name__)

# tady mam dat heslo pro overeni a musi se shodovat s tim na Facebooku#tady mam dat heslo pro overeni a musi se shodovat s tim na Facebooku#tady mam dat heslo pro overeni a musi se shodovat s tim na Facebooku
VERIFY_TOKEN = os.environ.get("CONFIG_VERIFY_TOKEN")
PAGE_ACCESS_TOKEN = os.environ.get("CONFIG_PAGE_ACCESS_TOKEN")

# Inicialization of Gemini
client = genai.Client()

grounding_tool = types.Tool(google_search=types.GoogleSearch())

config = types.GenerateContentConfig(
    tools=[grounding_tool], system_instruction="Answer formally and briefly."
)


def send_message(recipient_id, text):
    # data ktere se poslou na fb
    payload = {
        "messaging_type": "RESPONSE",
        "recipient": {"id": recipient_id},
        "message": {"text": text},
    }

    aut = {"access_token": PAGE_ACCESS_TOKEN}

    try:
        response = requests.post(
            "https://graph.facebook.com/v18.0/me/messages", params=aut, json=payload
        )

        print("Odpoved od FB:", response.text)
    except Exception as e:
        print(f"Chyba pri odesilani: {e}")


def send_image(recipient_id, path_to_image):
    # data ktere se poslou na fb
    recipient_dict = {"id": recipient_id}
    message_dict = {"attachment": {"type": "image", "payload": {}}}
    payload = {
        "recipient": json.dumps(recipient_dict),
        "message": json.dumps(message_dict),
    }

    files = {
        "filedata": (
            "image.png",
            open(path_to_image, "rb"),
            "image/png",
        )
    }

    aut = {"access_token": PAGE_ACCESS_TOKEN}

    try:
        response = requests.post(
            "https://graph.facebook.com/v18.0/me/messages",
            params=aut,
            data=payload,
            files=files,
        )

        print("Odpoved od FB:", response.text)
    except Exception as e:
        print(f"Chyba pri odesilani: {e}")


@app.route("/webhook", methods=["GET"])
def verify():
    mode = request.args.get("hub.mode")
    token = request.args.get("hub.verify_token")
    challenge = request.args.get("hub.challenge")

    print(token)
    if mode and token:
        if mode == "subscribe" and token == VERIFY_TOKEN:
            print("webhook uspesne overen")

            return challenge, 200

        else:
            # spatne heslo
            return "Forbidden", 403
    return "Bad Request", 400


@app.route("/webhook", methods=["POST"])
def handle_messages():
    body = request.get_json()

    if body.get("object") == "page":
        for entry in body["entry"]:
            messaging_events = entry.get("messaging", [])
            for event in messaging_events:
                if "message" in event and "text" in event["message"]:
                    print("--NOVA ZPRAVA--")
                    sender_id = event["sender"]["id"]
                    message_text = event["message"]["text"]
                    print(message_text)
                    if "gemini" in message_text:
                        response = client.models.generate_content(
                            model="gemini-2.5-flash-lite",
                            contents=message_text[9:],
                            config=config,
                        )
                        send_message(sender_id, response.text)

                    elif verify_command_text(message_text):
                        send_message(sender_id, pick_command(message_text))

                    elif verify_command_img(message_text):
                        send_image(sender_id, pick_command(message_text))
                    else:
                        # odpoved = f"Napsal jsi: {message_text}"
                        # send_message(sender_id, odpoved)
                        send_image(
                            sender_id,
                            f"/home/barely_engineer/Plocha/angel/kitties/kitty{randint(1, 3)}.PNG",
                        )

        return "EVENT RECEIVED", 200
    else:
        return "Not Found", 404


if __name__ == "__main__":
    app.run(host="0.0.0.0", port="8888", debug=True)
