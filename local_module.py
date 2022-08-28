from PIL import Image, ImageFilter, ImageTk
from tkinter import filedialog
import config


def blur_image(image):
    blurred_image = image.filter(ImageFilter.BLUR)
    config.edited_image_copy = blurred_image
    blurred_image = ImageTk.PhotoImage(blurred_image)
    return blurred_image

    # panel1 = Label(imageframe, image = blurImage)
    # panel1.blurImage = blurImage
    '''above statement is important since we are creating a new image inside
a function, with it's own local namespace. when the function ends the reference to
the image, it will be garbage collected. So, we are saving a refernce to the image in
the label widget. without this statement, blank label will be displayed'''

    # panel1.place(anchor=NW, width=1160, height=600)


def Horizontal_mirror(image):
    flipped = image.transpose(Image.FLIP_LEFT_RIGHT)

    config.edited_image_copy = flipped

    flipped = ImageTk.PhotoImage(flipped)
    return flipped


def Vertical_mirror(image):
    flipped = image.transpose(Image.FLIP_TOP_BOTTOM)

    config.edited_image_copy = flipped

    flipped = ImageTk.PhotoImage(flipped)
    return flipped


def crop_image(image, a, b, c, d):
    cropped_image = image.crop((a, b, c, d))

    config.edited_image_copy = cropped_image

    cropped_image = ImageTk.PhotoImage(cropped_image)
    return cropped_image


def paste_image(main_image, a, b):
    image_to_paste = Image.open(filedialog.askopenfilename())
    main_image.paste(image_to_paste, (a, b))

    config.edited_image_copy = main_image

    main_image = ImageTk.PhotoImage(main_image)
    return main_image


def resize_image(image, a, b):
    resized_image = image.resize((a, b))

    config.edited_image_copy = resized_image

    resized_image = ImageTk.PhotoImage(resized_image)
    return resized_image
