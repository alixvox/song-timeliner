import argparse
import youtube_dl
from mutagen import File
from mutagen.id3 import ID3NoHeaderError
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
    album = audio.get('album', ['Unknown'])[0]

    return artist, title, date, album

def organize_songs_into_albums(artist_data):
    for artist, title, _, album in artist_data:
        source_path = os.path.join(artist, f'{title}.mp3')
        album = album if album and album != 'Unknown' else title
        album_path = os.path.join(artist, album)

        if not os.path.exists(album_path):
            os.makedirs(album_path)

        if os.path.exists(source_path):
            os.rename(source_path, os.path.join(album_path, f'{title}.mp3'))

def create_csv(artist_data, filename):
    with open(filename, 'w', newline='', encoding='utf-8') as file:
        writer = csv.writer(file)
        writer.writerow(['Artist', 'Title', 'Release Date', 'Album'])
        for data in artist_data:
            writer.writerow(data)

def main():
    parser = argparse.ArgumentParser(description='Download and timeline songs.')
    parser.add_argument('artists', nargs='*', help='List of artist IDs (optional)')
    parser.add_argument('-d', '--download', action='store_true', help='Download new content for artists')
    parser.add_argument('-f', '--folder', action='store_true', help='Organize songs into album folders')
    args = parser.parse_args()

    # If no artist IDs are provided, process all existing directories
    if not args.artists:
        args.artists = [d for d in os.listdir('.') if os.path.isdir(d)]

    ydl_opts = {
        'format': 'bestaudio/best',
        'postprocessors': [
            {
                'key': 'FFmpegExtractAudio',
                'preferredcodec': 'mp3',
                'preferredquality': '192',
            },
            {
                'key': 'FFmpegMetadata',
            },
        ],
        'addmetadata': True
    }

    artist_data = []

    for artist_id in args.artists:
        artist_dir = os.path.join(os.getcwd(), artist_id)

        # Determine if the artist is from YouTube or SoundCloud
        if artist_id.startswith('UC'):
            artist_url = f'https://www.youtube.com/channel/{artist_id}'
        else:
            artist_url = f'https://soundcloud.com/{artist_id}'

        # Download only if -d flag is used
        if args.download:
            if not os.path.exists(artist_dir):
                os.makedirs(artist_dir)
            download_audio(artist_url, artist_id, ydl_opts)

        # Process each file in the artist's directory
        for file in os.listdir(artist_dir):
            if file.endswith('.mp3'):
                file_path = os.path.join(artist_dir, file)
                metadata = extract_metadata(file_path)
                if metadata:
                    artist_data.append([artist_id, metadata[1], metadata[2], metadata[3]])
                else:
                    artist_data.append([artist_id, os.path.splitext(file)[0], '', ''])

    # Organize songs into folders based on album name
    if args.folder:
        organize_songs_into_albums(artist_data)

    # Create CSV file
    csv_filename = f"stl-{'-'.join(args.artists)}.csv"
    create_csv(artist_data, csv_filename)

if __name__ == "__main__":
    main()
