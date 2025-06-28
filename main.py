import tkinter as gui
from tkinter import filedialog
from pytubefix import YouTube
from youtube_search import YoutubeSearch
videos_list = []

class Video():
  def __init__(self,id,title,channel):
    self.id = id
    self.title = title
    self.channel = channel


def clear_scren():
  pass
def download_video(id):
  path = filedialog.askdirectory()
  filename = YouTube(f"https://www.youtube.com/watch?v={id}").streams.first().title
  YouTube(f"https://www.youtube.com/watch?v={id}").streams.first().download(output_path=path,filename=f"{filename}.mp3")
def show_video(video):
  title = gui.Label(window,text=video.title)
  channel = gui.Label(window,text=video.channel)
  download = gui.Button(window,text="Download",command=lambda:download_video(str(video.id)))
  title.pack()
  channel.pack()
  download.pack(side="bottom")
def search_videos(input):
  results = YoutubeSearch(input, max_results=10).to_dict()
  for videos in results:
    current_video = Video(videos["id"],videos["title"],videos["channel"])
    videos_list.append(current_video)
  for video in videos_list:
    show_video(video)

window = gui.Tk()
window.title("Amapaiano")
window.geometry("300x400")
logo_image = gui.PhotoImage(file="logo.png")
logo = gui.Label(image=logo_image)
search = gui.Entry(window)
sumbit = gui.Button(window,text="Search",command=lambda:search_videos(str(search.get())))
logo.pack()
search.pack()
sumbit.pack()
window.mainloop()