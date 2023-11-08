import numpy as np
from PIL import Image
from tkinter import Tk, Canvas
from tkinter import filedialog

window = Tk()
window.withdraw()

file = filedialog.askopenfilename(filetypes=[("Images", "*.jpg;*.jpeg;*.png")])

image = Image.open(file)

image_array = np.array(image)


def unique_count(a):
    colors, count = np.unique(a.reshape(-1, a.shape[-1]), axis=0, return_counts=True)
    sorted_colors = sorted(zip(colors, count), key=lambda x: x[1], reverse=True)
    return sorted_colors[:10]


list_of_colors = unique_count(image_array)
rgb_list = []
for color in list_of_colors:
    rgb_list.append(tuple(color[0][:3]))

root = Tk()
root.title("Color Grid")

canvas = Canvas(root, width=500, height=500)
canvas.pack()

size = 100

def get_luminance(hex_color):
    # Convert the hex color to RGB values
    r = int(hex_color[1:3], 16)
    g = int(hex_color[3:5], 16)
    b = int(hex_color[5:7], 16)
    # Calculate the luminance using the formula
    r = r / 255 if r <= 0.03928 else ((r / 255 + 0.055) / 1.055) ** 2.4
    g = g / 255 if g <= 0.03928 else ((g / 255 + 0.055) / 1.055) ** 2.4
    b = b / 255 if b <= 0.03928 else ((b / 255 + 0.055) / 1.055) ** 2.4
    luminance = 0.2126 * r + 0.7152 * g + 0.0722 * b
    # Return the luminance value
    return luminance * 255

def contrast_color(hex_color):
    # Get the luminance of the hex color
    luminance = get_luminance(hex_color=hex_color)
    # Return white or black depending on the luminance
    if luminance < 140:
        return "#FFFFFF"
    else:
        return "#000000"
    

for i, color in enumerate(rgb_list):
    hex_color = "#%02x%02x%02x" % color
    row = i // 5
    col = i % 5
    text_color = contrast_color(hex_color)
    x1 = col * size
    y1 = row * size
    x2 = x1 + size
    y2 = y1 + size
    canvas.create_rectangle(x1,y1,x2,y2,fill=hex_color, outline=hex_color)
    canvas.create_text((x1 + x2) / 2, (y1 + y2) / 2, text=hex_color, anchor='center',fill=text_color)


root.mainloop()