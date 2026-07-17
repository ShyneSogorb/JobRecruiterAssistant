DATA = """
YouTube Downloader
A tool to download YouTube videos.

Downloads any public video via link
Downloads all public videos from a public playlist
"""

def load():
    code: str
    with open("C:\\Users\\user\\Documents\\MyProjects\\YT_Downloader\\MusicDownloader.py") as f:
        code = f.read()
    return f"""
{DATA}

Code: \n{code}

"""