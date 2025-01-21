import yt_dlp

def download_video(urls: list):
    options = {
        'format': 'best',
        'outtmppl': '%(title)s.%(ext)s'
    }

    with yt_dlp.YoutubeDL(options) as ydl:
        ydl.download(urls)

download_video([
    "https://www.youtube.com/watch?v=NhY6EhnjqGY&list=PLoVRMnw7TPbC_CnFmag1jbLQbbh555Y0X&index=2"
])