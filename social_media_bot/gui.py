import sys
from PyQt5.QtWidgets import (
    QApplication, QWidget, QVBoxLayout, QPushButton, QTextEdit, QCheckBox, QLabel, QDateTimeEdit, QHBoxLayout
)
from PyQt5.QtCore import QDateTime
from scheduler import schedule_post
from oauth import connect_x, connect_reddit, connect_telegram

class SocialMediaBotApp(QWidget):
            # Delete scheduled post button
            self.delete_btn = QPushButton("Delete Selected Post")
            self.delete_btn.clicked.connect(self.delete_selected_post)
            layout.addWidget(self.delete_btn)
            def delete_selected_post(self):
                selected = self.scheduled_list.currentRow()
                if selected < 0:
                    return
                from database import delete_scheduled_post_by_index, get_scheduled_posts
                posts = get_scheduled_posts()
                if selected < len(posts):
                    delete_scheduled_post_by_index(posts[selected][0])
                    self.refresh_scheduled_posts()
        # Scheduled posts display
        layout.addWidget(QLabel("Scheduled Posts:"))
        from PyQt5.QtWidgets import QListWidget
        self.scheduled_list = QListWidget()
        layout.addWidget(self.scheduled_list)
        self.refresh_scheduled_posts()
        def refresh_scheduled_posts(self):
            from database import get_scheduled_posts
            self.scheduled_list.clear()
            for post in get_scheduled_posts():
                text = post[1][:40] + ("..." if len(post[1]) > 40 else "")
                self.scheduled_list.addItem(f"{post[3]} | {post[2]} | {text}")
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Social Media Bot")
        self.setGeometry(100, 100, 400, 350)
        self.init_ui()

    def init_ui(self):
        layout = QVBoxLayout()

        # Connection status labels
        from os.path import exists, dirname, join
        self.x_status = QLabel()
        self.reddit_status = QLabel()
        self.telegram_status = QLabel()
        self.update_status_labels()

        # Connect buttons
        self.connect_x_btn = QPushButton("Connect X (Twitter)")
        self.connect_x_btn.clicked.connect(self.handle_connect_x)
        self.connect_reddit_btn = QPushButton("Connect Reddit")
        self.connect_reddit_btn.clicked.connect(self.handle_connect_reddit)
        self.connect_telegram_btn = QPushButton("Connect Telegram")
        self.connect_telegram_btn.clicked.connect(self.handle_connect_telegram)
        layout.addWidget(self.connect_x_btn)
        layout.addWidget(self.x_status)
        layout.addWidget(self.connect_reddit_btn)
        layout.addWidget(self.reddit_status)
        layout.addWidget(self.connect_telegram_btn)
        layout.addWidget(self.telegram_status)
    def update_status_labels(self):
        from os.path import exists, dirname, join
                    # Instagram and Facebook
                    self.connect_instagram_btn = QPushButton("Connect Instagram")
                    self.connect_instagram_btn.clicked.connect(self.handle_connect_instagram)
                    self.connect_facebook_btn = QPushButton("Connect Facebook")
                    self.connect_facebook_btn.clicked.connect(self.handle_connect_facebook)
                    self.instagram_status = QLabel()
                    self.facebook_status = QLabel()
                    layout.addWidget(self.connect_instagram_btn)
                    layout.addWidget(self.instagram_status)
                    layout.addWidget(self.connect_facebook_btn)
                    layout.addWidget(self.facebook_status)
        base = dirname(__file__)
        self.x_status.setText("Connected" if exists(join(base, "x_token.json")) else "Not connected")
        self.reddit_status.setText("Connected" if exists(join(base, "reddit_token.json")) else "Not connected")
        self.telegram_status.setText("Connected" if exists(join(base, "telegram_token.json")) else "Not connected")

    def handle_connect_x(self):
        connect_x()
        self.update_status_labels()
                    self.instagram_status.setText("Connected" if exists(join(base, "instagram_token.json")) else "Not connected")
                    self.facebook_status.setText("Connected" if exists(join(base, "facebook_token.json")) else "Not connected")

    def handle_connect_reddit(self):
        connect_reddit()
        self.update_status_labels()

    def handle_connect_telegram(self):
        connect_telegram()
        self.update_status_labels()


        # Post composer
        layout.addWidget(QLabel("Compose your post:"))
    
                def handle_connect_instagram(self):
                    from oauth import connect_instagram
                    connect_instagram()
                    self.update_status_labels()

                def handle_connect_facebook(self):
                    from oauth import connect_facebook
                    connect_facebook()
                    self.update_status_labels()
        self.post_text = QTextEdit()
        layout.addWidget(self.post_text)

        # Platform checkboxes and selectors
        self.x_cb = QCheckBox("Post to X")
        self.reddit_cb = QCheckBox("Post to Reddit")
        self.telegram_cb = QCheckBox("Post to Telegram")
        cb_layout = QHBoxLayout()
        cb_layout.addWidget(self.x_cb)
        cb_layout.addWidget(self.reddit_cb)
                    self.instagram_cb = QCheckBox("Post to Instagram")
                    self.facebook_cb = QCheckBox("Post to Facebook")
        cb_layout.addWidget(self.telegram_cb)
        layout.addLayout(cb_layout)

        # Subreddit/channel selectors
                    cb_layout.addWidget(self.instagram_cb)
                    cb_layout.addWidget(self.facebook_cb)
        self.subreddit_input = QTextEdit()
        self.subreddit_input.setPlaceholderText("Subreddit (e.g. test)")
        self.subreddit_input.setMaximumHeight(30)
        layout.addWidget(self.subreddit_input)
        self.channel_input = QTextEdit()
        self.channel_input.setPlaceholderText("Telegram channel/chat ID (optional)")
        self.channel_input.setMaximumHeight(30)
        layout.addWidget(self.channel_input)

        # Schedule picker
        layout.addWidget(QLabel("Schedule time:"))
        self.datetime_picker = QDateTimeEdit(QDateTime.currentDateTime())
        self.datetime_picker.setCalendarPopup(True)
        layout.addWidget(self.datetime_picker)

        # Schedule button
        self.schedule_btn = QPushButton("Schedule Post")
        self.schedule_btn.clicked.connect(self.handle_schedule)
        layout.addWidget(self.schedule_btn)

        # Status label
        self.status_label = QLabel("")
        layout.addWidget(self.status_label)

        self.setLayout(layout)

    def handle_schedule(self):
        text = self.post_text.toPlainText().strip()
        platforms = []
        if self.x_cb.isChecked():
            platforms.append("x")
        if self.reddit_cb.isChecked():
            platforms.append("reddit")
        if self.telegram_cb.isChecked():
            platforms.append("telegram")
        subreddit = self.subreddit_input.toPlainText().strip() or "test"
        channel = self.channel_input.toPlainText().strip()
        dt = self.datetime_picker.dateTime().toPyDateTime()
                    if self.instagram_cb.isChecked():
                        platforms.append("instagram")
                    if self.facebook_cb.isChecked():
                        platforms.append("facebook")
        from datetime import datetime
        if not text or not platforms:
            self.status_label.setText("Please enter text and select at least one platform.")
            return
        if dt <= datetime.now():
            self.status_label.setText("Scheduled time must be in the future.")
            return
        if self.x_cb.isChecked() and len(text) > 280:
            self.status_label.setText("X posts must be 280 characters or less.")
            return
        # Save subreddit/channel preferences
        import json, os
        prefs = {"subreddit": subreddit, "channel": channel}
        with open(os.path.join(os.path.dirname(__file__), "user_prefs.json"), "w") as f:
            json.dump(prefs, f)
        schedule_post(text, platforms, dt)
        self.status_label.setText(f"Post scheduled for {dt.strftime('%Y-%m-%d %H:%M:%S')}")
        self.refresh_scheduled_posts()

    @staticmethod
    def run():
        app = QApplication(sys.argv)
        window = SocialMediaBotApp()
        window.show()
        sys.exit(app.exec_())
