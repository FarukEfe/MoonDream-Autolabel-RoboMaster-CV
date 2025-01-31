import yt_dlp, argparse, os

def download_video(urls: list, output: str):
    # Download Information
    options = {
        'format': 'best',
        'outtmppl': output+'/%(title)s.%(ext)s'
    }

    # Run Download Script
    with yt_dlp.YoutubeDL(options) as ydl:
        n = len(urls)
        for i, url in enumerate(urls):
            try:
                ydl.download([url])
                print(f'Downloaded file {i} out of {n}.', end='\r')
            except:
                print(f'Failed to download: {url}. Ignoring...', end='\r')
        print('',end='\n') # Resetting \r suffix

# Sample RoboMaster Video: https://www.youtube.com/watch?v=NhY6EhnjqGY&list=PLoVRMnw7TPbC_CnFmag1jbLQbbh555Y0X&index=2
if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='YT Downloader')
    # Add flags & parse arguments
    parser.add_argument('-o','--output', type=str, help='Output file directory')
    parser.add_argument('-u', '--url', type=str, nargs='*', help='Manual entry for video url(s)')
    #parser.add_argument('-f', '--file', type=str, nargs='?', help='File directory listing downloads (has to be txt for simplicity)')
    args = parser.parse_args()
    # Handle output path
    output_dir = os.path.abspath(args.output)
    if not os.path.exists(output_dir):
        print("Output folder directory couldn't be found, exiting...", end='\r')
        exit(1)
    # Download URLs
    download_video(args.urls, output_dir)