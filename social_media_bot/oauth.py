import os
# Instagram and Facebook stubs
import requests
import time

META_TOKEN_PATH = os.path.join(os.path.dirname(__file__), "meta_token.json")

def connect_facebook():
    from PyQt5.QtWidgets import QInputDialog, QMessageBox
    app_id, ok1 = QInputDialog.getText(None, "Meta App ID", "Enter your Meta App ID:")
    if not ok1 or not app_id:
        return
    app_secret, ok2 = QInputDialog.getText(None, "Meta App Secret", "Enter your Meta App Secret:")
    if not ok2 or not app_secret:
        return
    redirect_uri = "https://localhost/"
    oauth_url = (
        f"https://www.facebook.com/v19.0/dialog/oauth?client_id={app_id}"
        f"&redirect_uri={redirect_uri}&scope=pages_manage_posts,pages_read_engagement,pages_show_list,instagram_basic,instagram_content_publish,pages_read_user_content,publish_to_groups&response_type=code"
    )
    import webbrowser
    webbrowser.open(oauth_url)
    code, ok3 = QInputDialog.getText(None, "Meta OAuth Code", "Paste the code from the redirected URL:")
    if not ok3 or not code:
        return
    # Exchange code for access token
    token_url = (
        f"https://graph.facebook.com/v19.0/oauth/access_token?client_id={app_id}"
        f"&redirect_uri={redirect_uri}&client_secret={app_secret}&code={code}"
    )
    try:
        resp = requests.get(token_url)
        data = resp.json()
        if "access_token" in data:
            with open(META_TOKEN_PATH, "w") as f:
                json.dump({"access_token": data["access_token"], "app_id": app_id, "app_secret": app_secret}, f)
            QMessageBox.information(None, "Meta OAuth", "Facebook/Instagram account connected!")
        else:
            QMessageBox.critical(None, "Meta OAuth", f"Failed: {data}")
    except Exception as e:
        QMessageBox.critical(None, "Meta OAuth", f"Exception: {e}")

def connect_instagram():
    connect_facebook()  # Same flow, same token
# oauth.py
# Placeholder for OAuth logic for X, Reddit, and Telegram
# In a desktop app, OAuth flows typically open a browser window for user authentication
# and receive the callback via a local server or manual code entry.

# For now, this file will contain stubs for connect functions.

import tweepy

X_TOKEN_PATH = os.path.join(os.path.dirname(__file__), "x_token.json")

def connect_x():
    api_key, ok1 = QInputDialog.getText(None, "X API Key", "Enter your X (Twitter) API Key:")
    if not ok1 or not api_key:
        return
    api_secret, ok2 = QInputDialog.getText(None, "X API Secret", "Enter your X (Twitter) API Secret:")
    if not ok2 or not api_secret:
        return
    auth = tweepy.OAuth1UserHandler(api_key, api_secret)
    try:
        auth_url = auth.get_authorization_url()
        import webbrowser
        webbrowser.open(auth_url)
        pin, ok3 = QInputDialog.getText(None, "X PIN", "Enter the PIN from the browser:")
        if not ok3 or not pin:
            return
        auth.get_access_token(pin)
        with open(X_TOKEN_PATH, "w") as f:
            json.dump({
                "api_key": api_key,
                "api_secret": api_secret,
                "access_token": auth.access_token,
                "access_token_secret": auth.access_token_secret
            }, f)
        QMessageBox.information(None, "X (Twitter)", "X account connected!")
    except Exception as e:
        QMessageBox.critical(None, "X (Twitter)", f"Failed: {e}")

import praw
import os
import json
from PyQt5.QtWidgets import QMessageBox

REDDIT_CLIENT_ID = os.getenv("REDDIT_CLIENT_ID", "")
REDDIT_CLIENT_SECRET = os.getenv("REDDIT_CLIENT_SECRET", "")
REDDIT_USER_AGENT = "SocialMediaBot/1.0 by DesktopApp"
TOKEN_PATH = os.path.join(os.path.dirname(__file__), "reddit_token.json")

def connect_reddit():
    if not REDDIT_CLIENT_ID or not REDDIT_CLIENT_SECRET:
        QMessageBox.warning(None, "Reddit OAuth", "Set REDDIT_CLIENT_ID and REDDIT_CLIENT_SECRET as environment variables.")
        return
    reddit = praw.Reddit(
        client_id=REDDIT_CLIENT_ID,
        client_secret=REDDIT_CLIENT_SECRET,
        redirect_uri="http://localhost:8080",
        user_agent=REDDIT_USER_AGENT
    )
    scopes = ["submit", "identity"]
    auth_url = reddit.auth.url(scopes, "...", "permanent")
    import webbrowser
    webbrowser.open(auth_url)
    code, ok = _prompt_for_code()
    if not ok:
        return
    try:
        refresh_token = reddit.auth.authorize(code)
        with open(TOKEN_PATH, "w") as f:
            json.dump({"refresh_token": refresh_token}, f)
        QMessageBox.information(None, "Reddit OAuth", "Reddit account connected!")
    except Exception as e:
        QMessageBox.critical(None, "Reddit OAuth", f"Failed: {e}")

def _prompt_for_code():
    from PyQt5.QtWidgets import QInputDialog
    code, ok = QInputDialog.getText(None, "Reddit OAuth", "Paste the code from the redirected URL:")
    return code, ok

from PyQt5.QtWidgets import QInputDialog, QMessageBox

TELEGRAM_TOKEN_PATH = os.path.join(os.path.dirname(__file__), "telegram_token.json")

def connect_telegram():
    token, ok1 = QInputDialog.getText(None, "Telegram Bot Token", "Enter your Telegram bot token:")
    if not ok1 or not token:
        return
    chat_id, ok2 = QInputDialog.getText(None, "Telegram Chat ID", "Enter your chat ID (e.g. @mychannel or -100123456):")
    if not ok2 or not chat_id:
        return
    with open(TELEGRAM_TOKEN_PATH, "w") as f:
        json.dump({"bot_token": token, "chat_id": chat_id}, f)
    QMessageBox.information(None, "Telegram", "Telegram bot connected!")
