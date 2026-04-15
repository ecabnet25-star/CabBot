def post_to_facebook(text, token=None):
    import requests, json, os
    from PyQt5.QtWidgets import QMessageBox, QInputDialog
    token_path = os.path.join(os.path.dirname(__file__), "meta_token.json")
    if not os.path.exists(token_path):
        QMessageBox.warning(None, "Facebook Post", "Meta (Facebook/Instagram) not connected.")
        return
    with open(token_path, "r") as f:
        meta = json.load(f)
    access_token = meta.get("access_token")
    # Get Page ID
    resp = requests.get(f"https://graph.facebook.com/v19.0/me/accounts?access_token={access_token}")
    data = resp.json()
    if "data" not in data or not data["data"]:
        QMessageBox.critical(None, "Facebook Post", "No Facebook Pages found for this user.")
        return
    # Let user pick a page
    pages = data["data"]
    page_names = [p["name"] for p in pages]
    page_id = None
    if len(pages) == 1:
        page_id = pages[0]["id"]
        page_token = pages[0]["access_token"]
    else:
        idx, ok = QInputDialog.getItem(None, "Select Facebook Page", "Choose a Page:", page_names, 0, False)
        if not ok:
            return
        for p in pages:
            if p["name"] == idx:
                page_id = p["id"]
                page_token = p["access_token"]
                break
    if not page_id:
        QMessageBox.critical(None, "Facebook Post", "No Page selected.")
        return
    # Post to Page
    post_url = f"https://graph.facebook.com/v19.0/{page_id}/feed"
    resp = requests.post(post_url, data={"message": text, "access_token": page_token})
    if resp.status_code == 200:
        QMessageBox.information(None, "Facebook Post", "Posted to Facebook Page successfully!")
    else:
        QMessageBox.critical(None, "Facebook Post", f"Failed: {resp.text}")

def post_to_instagram(text, token=None):
    import requests, json, os
    from PyQt5.QtWidgets import QMessageBox, QInputDialog
    token_path = os.path.join(os.path.dirname(__file__), "meta_token.json")
    if not os.path.exists(token_path):
        QMessageBox.warning(None, "Instagram Post", "Meta (Facebook/Instagram) not connected.")
        return
    with open(token_path, "r") as f:
        meta = json.load(f)
    access_token = meta.get("access_token")
    # Get Facebook Pages
    resp = requests.get(f"https://graph.facebook.com/v19.0/me/accounts?access_token={access_token}")
    data = resp.json()
    if "data" not in data or not data["data"]:
        QMessageBox.critical(None, "Instagram Post", "No Facebook Pages found for this user.")
        return
    # Find Pages with connected Instagram Business accounts
    ig_pages = []
    for p in data["data"]:
        page_id = p["id"]
        page_token = p["access_token"]
        ig_resp = requests.get(f"https://graph.facebook.com/v19.0/{page_id}?fields=instagram_business_account&access_token={page_token}")
        ig_data = ig_resp.json()
        ig_id = ig_data.get("instagram_business_account", {}).get("id")
        if ig_id:
            ig_pages.append((p["name"], ig_id, page_token))
    if not ig_pages:
        QMessageBox.critical(None, "Instagram Post", "No Instagram Business accounts linked to your Pages.")
        return
    # Let user pick IG account
    ig_names = [n for n, _, _ in ig_pages]
    ig_idx, ok = QInputDialog.getItem(None, "Select Instagram Account", "Choose an Instagram Business Account:", ig_names, 0, False)
    if not ok:
        return
    for n, ig_id, page_token in ig_pages:
        if n == ig_idx:
            break
    # Instagram requires a media object (image/video) to post. We'll post a text image.
    # For now, just post a caption (requires a valid image_url for real use).
    # Prompt user for image URL
    image_url, ok = QInputDialog.getText(None, "Instagram Image URL", "Enter a public image URL to post:")
    if not ok or not image_url:
        QMessageBox.warning(None, "Instagram Post", "Image URL required for Instagram posts.")
        return
    # Create media object
    media_url = f"https://graph.facebook.com/v19.0/{ig_id}/media"
    media_resp = requests.post(media_url, data={"image_url": image_url, "caption": text, "access_token": page_token})
    media_data = media_resp.json()
    if "id" not in media_data:
        QMessageBox.critical(None, "Instagram Post", f"Failed to create media: {media_data}")
        return
    creation_id = media_data["id"]
    # Publish media
    publish_url = f"https://graph.facebook.com/v19.0/{ig_id}/media_publish"
    publish_resp = requests.post(publish_url, data={"creation_id": creation_id, "access_token": page_token})
    if publish_resp.status_code == 200:
        QMessageBox.information(None, "Instagram Post", "Posted to Instagram successfully!")
    else:
        QMessageBox.critical(None, "Instagram Post", f"Failed: {publish_resp.text}")
# poster.py
# Posting logic for each platform

from PyQt5.QtWidgets import QMessageBox

def post_to_x(text, token=None):
    token_path = os.path.join(os.path.dirname(__file__), "x_token.json")
    if not os.path.exists(token_path):
        print("[POST] X: Not connected.")
        QMessageBox.warning(None, "X Post", "X (Twitter) not connected.")
        return
    with open(token_path, "r") as f:
        data = json.load(f)
    api_key = data.get("api_key")
    api_secret = data.get("api_secret")
    access_token = data.get("access_token")
    access_token_secret = data.get("access_token_secret")
    if not api_key or not api_secret or not access_token or not access_token_secret:
        print("[POST] X: Missing credentials.")
        QMessageBox.warning(None, "X Post", "Missing X credentials.")
        return
    try:
        auth = tweepy.OAuth1UserHandler(api_key, api_secret, access_token, access_token_secret)
        api = tweepy.API(auth)
        api.update_status(status=text)
        print("[POST] X: Success!")
        QMessageBox.information(None, "X Post", "Posted to X successfully!")
    except Exception as e:
        print(f"[POST] X: Failed - {e}")
        QMessageBox.critical(None, "X Post", f"Failed to post to X: {e}")

import os
import json
import praw

def post_to_reddit(text, token=None):
    # Try to load refresh token from file
    token_path = os.path.join(os.path.dirname(__file__), "reddit_token.json")
    if not os.path.exists(token_path):
        print("[POST] Reddit: Not connected.")
        QMessageBox.warning(None, "Reddit Post", "Reddit not connected.")
        return
    with open(token_path, "r") as f:
        data = json.load(f)
    refresh_token = data.get("refresh_token")
    client_id = os.getenv("REDDIT_CLIENT_ID", "")
    client_secret = os.getenv("REDDIT_CLIENT_SECRET", "")
    user_agent = "SocialMediaBot/1.0 by DesktopApp"
    # Load subreddit preference
    prefs_path = os.path.join(os.path.dirname(__file__), "user_prefs.json")
    subreddit_name = "test"
    if os.path.exists(prefs_path):
        with open(prefs_path, "r") as pf:
            prefs = json.load(pf)
            subreddit_name = prefs.get("subreddit", "test")
    if not client_id or not client_secret or not refresh_token:
        print("[POST] Reddit: Missing credentials.")
        QMessageBox.warning(None, "Reddit Post", "Missing Reddit credentials.")
        return
    reddit = praw.Reddit(
        client_id=client_id,
        client_secret=client_secret,
        refresh_token=refresh_token,
        user_agent=user_agent
    )
    try:
        subreddit = reddit.subreddit(subreddit_name)
        subreddit.submit(title="Bot Post", selftext=text)
        print(f"[POST] Reddit: Success in r/{subreddit_name}!")
        QMessageBox.information(None, "Reddit Post", f"Posted to r/{subreddit_name} successfully!")
    except Exception as e:
        print(f"[POST] Reddit: Failed - {e}")
        QMessageBox.critical(None, "Reddit Post", f"Failed to post to Reddit: {e}")

import requests

def post_to_telegram(text, token=None):
    token_path = os.path.join(os.path.dirname(__file__), "telegram_token.json")
    if not os.path.exists(token_path):
        print("[POST] Telegram: Not connected.")
        QMessageBox.warning(None, "Telegram Post", "Telegram not connected.")
        return
    with open(token_path, "r") as f:
        data = json.load(f)
    bot_token = data.get("bot_token")
    chat_id = data.get("chat_id")
    # Load channel preference
    prefs_path = os.path.join(os.path.dirname(__file__), "user_prefs.json")
    if os.path.exists(prefs_path):
        with open(prefs_path, "r") as pf:
            prefs = json.load(pf)
            channel = prefs.get("channel")
            if channel:
                chat_id = channel
    if not bot_token or not chat_id:
        print("[POST] Telegram: Missing credentials.")
        QMessageBox.warning(None, "Telegram Post", "Missing Telegram credentials.")
        return
    url = f"https://api.telegram.org/bot{bot_token}/sendMessage"
    payload = {"chat_id": chat_id, "text": text, "parse_mode": "Markdown"}
    try:
        resp = requests.post(url, json=payload)
        if resp.status_code == 200:
            print(f"[POST] Telegram: Success to {chat_id}!")
            QMessageBox.information(None, "Telegram Post", f"Posted to Telegram {chat_id} successfully!")
        else:
            print(f"[POST] Telegram: Failed - {resp.text}")
            QMessageBox.critical(None, "Telegram Post", f"Failed to post to Telegram: {resp.text}")
    except Exception as e:
        print(f"[POST] Telegram: Exception - {e}")
        QMessageBox.critical(None, "Telegram Post", f"Exception posting to Telegram: {e}")

def post_to_platforms(text, platforms, tokens=None):
    if tokens is None:
        tokens = {}
    if "x" in platforms:
        post_to_x(text, tokens.get("x"))
    if "reddit" in platforms:
        post_to_reddit(text, tokens.get("reddit"))
    if "telegram" in platforms:
        post_to_telegram(text, tokens.get("telegram"))
    if "instagram" in platforms:
        post_to_instagram(text, tokens.get("instagram"))
    if "facebook" in platforms:
        post_to_facebook(text, tokens.get("facebook"))
