
import tkinter as gui
from tkinter import filedialog, messagebox, ttk
from pytubefix import YouTube
from youtube_search import YoutubeSearch
import threading

videos_list = []

class Video():
    def __init__(self, id, title, channel):
        self.id = id
        self.title = title
        self.channel = channel

def clear_results():
    for widget in results_frame.winfo_children():
        widget.destroy()
    videos_list.clear()

def download_video(id, title):
    try:
        path = filedialog.askdirectory()
        if path:
            progress_window = gui.Toplevel(window)
            progress_window.title("Downloading...")
            progress_window.geometry("300x100")
            progress_window.resizable(False, False)
            
            progress_label = gui.Label(progress_window, text="Downloading video...")
            progress_label.pack(pady=20)
            
            progress_bar = ttk.Progressbar(progress_window, mode='indeterminate')
            progress_bar.pack(pady=10)
            progress_bar.start()
            
            def download_thread():
                try:
                    yt = YouTube(f"https://www.youtube.com/watch?v={id}")
                    stream = yt.streams.filter(only_audio=True).first()
                    stream.download(output_path=path, filename=f"{title}.mp3")
                    progress_window.destroy()
                    messagebox.showinfo("Success", f"Downloaded: {title}")
                except Exception as e:
                    progress_window.destroy()
                    messagebox.showerror("Error", f"Download failed: {str(e)}")
            
            threading.Thread(target=download_thread, daemon=True).start()
    except Exception as e:
        messagebox.showerror("Error", f"Download failed: {str(e)}")

def show_video(video, row):
    video_frame = gui.Frame(results_frame, bg="#f0f0f0", relief="ridge", bd=1)
    video_frame.grid(row=row, column=0, sticky="ew", padx=5, pady=2)
    video_frame.grid_columnconfigure(0, weight=1)
  
    title_label = gui.Label(video_frame, text=video.title, font=("Arial", 10, "bold"), 
                           bg="#f0f0f0", wraplength=400, justify="left")
    title_label.grid(row=0, column=0, sticky="w", padx=10, pady=(5, 0))
    
    channel_label = gui.Label(video_frame, text=f"by {video.channel}", font=("Arial", 8), 
                             fg="gray", bg="#f0f0f0")
    channel_label.grid(row=1, column=0, sticky="w", padx=10, pady=(0, 5))
    
    download_btn = gui.Button(video_frame, text="Download MP3", 
                             command=lambda: download_video(video.id, video.title),
                             bg="#4CAF50", fg="white", font=("Arial", 8, "bold"),
                             relief="flat", padx=15, pady=5)
    download_btn.grid(row=0, column=1, rowspan=2, padx=10, pady=5, sticky="e")

def search_videos():
    query = search_entry.get().strip()
    if not query:
        messagebox.showwarning("Warning", "Please enter a search term")
        return
    
    clear_results()
    
    loading_label = gui.Label(results_frame, text="Searching...", font=("Arial", 12))
    loading_label.grid(row=0, column=0, pady=20)
    
    def search_thread():
        try:
            results = YoutubeSearch(query, max_results=10).to_dict()
            
            loading_label.destroy()
            
            if not results:
                no_results = gui.Label(results_frame, text="No results found", font=("Arial", 12))
                no_results.grid(row=0, column=0, pady=20)
                return
            
            for i, video_data in enumerate(results):
                current_video = Video(video_data["id"], video_data["title"], video_data["channel"])
                videos_list.append(current_video)
                show_video(current_video, i)
                
        except Exception as e:
            loading_label.destroy()
            error_label = gui.Label(results_frame, text=f"Search failed: {str(e)}", 
                                   font=("Arial", 10), fg="red")
            error_label.grid(row=0, column=0, pady=20)
    
    threading.Thread(target=search_thread, daemon=True).start()

window = gui.Tk()
window.title("Amapiano YouTube Downloader")
window.geometry("600x700")
window.configure(bg="#ffffff")
window.resizable(True, True)

header_frame = gui.Frame(window, bg="#2196F3", height=80)
header_frame.pack(fill="x", padx=0, pady=0)
header_frame.pack_propagate(False)

try:
    logo_image = gui.PhotoImage(file="logo.png")
    logo_image = logo_image.subsample(2, 2)
    logo_label = gui.Label(header_frame, image=logo_image, bg="#2196F3")
    logo_label.pack(side="left", padx=20, pady=10)
except:
    pass

title_label = gui.Label(header_frame, text="Amapiano Downloader", 
                       font=("Arial", 18, "bold"), fg="white", bg="#2196F3")
title_label.pack(side="left", padx=10, pady=20)

search_frame = gui.Frame(window, bg="#ffffff", pady=20)
search_frame.pack(fill="x", padx=20)

search_label = gui.Label(search_frame, text="Search for music:", 
                        font=("Arial", 12), bg="#ffffff")
search_label.pack(anchor="w", pady=(0, 5))

input_frame = gui.Frame(search_frame, bg="#ffffff")
input_frame.pack(fill="x")

search_entry = gui.Entry(input_frame, font=("Arial", 12), relief="solid", bd=1)
search_entry.pack(side="left", fill="x", expand=True, ipady=8)
search_entry.bind("<Return>", lambda e: search_videos())

search_btn = gui.Button(input_frame, text="Search", command=search_videos,
                       bg="#2196F3", fg="white", font=("Arial", 12, "bold"),
                       relief="flat", padx=20, pady=8)
search_btn.pack(side="right", padx=(10, 0))

clear_btn = gui.Button(input_frame, text="Clear", command=clear_results,
                      bg="#f44336", fg="white", font=("Arial", 12, "bold"),
                      relief="flat", padx=20, pady=8)
clear_btn.pack(side="right", padx=(5, 0))

canvas_frame = gui.Frame(window, bg="#ffffff")
canvas_frame.pack(fill="both", expand=True, padx=20, pady=(0, 20))

canvas = gui.Canvas(canvas_frame, bg="#ffffff")
scrollbar = ttk.Scrollbar(canvas_frame, orient="vertical", command=canvas.yview)
results_frame = gui.Frame(canvas, bg="#ffffff")

results_frame.bind(
    "<Configure>",
    lambda e: canvas.configure(scrollregion=canvas.bbox("all"))
)

canvas.create_window((0, 0), window=results_frame, anchor="nw")
canvas.configure(yscrollcommand=scrollbar.set)

canvas.pack(side="left", fill="both", expand=True)
scrollbar.pack(side="right", fill="y")

results_frame.grid_columnconfigure(0, weight=1)

def on_mousewheel(event):
    canvas.yview_scroll(int(-1*(event.delta/120)), "units")

canvas.bind_all("<MouseWheel>", on_mousewheel)

status_frame = gui.Frame(window, bg="#f0f0f0", height=30)
status_frame.pack(fill="x", side="bottom")
status_frame.pack_propagate(False)

status_label = gui.Label(status_frame, text="Ready to search", 
                        font=("Arial", 9), bg="#f0f0f0", fg="gray")
status_label.pack(side="left", padx=10, pady=5)

window.mainloop()
