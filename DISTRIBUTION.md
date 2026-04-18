# How to Distribute Your App

1. Upload the file `dist/main.exe` to a file hosting service (Google Drive, Dropbox, OneDrive, or GitHub Releases).
2. Share the download link with your users.
3. Users can download and run `main.exe` directly—no Python installation required.

## Optional: Create a Windows Installer
For a more professional experience (Start Menu shortcut, uninstall, etc.), use a tool like Inno Setup or NSIS to wrap `main.exe` in an installer. Let me know if you want this step!

---

**Note:** If your app needs to write files, recommend users run it from a folder where they have write permissions (not `C:\Program Files`).