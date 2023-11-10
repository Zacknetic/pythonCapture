import tkinter as tk
from PIL import ImageGrab
import numpy as np
from collections import Counter

# Function to get the dominant color
def get_dominant_color(x, y, width, height):
    # Capture a screen area
    screen = ImageGrab.grab(bbox=(x, y, x+width, y+height))
    # Convert the image to RGB
    screen = screen.convert('RGB')
    # Convert the image to a numpy array
    screen_array = np.array(screen)
    # Reshape the array to a list of RGB values
    rgb_array = screen_array.reshape((screen_array.shape[0]*screen_array.shape[1], 3))
    # Count the frequency of each color
    color_counts = Counter(map(tuple, rgb_array))
    # Get the most common color
    dominant_color = color_counts.most_common(1)[0][0]
    return dominant_color

# Function to update the color square in the GUI
def update_color_square():
    dominant_color = get_dominant_color(1000, 500, 100, 100)
    color_label.config(bg='#%02x%02x%02x' % dominant_color)
    # Schedule the `update_color_square` function to run every 1000 milliseconds
    root.after(20, update_color_square)

# Create a tkinter window
root = tk.Tk()
root.title("Dominant Color Display")

# Create a label to show the color
color_label = tk.Label(root, text='Dominant Color', font=('Helvetica', 32), width=20, height=10)
color_label.pack()

# Start the GUI loop and periodically update the color square
update_color_square()
root.mainloop()
