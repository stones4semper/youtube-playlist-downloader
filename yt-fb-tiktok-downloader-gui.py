import os
import sys
from PyQt5.QtWidgets import QApplication, QWidget, QVBoxLayout, QLabel, QLineEdit, QPushButton, QTextEdit, QRadioButton
from PyQt5.QtCore import QThread, pyqtSignal
from pytube import Playlist, YouTube
from facebook_scraper import get_video_urls
from TikTokApi import TikTokApi

class DownloadThread(QThread):
    progress_update = pyqtSignal(str)

    def __init__(self, url, platform, parent=None):
        super().__init__(parent)
        self.url = url
        self.platform = platform
        self.running = True
        self.paused = False

    def run(self):
        try:
            if self.platform == "YouTube":
                self.download_youtube_video(self.url)
            elif self.platform == "Facebook":
                self.download_facebook_video(self.url)
            elif self.platform == "TikTok":
                self.download_tiktok_video(self.url)
            else:
                self.progress_update.emit("Invalid platform selected.")
        except Exception as e:
            self.progress_update.emit(f"An error occurred: {str(e)}")

    def download_youtube_video(self, url):
        yt = YouTube(url)
        video = yt.streams.filter(progressive=True, file_extension="mp4").order_by("resolution").desc().first()
        if video:
            video_title = f"{yt.title}.mp4"
            video_title = "".join(c if c.isalnum() or c in [' ', '_', '-'] else '_' for c in video_title)
            self.progress_update.emit(f"Downloading YouTube video: '{yt.title}'...")
            video.download("Videos", filename=video_title)
            self.progress_update.emit(f"YouTube video '{yt.title}' downloaded successfully in the highest resolution available: {video.resolution}")
        else:
            self.progress_update.emit(f"YouTube video '{yt.title}' could not be downloaded")

    def download_facebook_video(self, url):
        video_urls = get_video_urls(url)
        if video_urls:
            video_url = video_urls[0]  # Assuming the first URL is the video URL
            # Download the video using appropriate methods
            self.progress_update.emit("Downloading Facebook video...")
            # Add code to download video from Facebook
        else:
            self.progress_update.emit("No video found on the provided Facebook URL.")

    def download_tiktok_video(self, url):
        api = TikTokApi()
        video = api.get_video_by_url(url)
        if video:
            video_url = video['itemInfo']['itemStruct']['video']['playAddr']
            # Download the video using appropriate methods
            self.progress_update.emit("Downloading TikTok video...")
            # Add code to download video from TikTok
        else:
            self.progress_update.emit("Failed to fetch TikTok video.")

    def stop(self):
        self.running = False

    def pause(self):
        self.paused = True

    def resume(self):
        self.paused = False

class MainWindow(QWidget):
    def __init__(self):
        super().__init__()
        self.init_ui()

    def init_ui(self):
        self.setWindowTitle("Video Downloader")
        layout = QVBoxLayout()

        self.url_label = QLabel("URL:")
        self.url_input = QLineEdit()
        layout.addWidget(self.url_label)
        layout.addWidget(self.url_input)

        self.platform_label = QLabel("Select Platform:")
        layout.addWidget(self.platform_label)

        self.youtube_radio = QRadioButton("YouTube")
        self.facebook_radio = QRadioButton("Facebook")
        self.tiktok_radio = QRadioButton("TikTok")

        self.youtube_radio.setChecked(True)

        layout.addWidget(self.youtube_radio)
        layout.addWidget(self.facebook_radio)
        layout.addWidget(self.tiktok_radio)

        self.download_button = QPushButton("Download")
        self.download_button.clicked.connect(self.start_download)
        layout.addWidget(self.download_button)

        self.stop_button = QPushButton("Stop")
        self.stop_button.clicked.connect(self.stop_download)
        self.stop_button.setEnabled(False)  # Disable initially
        layout.addWidget(self.stop_button)

        self.log_output = QTextEdit()
        layout.addWidget(self.log_output)

        self.setLayout(layout)

    def start_download(self):
        url = self.url_input.text().strip()
        if url:
            self.log_output.clear()
            platform = self.get_selected_platform()
            self.download_thread = DownloadThread(url, platform)
            self.download_thread.progress_update.connect(self.update_progress)
            self.download_thread.start()
            self.download_button.setEnabled(False)
            self.stop_button.setEnabled(True)  # Enable stop button
        else:
            self.log_output.append("Please enter a URL.")

    def stop_download(self):
        if hasattr(self, 'download_thread'):
            self.download_thread.stop()
            self.download_button.setEnabled(True)
            self.stop_button.setEnabled(False)

    def get_selected_platform(self):
        if self.youtube_radio.isChecked():
            return "YouTube"
        elif self.facebook_radio.isChecked():
            return "Facebook"
        elif self.tiktok_radio.isChecked():
            return "TikTok"

    def update_progress(self, message):
        self.log_output.append(message)

    def closeEvent(self, event):
        if hasattr(self, 'download_thread'):
            self.download_thread.stop()
        event.accept()

if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = MainWindow()
    window.show()
    sys.exit(app.exec_())
