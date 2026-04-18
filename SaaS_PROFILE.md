# SaaS Profile: Social Media Bot

## What does the SaaS do?
- Schedules posts for future delivery across X (Twitter), Reddit, Telegram, Facebook, and Instagram.
- Allows users to compose posts, select platforms, and pick subreddit/channel/page.
- Delivers posts automatically at the scheduled time (app must be running).
- Connects directly to each platform's API for posting (OAuth required).
- Stores scheduled posts locally in SQLite (no cloud backend).
- For Instagram, requires a public image URL for posting.
- Does not generate captions or auto-post from a product feed by default (manual entry only).

## What is it built in?
- Python 3.8+
- PyQt5 for GUI
- APScheduler for scheduling
- Tweepy, PRAW, requests, requests-oauthlib for platform APIs

## How does it connect to social platforms?
- Direct API integration: Authenticates and posts directly to X, Reddit, Telegram, Facebook, and Instagram using their APIs.
- No manual copy-paste: Once connected, posts are delivered automatically.

## Web Browser Version
To make this app accessible in a web browser, it must be rewritten as a web application (Flask/Django backend, React/Vue/HTML frontend, etc.).
