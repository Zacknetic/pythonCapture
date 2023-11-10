import tkinter as tk
from PIL import ImageGrab
import numpy as np
import colorsys
from collections import Counter

# Function to ensure the value (brightness) of the color is above a certain threshold
def ensure_minimum_brightness(rgb, min_brightness=0.1):
    # Convert RGB to HSV
    hsv = colorsys.rgb_to_hsv(rgb[0]/255, rgb[1]/255, rgb[2]/255)
    # Check if the value is below the threshold
    if hsv[2] < min_brightness:
        hsv = (hsv[0], hsv[1], min_brightness)
    # Convert back to RGB
    return tuple(int(c * 255) for c in colorsys.hsv_to_rgb(*hsv))

# Function to get the dominant color
def get_dominant_color():
    # Get user input values
    x = int(entry_x.get())
    y = int(entry_y.get())
    width = int(entry_width.get())
    height = int(entry_height.get())
    border = int(entry_border.get())

    # Capture a screen area with the specified border
    screen = ImageGrab.grab(bbox=(x + border, y + border, x + width - border, y + height - border))
    
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
    # Ensure the dominant color is not too dark
    dominant_color = ensure_minimum_brightness(dominant_color)

    # Update the GUI with the dominant color
    color_label.config(bg='#%02x%02x%02x' % dominant_color)
    color_label.after(20, get_dominant_color)  # Re-run this function after 500 ms

# Create the main window
root = tk.Tk()
root.title("Dominant Color Detector")

# Add entry widgets and labels for user input
tk.Label(root, text='X Coordinate:').grid(row=0, column=0)
entry_x = tk.Entry(root)
entry_x.grid(row=0, column=1)
entry_x.insert(0, '1000')

tk.Label(root, text='Y Coordinate:').grid(row=1, column=0)
entry_y = tk.Entry(root)
entry_y.grid(row=1, column=1)
entry_y.insert(0, '500')

tk.Label(root, text='Width:').grid(row=2, column=0)
entry_width = tk.Entry(root)
entry_width.grid(row=2, column=1)
entry_width.insert(0, '100')

tk.Label(root, text='Height:').grid(row=3, column=0)
entry_height = tk.Entry(root)
entry_height.grid(row=3, column=1)
entry_height.insert(0, '100')

tk.Label(root, text='Border Width:').grid(row=4, column=0)
entry_border = tk.Entry(root)
entry_border.grid(row=4, column=1)
entry_border.insert(0, '0')

# Add a label to display the dominant color
color_label = tk.Label(root, text='Dominant Color', font=('Helvetica', 16), width=20, height=5)
color_label.grid(row=5, column=0, columnspan=2)

# Add a button to start the color detection
button_start = tk.Button(root, text='Start Detection', command=get_dominant_color)
button_start.grid(row=6, column=0, columnspan=2)

# Start the GUI event loop
root.mainloop()
