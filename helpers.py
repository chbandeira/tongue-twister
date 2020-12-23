import os
import requests
import urllib.parse
import speech_recognition as sr

from flask import redirect, render_template, request, session
from functools import wraps
from os import path
from pydub import AudioSegment
from difflib import SequenceMatcher


def error(message, code=400):
    """Render message as an error to user."""
    def escape(s):
        """
        Escape special characters.

        https://github.com/jacebrowning/memegen#special-characters
        """
        for old, new in [("-", "--"), (" ", "-"), ("_", "__"), ("?", "~q"),
                         ("%", "~p"), ("#", "~h"), ("/", "~s"), ("\"", "''")]:
            s = s.replace(old, new)
        return s
    return render_template("error.html", top=code, bottom=message), code


def login_required(f):
    """
    Decorate routes to require login.

    http://flask.pocoo.org/docs/1.0/patterns/viewdecorators/
    """
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if session.get("user_id") is None:
            return redirect("/login")
        return f(*args, **kwargs)
    return decorated_function


def recognize():
    """Convert audio from file to text"""
    # convert webm to wav
    sound = AudioSegment.from_file("assets/audio.webm", "webm")
    sound.export("assets/audio.wav", format="wav")

    # obtain path to "audio.wav" in the same folder as this script
    AUDIO_FILE = path.join(path.dirname(path.realpath(__file__)), "assets/audio.wav")

    # use the audio file as the audio source
    r = sr.Recognizer()
    with sr.AudioFile(AUDIO_FILE) as source:
        audio = r.record(source)  # read the entire audio file

    try:
        text = r.recognize_google(audio)
        print("Google thinks you said " + text)
        return text
    except sr.UnknownValueError:
        print("Google could not understand audio")
    except sr.RequestError as e:
        print("Google error; {0}".format(e))


def match(text, speech):
    return SequenceMatcher(None, text, speech)