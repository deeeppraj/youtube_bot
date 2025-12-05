from youtube_transcript_api import YouTubeTranscriptApi
transcript = YouTubeTranscriptApi()

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
