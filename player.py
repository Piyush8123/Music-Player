from tkinter import *
from PIL import ImageTk,Image
from tkinter import filedialog
import pygame
import time
from mutagen.mp3 import MP3
import tkinter.ttk as ttk

root = Tk()
root.title("Music Player")
root.geometry("700x450")

# Initialize Pygame
pygame.mixer.init()



# Create function for one song
def add_song():
    song = filedialog.askopenfilename(initialdir='C:/Users/sanju/Music/my music', title="Choose A Song", filetypes=(("mp3 Files", "*.mp3"),))
    # Strip out directory structure and .mp3 from song title
    song = song.replace("C:/Users/sanju/Music/my music/", "")
    song = song.replace(".mp3", "")
    # Add To End of Playlist
    player_box.insert(END, song)

# Create function for one song
def multi_song():
    songs = filedialog.askopenfilenames(initialdir='C:/Users/sanju/Music/my music', title="Choose A Song", filetypes=(("mp3 Files", "*.mp3"),))

    # Loop thru song list and replace directory structure and mp3 from song name
    for song in songs:
        # Strip out directory structure and .mp3 from song title
        song = song.replace("C:/Users/sanju/Music/my music/", "")
        song = song.replace(".mp3", "")
        # Add To End of Playlist
        player_box.insert(END, song)

# Create delete function
def delete():
    player_box.delete(ANCHOR)

# Create del_all function
def del_all():
    player_box.delete(0,END)

# Create previous function
def previous():
    # Reset slider position and status bar
    status.config(text='')
    song_slider.config(value=0)

    # Get current no.
    prev = player_box.curselection()
    # Get no. - 1 for backward
    prev = prev[0] - 1

    prev_song = player_box.get(prev)
    prev_song = 'C:/Users/sanju/Music/my music/{}.mp3'.format(prev_song)

    pygame.mixer.music.load(prev_song)
    pygame.mixer.music.play(loops=0)

    # Clear the selection
    player_box.selection_clear(0, END)
    # Create active to previous song
    player_box.activate(prev)
    # Set selection to active song
    player_box.selection_set(prev, last=None)


# Create next function
def next():
    # Reset slider position and status bar
    status.config(text = '')
    song_slider.config(value = 0)

    # Get current no.
    nxt = player_box.curselection()
    # Get no. + 1 for forward
    nxt = nxt[0] + 1

    nxt_song = player_box.get(nxt)
    nxt_song = 'C:/Users/sanju/Music/my music/{}.mp3'.format(nxt_song)

    pygame.mixer.music.load(nxt_song)
    pygame.mixer.music.play(loops=0)

    # Clear the selection
    player_box.selection_clear(0,END)
    # Create active to next song
    player_box.activate(nxt)
    # Set selection to active song
    player_box.selection_set(nxt,last=None)

# Create function to get time
def song_time():
    if stopped:
        return

    # Grab Current Song Time
    current_time = pygame.mixer.music.get_pos() / 1000
    # Convert Song Time To Time Format
    converter = time.strftime('%M:%S',time.gmtime(current_time))


    active = player_box.get(ACTIVE)
    active = 'C:/Users/sanju/Music/my music/{}.mp3'.format(active)

    # Get the song length
    len = MP3(active)
    song_length = len.info.length
    hour = time.strftime('%M:%S',time.gmtime(song_length))

    # Created for autoplay
    if v.get() == "Autoplay":
        if int(song_slider.get()) == int(song_length):
            next()

    # Check if song is over
    if int(song_slider.get()) == int(song_length):
        stop()


    elif paused:
        # Check to see if paused, if so - pass
        pass
    else:
        # Move slider according to play time
        acc_time = int(song_slider.get()) + 1
        song_slider.config(to = song_length,value  = acc_time)
        # Convert slider position to time format
        converter = time.strftime('%M:%S', time.gmtime(int(song_slider.get())))
        status.config(text='Time Passed : {} of {}'.format(converter, hour))

    if current_time >= 1:
        status.config(text='Time Passed : {} of {}'.format(converter,hour))

    status.after(1000, song_time)

# Create play function
def play():
    global  stopped
    stopped = False
    # Song with directory structure.
    active = player_box.get(ACTIVE)
    active = 'C:/Users/sanju/Music/my music/{}.mp3'.format(active)
    # Load song
    pygame.mixer.music.load(active)
    # Play Song
    pygame.mixer.music.play(loops = 0)
    # Get the song time
    song_time()

# Create stopped variable
global stopped
stopped = False

# Create stop function

def stop():
    # Stop the song
    pygame.mixer.music.stop()
    # Clear Playlist Bar
    player_box.selection_clear(ACTIVE)

    status.config(text='')

    # Set our slider to zero
    song_slider.config(value=0)

    # Set Stop Variable To True
    global stopped
    stopped = True

# Create paused variable
global paused
paused = False
# Create pause function
def pause(is_paused):
    global paused
    paused = is_paused

    if paused:
        # Unpause
        pygame.mixer.music.unpause()
        paused = False
    else:
        #Pause
        pygame.mixer.music.pause()
        paused = True

# Create vol function
def vol(x):
    pygame.mixer.music.set_volume(volumn_slider.get())

# Create slide function
def slide(x):
    # Song with directory structure.
    active = player_box.get(ACTIVE)
    active = 'C:/Users/sanju/Music/my music/{}.mp3'.format(active)
    # Load song
    pygame.mixer.music.load(active)
    # Play Song
    pygame.mixer.music.play(loops=0,start = song_slider.get())


# Create main frame
main = Frame(root)
main.pack(pady =20)

# Create playlist box
player_box = Listbox(main,bg = "black",fg = "green",width = 60,selectbackground = "green",selectforeground = "black")
player_box.grid(row = 0,column = 0)

# Create volumn slider frame
volumn = LabelFrame(main,text = "Volume")
volumn.grid(row = 0,column = 1)

# Create volumn slider
volumn_slider = ttk.Scale(volumn,from_ = 0,to = 1,value = 1,orient = VERTICAL,length = 125,command = vol)
volumn_slider.pack(pady = 10)

# Create song slider
song_slider = ttk.Scale(main,from_ = 0,to = 100,value = 0,orient = HORIZONTAL,length = 360,command = slide)
song_slider.grid(row = 2,column = 0)

# Create autoplay button
v = StringVar()
auto_btn = Checkbutton(main,text = "Autoplay",variable = v,onvalue = "Autoplay")
auto_btn.deselect()
auto_btn.grid(row = 2,column = 1)


# Define images to button
back_img = ImageTk.PhotoImage(Image.open('images/back.png'))
forward_img = ImageTk.PhotoImage(Image.open('images/forward.png'))
play_img = ImageTk.PhotoImage(Image.open('images/play.png'))
pause_img = ImageTk.PhotoImage(Image.open('images/pause.png'))
stop_img =ImageTk.PhotoImage(Image.open('images/stop.png'))

# Create menu to add songs
add_menu = Menu(root)
root.config(menu = add_menu)
var = Menu(add_menu,tearoff = 0)
add_menu.add_cascade(label = "Songs",menu = var)
var.add_command(label = "Add one song to playlist",command = add_song)
var.add_command(label = "Add many songs to playlist",command = multi_song)

# Create delete menu to delete songs
del_song = Menu(add_menu,tearoff = 0)
add_menu.add_cascade(label = "Remove Songs",menu = del_song)
del_song.add_command(label = "Delete a song",command = delete)
del_song.add_command(label = "Delete all songs",command = del_all)


# Create button frame
control = Frame(main)
control.grid(row = 1,column = 0,pady = 20)

# Create Buttons like Play,Stop,etc..
back = Button(control,image = back_img,width = 60,height = 95,borderwidth = 0,command = previous)
forward = Button(control,image = forward_img,width = 60,height = 25,borderwidth = 0,command = next)
play = Button(control,image = play_img,width = 60,height = 60,borderwidth = 0,command = play)
pause_btn = Button(control, image=pause_img, borderwidth=0, command=lambda: pause(paused))
stop_btn = Button(control,image = stop_img,width = 60,height = 60,borderwidth = 0,command = stop)

back.grid(row=0,column=0,padx = 10)
forward.grid(row=0,column=1,padx = 10)
play.grid(row=0,column=2,padx = 10)
pause_btn.grid(row=0, column=3, padx=10)
stop_btn.grid(row=0,column=4,padx = 10)

# Create status bar
status = Label(root,text = "Status Bar",bd = 1,relief = GROOVE,anchor = E)
status.pack(fill = X,side = BOTTOM,ipady = 2)

# Label To represent song name and location
song_name = Label(root)
song_name.pack(pady=20)


root.mainloop()