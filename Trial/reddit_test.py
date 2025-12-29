import requests,os
url = input("Enter reddit video url : ")[:-1]+".json"
r = requests.get(url,headers={"User-agent":"Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/139.0.0.0 Safari/537.36"})
data = r.json()[0]
video_url = data["data"]['children'][0]['data']['secure_media']['reddit_video']['fallback_url']
audio_url = "https://v.redd.it/"+video_url.split("/")[3]+"/DASH_AUDIO_128.mp4"
print(video_url)
print(audio_url)
with open("video.mp4","wb") as f:
    g = requests.get(video_url,stream=True)
    f.write(g.content)