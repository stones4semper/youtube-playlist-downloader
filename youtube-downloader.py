import os
from pytube import Playlist, YouTube

def show_progress(stream, chunk, file_handle, bytes_remaining):
    current = ((stream.filesize - bytes_remaining) / stream.filesize)
    percent = ('{0:.1f}').format(current * 100)
    print(f"\rDownloading... {percent}% complete", end='', flush=True)

playlist_url = input("Please enter the playlist URL: ")
pl = Playlist(playlist_url)
playlist_title = pl.title

folder_name = f"Videos/{playlist_title}"
os.makedirs(folder_name, exist_ok=True)

i = 0

for video_url in pl.video_urls:
    i += 1
    yt = YouTube(video_url)
    video = yt.streams.filter(progressive=True, file_extension="mp4").order_by("resolution").desc().first()
    if video:
        video_title = f"{i:02d} - {yt.title}"
        video_title = video_title.replace('/', '_')
        video.register_on_progress_callback(show_progress)
        video.download(folder_name, filename=video_title)
        print(f"\nVideo {i}: '{yt.title}' downloaded successfully in the highest resolution available: {video.resolution}")
    else:
        print(f"Video {i}: '{yt.title}' could not be downloaded")

print("All videos downloaded successfully")
