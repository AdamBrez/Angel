import os
from random import randint


def help_command():
    return """
    possible command to use:
-cevent -> closest upcoming event

-meme -> sends a meme
    
-progress -> progress of my NY resolutions
    
-nicepic -> send a pic from collection
    
-booklist -> list of books to read
    
-filmlist -> list of films to watch
    """


def events():
    return """
digitalni cesko / Praha / 13.3.
opensearchcon / Praha / 16-17.4.
bis 2026 / Praha / 10-12.6.
devconf / Brno / 18-19.6.
cyber_con / Brno / 9-10.9.
frontkon / Praha / 6.10.
open source summit / Praha / 7-9.10.
    """


def filmlist(new_title=None):
    if new_title is None:
        with open("lists/filmlist.txt", "r") as file:
            return file.read()

    else:
        with open("lists/filmlist.txt", "r+") as file:
            file.write(f"{new_title}\n")
            return file.read()


def booklist(new_title=None):
    if new_title is None:
        with open("lists/booklist.txt", "r") as file:
            return file.read()

    else:
        with open("lists/booklist.txt", "r+") as file:
            file.write(f"{new_title}\n")
            return file.read()


def pick_pic():
    path = "/home/barely_engineer/Plocha/angel/nicepics/"
    chosen_pic = f"/home/barely_engineer/Plocha/angel/nicepics/nicepic{randint(1, len(os.listdir(path)))}.PNG"
    return chosen_pic


#####################################################
# Functions for the logic of the agent are down below#
#####################################################


def verify_command_text(sent_text):
    commands = [
        "-events",
        "-cevent",
        "-booklist",
        "-filmlist",
        "-help",
    ]
    if sent_text.lower() in commands:
        return True
    else:
        return False


def verify_command_img(sent_text):
    commands = [
        "-meme",
        "-progress",
        "-nicepic",
    ]
    if sent_text.lower() in commands:
        return True
    else:
        return False


def pick_command(sent_command):
    sent_command = sent_command.lower()

    commands = {
        "-help": help_command(),
        "-filmlist": filmlist(),
        "-events": events(),
        "-booklist": booklist(),
        "-nicepic": pick_pic(),
    }

    return commands[sent_command]
