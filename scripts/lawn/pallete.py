import json
import math
from collections import Counter

import matplotlib.pyplot as plt
import numpy as np
from Picture import ImageIOLocal, Picture
from PIL import Image, ImageOps


def posterize(image_path: str, size: tuple = (8, 8)) -> Image:
    # Open the image
    image = Picture(image_path, ImageIOLocal())._pil_image
    small = image.resize(size)

    np_image = np.array(small)

    np_normalized = np.ceil(np_image / 100) * 100
    np_normalized = np.clip(np_normalized, None, 255).astype(np.uint8)
    im_posterize = Image.fromarray(np_normalized)

    return im_posterize


def rgb_to_hex(rgb):
    """Converts RGB color values to a hexadecimal color code."""
    r, g, b = rgb
    hex_code = "#{:02x}{:02x}{:02x}".format(r, g, b)
    return hex_code


def hex_to_rgb(hex_code):
    """Converts a hexadecimal color code to RGB color values."""
    hex_code = hex_code.lstrip("#")
    r = int(hex_code[0:2], 16)
    g = int(hex_code[2:4], 16)
    b = int(hex_code[4:6], 16)
    rgb = (r, g, b)
    return rgb


def filter_image_by_color(image, target_color_hex, size: tuple = (200, 200)):
    target_color = hex_to_rgb(target_color_hex)

    # Convert the image to a NumPy array
    np_image = np.array(image)

    # Convert the target color to NumPy array
    target_color = np.array(target_color)

    # Create a mask of pixels that match the target color
    mask = np.all(np_image == target_color, axis=2)

    # Create a new NumPy array with only the target color pixels
    filtered_np_image = np.zeros_like(np_image)
    filtered_np_image[mask] = target_color

    # Create a PIL image from the filtered NumPy array
    filtered_image = Image.fromarray(filtered_np_image)

    return filtered_image


def generate_color_palette(image_path: str, size: tuple = (200, 200)):
    image = posterize(image_path, size)
    image.save(f"output/posterize_{image_path}")

    # Get a flat list of RGB values for all pixels
    rgb_values = list(image.getdata())

    # Convert RGB values to HTML hex colors
    hex_colors = [f"#{r:02x}{g:02x}{b:02x}" for r, g, b in rgb_values]
    counter = Counter(hex_colors)

    # Count the occurrences of each color
    color_counts = {}
    for hex_color in hex_colors:
        if hex_color in color_counts:
            color_counts[hex_color] += 1
        else:
            color_counts[hex_color] = 1

    # Extract the colors and counts for plotting
    colors = list(color_counts.keys())
    counts = list(color_counts.values())

    # Create the histogram plot
    plt.bar(colors, counts, color=colors)

    # Set the x-axis labels to the HTML hex colors
    plt.xticks(rotation=90)

    # Display the plot
    plt.tight_layout()
    plt.savefig(f"output/histogram_{image_path}")

    # for count, color in enumerate(counter.most_common(3)):
    for count, color in enumerate(
        [("#c8c864", 0), ("#64c864", 0), ("#c8c8c8", 0), ("#ffc8c8", 0)]
    ):
        filtered_image = filter_image_by_color(image, color[0], size)
        filename_color = color[0].strip("#")
        file_name = f"output/filter_{count+1}_{image_path}"
        filtered_image.save(file_name)

    return counter


from glob import glob

size = (200, 200)
images = sorted(glob("2023*.jpg"))
html = """<head>
    <title>Lawn</title>
</head>"""

for image in images:
    print(f"\n\n{image}")
    color_counts = generate_color_palette(image, size)
    top_pallete = ""
    for color in color_counts.most_common(5):
        print(color)

    top_colors_list = [
        f"<td style='padding: 5px; background-color: {c[0]};'>{c[0]}</td>"
        for c in color_counts.most_common(5)
    ]
    top_colors = "".join(top_colors_list)
    image_html = f"""
<h1>{image}</h1>
<table>
<tr valign='top'>
    <td><img src='output/{image}'></td>
    <td><img src='output/posterize_{image}'></td>
    <td><img src='output/histogram_{image}' width=400><br/>
    <table>
        <tr>
    {       top_colors}
        </tr>
    </table>
    </td>
    <td><img src='output/filter_1_{image}'></td>
    <td><img src='output/filter_2_{image}'></td>
    <td><img src='output/filter_3_{image}'></td>
    <td><img src='output/filter_4_{image}'></td>
    
</tr>
</table>
    """
    html += image_html


with open("lawn.html", "w") as file:
    file.write(html)
