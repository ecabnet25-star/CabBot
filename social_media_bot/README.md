## Social Media Bot Desktop App

This is a cross-platform desktop app for scheduling and posting to X (Twitter), Reddit, and Telegram.

### Features
- Connect your X, Reddit, and Telegram accounts securely
- Compose posts and schedule them for future delivery
- Select subreddit/channel for each post
- View and delete scheduled posts
- Local SQLite storage (no cloud required)

### Setup
1. Install Python 3.8+
2. Install dependencies:
   ```
   pip install pyqt5 apscheduler requests tweepy praw requests-oauthlib
   ```
3. Set up Reddit API credentials as environment variables:
   - `REDDIT_CLIENT_ID`
   - `REDDIT_CLIENT_SECRET`
4. Run the app:
   ```
   python main.py
   ```

### Usage
1. Click "Connect" for each platform and follow the prompts.
2. Compose your post, select platforms, and schedule a time.
3. (Optional) Enter subreddit or Telegram channel.
4. View and manage scheduled posts in the app.

**Note:** You must leave the app running for scheduled posts to be delivered.