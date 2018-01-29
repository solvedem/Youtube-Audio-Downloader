# solvedem

from Tkinter import *
import pafy
import urllib
import urllib2
from bs4 import BeautifulSoup

# BOARD SETUP ---------------------------------------------------------------------------------------------------

root = Tk()
root.title("Audio Downloader")

Label(root, text="url/search").grid(row=0)
Label(root, text="save as").grid(row=1)
inputbox1 = Entry()
inputbox2 = Entry()
inputbox1.grid(row=0, column=1)
inputbox2.grid(row=1, column=1)
variable = StringVar(root)
variable.set("mp3") 
w = OptionMenu(root, variable, *["mp3","m4a",".wav"])
w.grid(row=0, column = 2)

left_col = ["Status","Title","Likes","Dislikes","Duration","Bitrate"]
j = 0
for i in range(4, 10):
    Label(root, text=left_col[j]).grid(row=i)
    j += 1

status_label, title_label,likes_label = (Label(root, text=""),Label(root, text=""),Label(root, text=""))
dislikes_label,duration_label,bitrate_label = (Label(root, text=""),Label(root, text=""),Label(root, text=""))
labels = [status_label, title_label, likes_label, dislikes_label, duration_label, bitrate_label]
r = 4
for label in labels:
    label.grid(row=r, column=1)
    r += 1

# HELPER FUNCTIONS ---------------------------------------------------------------------------------------------------

def get_url(qu):
    query = urllib.quote(qu)
    url = "https://www.youtube.com/results?search_query=" + query
    response = urllib2.urlopen(url)
    html = response.read()
    soup = BeautifulSoup(html, "lxml")
    vid = soup.findAll(attrs={'class':'yt-uix-tile-link'})[0]
    return 'https://www.youtube.com' + vid['href']

def clear_labels(labels):
    for label in labels:
        label["text"] = ""

def clear_entries(entries):
    for entry in entries:
        entry.delete(0,END)

def convert_and_download(url, title, extension, root):
    status_label["text"] = "Converting..."
    root.update()
    try:
        video = pafy.new(url)
    except:
        video = pafy.new(get_url(url))
    title_label["text"] = video.title[0:20]
    likes_label["text"] = video.likes
    dislikes_label["text"] = video.dislikes
    duration_label["text"] = video.duration
    bestaudio = video.getbestaudio()
    bitrate_label["text"] = bestaudio.bitrate
    if title == "":
        title = video.title[0:10]
    status_label["text"] = "Downloading..."
    root.update()
    bestaudio.download(quiet=True, filepath=str(title + "." + extension))

def click():
    status_label["text"] = ""
    url = inputbox1.get()
    title = inputbox2.get()
    extension = variable.get()
    clear_labels(labels)
    try:
        convert_and_download(url, title, extension, root)
        status_label["text"] = "Success"
        clear_entries([inputbox1,inputbox2])
    except:
        status_label["text"] = "Error"
        clear_entries([inputbox1,inputbox2])

# MAIN LOOP ---------------------------------------------------------------------------------------------------

Button(text="Download",command=click).grid(row=2, column=1)
root.mainloop()


