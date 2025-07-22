# ffmpeg -i "[link]"-c:v libx264 -preset ultrafast -crf [1-30 (its for quality, 1 is the best quality] [create video name with].mp4

# :: for example ffmpeg -i https://example.site/720p.m3u8 -c:v libx264 -preset ultrafast -crf 1 720p-film.mp4



import requests
import subprocess


input_url = 'link here'
output_file = 'output.mp4'

# Spoof user agent to avoid HTTP 403 Forbidden
headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko)Chrome/91.0.4472.124 Safari/537.36','Referer': 'https://developer.mozilla.org/en-US/docs/Web/JavaScript'  }

# Download HLS playlist with spoofed user agent
response = requests.get(input_url)

if response.status_code == 200:
    # Use FFmpeg to process HLS playlist and create MP4 output
    ffmpeg_command = f'ffmpeg -protocol_whitelist file,http,https,tcp,tls,crypto -i {input_url} -c copy {output_file}'
    subprocess.run(ffmpeg_command, shell=True)
else:
    print(f"Failed to retrieve the playlist. Status code: {response.status_code}")