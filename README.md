# Song Timeliner

## Overview

Song Timeliner is a Python application designed to create timelines of multiple artists' discographies. It organizes songs based on their metadata, including release dates, and compiles this information into a CSV file. The application can process existing song files in the directory or download new content from YouTube(untested) and SoundCloud to retrieve accurate metadata.

## Prerequisites

Before you begin, ensure you have the following installed on your system:

1.  Python 3
2.  `ffmpeg` or `ffprobe` for handling media files

## Installation

### Step 1: Clone the Repository

Clone the `song-timeliner` repository to your local machine:

```bash
git clone https://github.com/yourusername/song-timeliner.git
cd song-timeliner
```

### Step 2: Install Python dependencies

Install the required Python packages:

```bash
pip install -r requirements.txt
```

## Usage (Methods)

### Method 1: Processing Existing Songs

If you already have your songs with metadata downloaded, you can run this app without any arguments to process folders within the directory. Once you've dropped the artists' folders into the root directory, run the command by itself:

```bash
python3 song-timeliner.py
```

This command will process all artist folders present in the root directory of the project.

### Method 2: Downloading and Processing New Songs

To download and process songs for specific artists, you can use either SoundCloud usernames or YouTube channel IDs:

- **For SoundCloud**: Use the username from the SoundCloud artist's URL. For example, for `https://soundcloud.com/postmalone`, use `postmalone`.
- **For YouTube**: Use the channel ID from the YouTube channel's URL. This is typically a string that starts with 'UC'. For example, for `https://www.youtube.com/channel/UCwZEU0wAwIyZb4x5G_KJp2w`, use `UCwZEU0wAwIyZb4x5G_KJp2w`.

Run the script with the `-d` flag (or `--download`) followed by the artist identifiers:

```bash
python3 song-timeliner.py -d [username/ID] [another username/ID]
## For example:
python3 song-timeliner.py -d postmalone UCwZEU0wAwIyZb4x5G_KJp2w
```

This command will download all content for these artists into folders by artist and album. (if their folders don't already exist) and process their songs.

## Contributing

Contributions to Song Timeliner are welcome! Please ensure to follow the project's code style and add unit tests for any new features.

## License

\[chosen license\]

## Contact

For any queries or contributions, please contact me at j.alex.leeper@gmail.com!

J. Alex Leeper

&nbsp;