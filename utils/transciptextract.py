from youtube_transcript_api import YouTubeTranscriptApi
from youtube_transcript_api.proxies import WebshareProxyConfig
import os
transcript = YouTubeTranscriptApi(
    proxy_config=WebshareProxyConfig(
        proxy_username=os.getenv("WEBSHARE_USER"),
        proxy_password=os.getenv("WEBSHARE_PASS")
    )
)

def load_language(id):
    a = transcript.list(video_id=id)
    b = []
    for item in a :
        x = item.language_code
        b.append(x)
    return b

def load_data(id,lang):
    content = transcript.fetch(video_id=id,languages=[lang]).to_raw_data()
    a = []
    for  item in content:
        a.append(item['text'])

    text = "".join(a)
    return text
