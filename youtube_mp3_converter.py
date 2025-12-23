import tkinter as tk
from tkinter import ttk, messagebox
import os
import yt_dlp
import threading

# --- Ensure Python can find ffmpeg in the current folder ---
os.environ["PATH"] += os.pathsep + os.getcwd()

# --- Download function ---
def download_mp3():
    url = url_entry.get().strip()
    if not url:
        messagebox.showwarning("Input Error", "Please enter a YouTube URL")
        return

    os.makedirs("downloads", exist_ok=True)

    # Progress hook for yt_dlp
    def progress_hook(d):
        if d['status'] == 'downloading':
            total_bytes = d.get('total_bytes') or d.get('total_bytes_estimate')
            downloaded_bytes = d.get('downloaded_bytes', 0)
            if total_bytes:
                percent = downloaded_bytes / total_bytes * 100
                progress_var.set(percent)
                root.update_idletasks()
        elif d['status'] == 'finished':
            progress_var.set(100)
            root.update_idletasks()

    ydl_opts = {
        'format': 'bestaudio/best',
        'outtmpl': 'downloads/%(title)s.%(ext)s',
        'postprocessors': [{
            'key': 'FFmpegExtractAudio',
            'preferredcodec': 'mp3',
            'preferredquality': '192',
        }],
        'progress_hooks': [progress_hook],
        'quiet': True,
    }

    def run_download():
        try:
            with yt_dlp.YoutubeDL(ydl_opts) as ydl:
                ydl.download([url])
            messagebox.showinfo("Success", "MP3 downloaded in the 'downloads' folder!")
            progress_var.set(0)
        except Exception as e:
            messagebox.showerror("Error", f"Download failed:\n{e}")
            progress_var.set(0)

    # Run download in a separate thread to avoid freezing the GUI
    threading.Thread(target=run_download, daemon=True).start()

# --- GUI ---
root = tk.Tk()
root.title("YouTube MP3 Downloader")
root.geometry("400x150")
root.resizable(False, False)

tk.Label(root, text="YouTube URL:").pack(pady=(10, 0))
url_entry = tk.Entry(root, width=50)
url_entry.pack(pady=(0, 10))
url_entry.focus()

download_btn = tk.Button(root, text="Download MP3", command=download_mp3, width=20)
download_btn.pack(pady=(0, 10))

# Progress bar
progress_var = tk.DoubleVar()
progress_bar = ttk.Progressbar(root, variable=progress_var, maximum=100)
progress_bar.pack(fill='x', padx=20, pady=(0, 10))

root.mainloop()
