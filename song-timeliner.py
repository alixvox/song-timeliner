import argparse
import youtube_dl
from mutagen import File
import os
import csv

def download_audio(url, artist, ydl_opts):
    ydl_opts['outtmpl'] = f'{artist}/%(title)s.%(ext)s'
    with youtube_dl.YoutubeDL(ydl_opts) as ydl:
        ydl.download([url])

def extract_metadata(file_path):
    audio = File(file_path, easy=True)
    
    if audio is None or not audio.tags:
        print(f"No metadata found in {file_path}")
        return None

    title = audio.get('title', [os.path.basename(file_path).split('.')[0]])[0]
    artist = audio.get('artist', ['Unknown'])[0]
    date = audio.get('date', [''])[0]

    return artist, title, date

def create_csv(artist_data, filename):
    with open(filename, 'w', newline='', encoding='utf-8') as file:
        writer = csv.writer(file)
        writer.writerow(['Artist', 'Title', 'Release Date'])
        for data in artist_data:
            writer.writerow(data)

def convert_args_to_urls(arguments):
    artist_urls = {}
    bc_albums = {}
    processing_bc = False
    current_bc_artist = None

    for arg in arguments:
        if arg == 'bc':
            processing_bc = True
        elif arg == 'cb':
            processing_bc = False
            current_bc_artist = None
        elif processing_bc:
            if current_bc_artist is None:
                current_bc_artist = arg
            else:
                bc_albums.setdefault(current_bc_artist, []).append(f'https://{current_bc_artist}.bandcamp.com/album/{arg}')
        else:
            artist_id = arg
            if artist_id.startswith('UC'):
                artist_urls[artist_id] = f'https://www.youtube.com/channel/{artist_id}'
            else:
                artist_urls[artist_id] = f'https://soundcloud.com/{artist_id}'

    return artist_urls, bc_albums

def main():
    parser = argparse.ArgumentParser(description='Download and timeline songs.')
    parser.add_argument('args', nargs=argparse.REMAINDER, help='List of artist IDs and Bandcamp albums')
    parser.add_argument('-d', '--download', action='store_true', help='Download new content for artists')
    args = parser.parse_args()

    # Convert arguments to URLs
    artist_urls, bc_album_urls = convert_args_to_urls(args.args)

    ydl_opts = {
        'format': 'bestaudio/best',
        'postprocessors': [{
            'key': 'FFmpegExtractAudio',
            'preferredcodec': 'mp3',
            'preferredquality': '192',
        }, {
            'key': 'FFmpegMetadata',
        }],
        'addmetadata': True
    }

    artist_data = []

    # Download and process artists
    if args.download:
        for artist_id, url in artist_urls.items():
            artist_dir = os.path.join(os.getcwd(), artist_id)
            if not os.path.exists(artist_dir):
                os.makedirs(artist_dir)
            download_audio(url, artist_id, ydl_opts)

        # Process Bandcamp albums
        for artist_id, albums in bc_album_urls.items():
            artist_dir = os.path.join(os.getcwd(), 'bc-' + artist_id)
            if not os.path.exists(artist_dir):
                os.makedirs(artist_dir)
            for album_url in albums:
                download_audio(album_url, 'bc-' + artist_id, ydl_opts)

    # Process each file in the artist's directory
    for artist_id in os.listdir('.'):
        if os.path.isdir(artist_id):
            artist_dir = os.path.join(os.getcwd(), artist_id)
            for file in os.listdir(artist_dir):
                if file.endswith('.mp3'):
                    file_path = os.path.join(artist_dir, file)
                    metadata = extract_metadata(file_path)
                    if metadata:
                        artist_data.append([artist_id, metadata[1], metadata[2]])
                    else:
                        artist_data.append([artist_id, os.path.splitext(file)[0], ''])

    # Get a list of artist directories
    artist_dirs = [d for d in os.listdir('.') if os.path.isdir(d) and not d.startswith('.')]
    
    # Check if there are any artist directories
    if not artist_dirs:
        print("Error: No artist folders found in the directory.")
        return

    # Create CSV file
    csv_filename = f"stl-{'-'.join(artist_dirs)}.csv"
    create_csv(artist_data, csv_filename)

if __name__ == "__main__":
    main()
