import os
import sys
from PyQt5.QtWidgets import QApplication, QWidget, QVBoxLayout, QLabel, QLineEdit, QPushButton, QTextEdit
from PyQt5.QtCore import QThread, pyqtSignal
from pytube import Playlist, YouTube

class DownloadThread(QThread):
    progress_update = pyqtSignal(str)

    def __init__(self, playlist_url, parent=None):
        super().__init__(parent)
        self.playlist_url = playlist_url
        self.running = True
        self.paused = False

    def run(self):
        pl = Playlist(self.playlist_url)
        playlist_title = pl.title
        folder_name = f"Videos/{playlist_title}"
        os.makedirs(folder_name, exist_ok=True)

        i = 0
        for video_url in pl.video_urls:
            if not self.running:
                break
            i += 1
            yt = YouTube(video_url)
            video = yt.streams.filter(progressive=True, file_extension="mp4").order_by("resolution").desc().first()
            if video:
                video_title = f"{i:02d} - {yt.title}.mp4"  # Add '.mp4' extension
                video_title = video_title.replace('/', '_')
                self.progress_update.emit(f"Downloading video {i}: '{yt.title}'...")
                video.download(folder_name, filename=video_title)
                self.progress_update.emit(f"Video {i}: '{yt.title}' downloaded successfully in the highest resolution available: {video.resolution}")
            else:
                self.progress_update.emit(f"Video {i}: '{yt.title}' could not be downloaded")
            while self.paused:
                if not self.running:
                    break
                self.sleep(1)

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
        self.setWindowTitle("YouTube Playlist Downloader")
        layout = QVBoxLayout()

        self.url_label = QLabel("Playlist URL:")
        self.url_input = QLineEdit()
        layout.addWidget(self.url_label)
        layout.addWidget(self.url_input)

        self.download_button = QPushButton("Download")
        self.download_button.clicked.connect(self.start_download)
        layout.addWidget(self.download_button)

        self.pause_button = QPushButton("Pause")
        self.pause_button.clicked.connect(self.pause_download)
        self.pause_button.setEnabled(False)
        layout.addWidget(self.pause_button)

        self.resume_button = QPushButton("Resume")
        self.resume_button.clicked.connect(self.resume_download)
        self.resume_button.setEnabled(False)
        layout.addWidget(self.resume_button)

        self.log_output = QTextEdit()
        layout.addWidget(self.log_output)

        self.setLayout(layout)

    def start_download(self):
        playlist_url = self.url_input.text().strip()
        if playlist_url:
            self.log_output.clear()
            self.download_thread = DownloadThread(playlist_url)
            self.download_thread.progress_update.connect(self.update_progress)
            self.download_thread.start()
            self.download_button.setEnabled(False)
            self.pause_button.setEnabled(True)
        else:
            self.log_output.append("Please enter a playlist URL.")

    def pause_download(self):
        if hasattr(self, 'download_thread'):
            self.download_thread.pause()
            self.pause_button.setEnabled(False)
            self.resume_button.setEnabled(True)

    def resume_download(self):
        if hasattr(self, 'download_thread'):
            self.download_thread.resume()
            self.resume_button.setEnabled(False)
            self.pause_button.setEnabled(True)

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
