import requests
import json
import os
from dotenv import load_dotenv

load_dotenv("/home/barely_engineer/Plocha/angel/.env")


def send_image(recipient_id, path_to_image):
    recipient_dict = {"id": recipient_id}
    message_dict = {"attachment": {"type": "image", "payload": {}}}
    payload = {
        "messaging_type": "UPDATE",  # this should let sending messages even after 24 hours after me messaging bot. Otherwise meta will block it
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

    aut = {"access_token": os.getenv("CONFIG_PAGE_ACCESS_TOKEN")}

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


send_image(os.getenv("RECIPIENT_ID"), "/home/barely_engineer/Plocha/angel/timetick.png")
