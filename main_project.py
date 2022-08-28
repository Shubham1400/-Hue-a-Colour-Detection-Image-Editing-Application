from tkinter import *
import tkinter.messagebox
from tkinter import filedialog
from PIL import Image, ImageFilter, ImageTk, ImageEnhance
import os
import config  # module I created to use global variables across all modules
import local_module as lm  # self made module for image editing

root = Tk()

# setting main window size, title, icon and background colour
root.geometry('1360x720+80+50')
root.title("Hue")
root.iconbitmap(r'hue.ico')
root.configure(bg='#191919')

'''Global variables'''
image = ''
a = b = c = d = 0
panel = ''
instruction_label = ''


# creating menubar
menubar = Menu(root, bg='#000000', background='#404040', foreground='white', activebackground='#004c99',
               activeforeground='white')
root.config(menu=menubar)

'''displays the PIL images as PIL images is passed which is convertet to photoimage in the function
Also displays the original image'''


def display_image(imagecopy):
    imagecopy = ImageTk.PhotoImage(imagecopy)

    global panel
    panel = Label(imageframe, image=imagecopy)
    panel.imagecopy = imagecopy
    panel.place(anchor=NW, width=1160, height=600)


def browsefile():
    browser_image_address = filedialog.askopenfilename()  # open browsing window to select file
    statusbar['text'] = os.path.basename(browser_image_address)  # displays image name on the statusbar
    global image
    image = Image.open(browser_image_address)
    image = image.resize((1160, 600), Image.ANTIALIAS)

    imagecopy = image.copy()  # copying image to another image object

    display_image(imagecopy)


# creating submenu
submenu = Menu(menubar, bd=0, tearoff=0, background='#404040', foreground='white', activebackground='#004c99',
               activeforeground='white')
menubar.add_cascade(label='File', menu=submenu)
submenu.add_command(label='Open...', command=browsefile)
submenu.add_cascade(label='Save...')
submenu.add_command(label='Save as...')
submenu.add_separator()
submenu.add_command(label='Exit', command=root.destroy)


def aboutus():
    tkinter.messagebox.showinfo('My project', 'Hue: An image manipulation app from Shubham Prashant IT-B2. Subject '
                                              'Teacher: Dr. Sandeep Saxena')


submenu = Menu(menubar, bd=0, tearoff=0, background='#404040', foreground='white', activebackground='#004c99',
               activeforeground='white')
menubar.add_cascade(label='Help', menu=submenu)
submenu.add_command(label='About...', command=aboutus)

# adding statusbar
statusbar = Label(root, text='Hue', relief=GROOVE, background='#191919', foreground='#dec1bf', anchor=W)
statusbar.pack(fill=X, side=BOTTOM)

# creating a frame for displaying image and file select button
imageframe = Frame(root, bg='#202020', relief=SUNKEN, borderwidth=0.5)
imageframe.place(anchor=NW, width=1160, height=600)

# making the select image button
Label(imageframe, text='~~~~~~~~~~~~', background='#202020', foreground='#dec1bf').place(x=550, y=225)
browsephoto = PhotoImage(file='plus(2).png')
selectbutton = Button(imageframe, image=browsephoto, command=browsefile)
selectbutton.place(x=565, y=250)
Label(imageframe, text='~~~~~~~~~~~~\nBROWSE IMAGE', bg='#202020', foreground='#dec1bf').place(x=550, y=320)

# making option frame for image editing buttons
optionframe = Frame(root, background='#202020', relief=SUNKEN, borderwidth=0.5)
optionframe.place(x=1160, y=0, width=200, height=700)

# function to make frame and label for displaying instructions
def instruction_display(Text):

    instruction_label = Label(root, background = '#191919', foreground = 'white', text = Text).place(x=5, y=605)


'''Displays the photoimage as the photoimage converted image is received in the argument
also has button features which chooses if the changes in images are to be kept or discarded'''


def label_frame(edited_image):  # make a label frame which will display the image on the image frame
    panel1 = Label(imageframe, image=edited_image)
    panel1.edited_image = edited_image
    panel1.place(anchor=NW, width=1160, height=600)

    '''global flag_for_unbinding

    if flag_for_unbinding == 1:
        imageframe.unbind("<Button-1>", click_left_paste)
        

    if flag_for_unbinding == 2:
        imageframe.unbind("<Button-1>", mouse_click_left_resize)
        
        
    if flag_for_unbinding == 3:
        imageframe.unbind("<Button-1>", mouse_click_left_crop)
        imageframe.unbind("<Button-3>", mouse_click_right_crop)

    flag_for_unbinding = 0
    
The second argument to unbind is a 'funcid', not a function. help(root.unbind) returns
unbind(sequence, funcid=None) method of tkinter.Tk instance. Unbind for this widget for event SEQUENCE the function identified with FUNCID.
>>> i = root.bind('<Button-1>', int)
>>> i
'1733092354312int'
>>> root.unbind('<Button-1>', i)  # Specific binding removed.

Buried in the output from help(root.bind) is this: "Bind will return an identifier to allow deletion of the bound function with unbind without memory leak."'''

    def saved_changes():
        global image
        image = config.edited_image_copy
        display_image(image)

    keep_changes = Button(root, text='KEEP CHANGES', background='#191919', foreground='white', command=saved_changes)
    keep_changes.place(x=1060, y=610)

    def revert_changes():
        display_image(image)

    revert_changes = Button(root, text='REVERT', background='#191919', foreground='white', command=revert_changes)
    revert_changes.place(x=1082, y=636)

    def save_images():
        global image
        new_image = filedialog.asksaveasfile(defaultextension='.jpg',
                                             filetypes=[("jpg file", "*.jpg"),
                                                        ("png file", "*.png"), ("All files", "*.*")])
        if new_image:
            image.save(new_image)

    save_image = Button(optionframe, text='SAVE\nIMAGE', background='#191919', foreground='white', command=save_images)
    save_image.place(x=75, y=620)


def detect():
    os.system('python presentation.py')  # runs secondary module(or you can call script) from another module


# adding colour detector button
detectorphoto = PhotoImage(file='rgb.png')
detection = Button(optionframe, image=detectorphoto, command=lambda: os.system('python detector.py'))
detection.place(x=80, y=80)
Label(optionframe, text='FIND COLOUR', background='#202020', foreground='#dec1bf').place(x=59, y=117)


def colour_image(scale_value):
    global image
    coloured_image = ImageEnhance.Color(image)
    coloured_image_copy = coloured_image.enhance(float(scale_value) / 10)

    config.edited_image_copy = coloured_image_copy

    coloured_image_copy = ImageTk.PhotoImage(coloured_image_copy)
    label_frame(coloured_image_copy)


def colour_feature():
    instruction_display(config.colour_text)
    # scale bar widget
    Scale_bar = Scale(root, from_=0, to=100, orient=HORIZONTAL, foreground='white', background='#191919', troughcolor='#b4b4aa',
                      activebackground='black', highlightbackground='#191919', command=colour_image)
    Scale_bar.set(10)
    Scale_bar.place(x=790, y=600)


# adding feature buttons
colorphoto = PhotoImage(file='rotate.png')
color = Button(optionframe, image=colorphoto, command=colour_feature)
color.place(x=80, y=140)
Label(optionframe, text='COLOUR', background='#202020', foreground='#dec1bf').place(x=73, y=177)


def mouse_click_left_crop(event):  # gives upper left coordinate for cropping
    global a, b
    a = event.x
    b = event.y


def mouse_click_right_crop(event):  # gives lower right coordinate for cropping
    global a, b, c, d
    c = event.x
    d = event.y
    cropped_image = lm.crop_image(image, a, b, c, d)
    label_frame(cropped_image)


def crop_feature():
    instruction_display(config.crop_text)
    # creates mouse click events to find coordinates, 1 for left click and  for right click
    global panel
    panel.bind("<Button-1>", mouse_click_left_crop)
    panel.bind("<Button-3>", mouse_click_right_crop)
    global flag_for_unbinding
    flag_for_unbinding = 3


cropphoto = PhotoImage(file='crop.png')
crop = Button(optionframe, image=cropphoto, command=crop_feature)
crop.place(x=80, y=200)
Label(optionframe, text='CROP', background='#202020', foreground='#dec1bf').place(x=80, y=237)


def mouse_click_left_resize(event):
    global a, b
    a = event.x
    b = event.y
    resized_image = lm.resize_image(image, a, b, )
    label_frame(resized_image)


def resize_feature():
    instruction_display(config.resize_text)
    global panel
    panel.bind("<Button-1>", mouse_click_left_resize)
    global flag_for_unbinding
    flag_for_unbinding = 2


resizephoto = PhotoImage(file='resize.png')
resize = Button(optionframe, image=resizephoto, command=resize_feature)
resize.place(x=80, y=260)
Label(optionframe, text='RESIZE', background='#202020', foreground='#dec1bf').place(x=78, y=297)


def click_left_paste(event):  # give top left coordinate for pasting image
    a = event.x
    b = event.y
    pasted_image = lm.paste_image(image, a, b)
    label_frame(pasted_image)


def paste_feature():
    instruction_display(config.paste_text)
    global panel
    panel.bind("<Button-1>", click_left_paste)
    global flag_for_unbinding
    flag_for_unbinding = 1


pastephoto = PhotoImage(file='add.png')
paste = Button(optionframe, image=pastephoto, command=paste_feature)
paste.place(x=80, y=320)
Label(optionframe, text='ADD', background='#202020', foreground='#dec1bf').place(x=83, y=357)


def hori_flip():
    global image
    flipped = lm.Horizontal_mirror(image)
    label_frame(flipped)


def vert_flip():
    global image
    flipped = lm.Vertical_mirror(image)
    label_frame(flipped)


def mirror_feature():
    instruction_display(config.flip_text)
    horizontal_flip = Button(root, text='HORIZONTAL\nINVERT', background='#191919', foreground='white', command=hori_flip)
    horizontal_flip.place(x=900, y=600)

    vertical_flip = Button(root, text='VERTICAL\nINVERT', background='#191919', foreground='white', command=vert_flip)
    vertical_flip.place(x=980, y=600)


mirrorphoto = PhotoImage(file='different.png')
mirror = Button(optionframe, image=mirrorphoto, command=mirror_feature)
mirror.place(x=80, y=380)
Label(optionframe, text='MIRROR', background='#202020', foreground='#dec1bf').place(x=73, y=417)


def contrast_image(scale_value):
    global image
    contrasted_image = ImageEnhance.Contrast(image)
    contrasted_image_copy = contrasted_image.enhance(float(scale_value) / 10)

    config.edited_image_copy = contrasted_image_copy

    contrasted_image_copy = ImageTk.PhotoImage(contrasted_image_copy)
    label_frame(contrasted_image_copy)


def contrast_feature():
    instruction_display(config.contrast_text)
    
    # scale bar widget
    Scale_bar = Scale(root, from_=0, to=100, orient=HORIZONTAL, foreground='white', background='#191919', troughcolor='#b4b4aa',
                      activebackground='black', highlightbackground='#191919', command=contrast_image)
    Scale_bar.set(10)
    Scale_bar.place(x=790, y=600)


contrastphoto = PhotoImage(file='contrast.png')
contrast = Button(optionframe, image=contrastphoto, command=contrast_feature)
contrast.place(x=80, y=440)
Label(optionframe, text='CONTRAST', background='#202020', foreground='#dec1bf').place(x=65, y=477)


def blur_feature():
    instruction_display(config.blur_text)
    
    blurred_Image = lm.blur_image(image)
    label_frame(blurred_Image)  # calls the label function which displays the image of imageframe


blurphoto = PhotoImage(file='transparency.png')
blur = Button(optionframe, image=blurphoto, command=blur_feature)
blur.place(x=80, y=500)
Label(optionframe, text='BLUR', background='#202020', foreground='#dec1bf').place(x=82, y=537)

root.mainloop()
