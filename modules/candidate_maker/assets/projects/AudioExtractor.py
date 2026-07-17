DATA ="""
Audio Extractor
A Python tool to extract audio from video.

Converts MP4 video into MP3 audio
Works on a single file or an entire folder of videos
Uses multithreading to process files much faster
"""

def load():
    code: str
    with open("C:\\Users\\user\\Documents\\MyProjects\\VideoAudio\\audioConversor.py") as f:
        code = f.read()
    return f"""
{DATA}

Code: \n{code}

"""