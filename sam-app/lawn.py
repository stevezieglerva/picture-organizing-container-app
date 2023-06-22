import math

import matplotlib.pyplot as plt
import numpy as np
from PIL import Image, ImageOps


def ceiling(value, grouping: int):
    value = math.ceil(value / grouping) * grouping
    if value > 255:
        value = 255
    return value


def get_dominant_color(image, grouping: int):
    colors = image.getcolors(image.width * image.height)
    dominant_color = max(colors, key=lambda item: item[0])[1]
    dominant_color = (
        ceiling(dominant_color[0], grouping),
        ceiling(dominant_color[1], grouping),
        ceiling(dominant_color[2], grouping),
    )
    return "#{:02x}{:02x}{:02x}".format(*dominant_color)


def rgb_to_hex(rgb_tuple):
    r, g, b = rgb_tuple
    hex_code = "#{:02x}{:02x}{:02x}".format(r, g, b)
    return hex_code


def classify_color(hex_code):
    color_mapping = {
        "White": [(221, 232, 242)],
        "Gray": [(164, 163, 158)],
        "Black": [(1, 1, 1)],
        "Green": [(0, 128, 0)],
        "Yellow": [(255, 255, 0)],
        "Brown": [(85, 65, 62)],
        "Light Green": [(144, 238, 144)],
        "Dark Green": [(106, 117, 60)],
        "Light Yellow": [(255, 255, 153)],
        "Dark Yellow": [(204, 204, 0)],
        "Yellow-Green": [(154, 205, 50)],
    }

    hex_code = hex_code.lstrip("#")
    print(f"\n\n{hex_code}")
    given_rgb = tuple(int(hex_code[i : i + 2], 16) for i in (0, 2, 4))
    scores = []
    for color, rgb_values in color_mapping.items():
        print(f"\tcolor: {color}, rgb_values: {rgb_values}")
        for rgb in rgb_values:
            print(f"\t\tgiven: {given_rgb}")
            print(f"\t\trgb:   {rgb}")

            red_delta = 0
            if rgb[0] > 0:
                red_delta = round(abs(given_rgb[0] - rgb[0]) / rgb[0], 2)
            green_delta = 0
            if rgb[1] > 0:
                green_delta = round(abs(given_rgb[1] - rgb[1]) / rgb[1], 2)
            blue_delta = 0
            if rgb[2] > 0:
                blue_delta = round(abs(given_rgb[2] - rgb[2]) / rgb[2], 2)
            total_delta = red_delta + green_delta + blue_delta
            scores.append((total_delta, color))

            print(f"\t\tdeltas: {red_delta}, {green_delta}, {blue_delta}")
            # if all(abs(given_rgb[i] - rgb[i]) <= 0.2 * 255 for i in range(3)):
            #     return color
    print(sorted(scores))
    best_color_match = sorted(scores)[0][1]
    best_color = color_mapping[best_color_match]
    print(f"best_color_match: {best_color_match}")
    return best_color_match, rgb_to_hex(best_color[0])


def generate_html_table(grid, image_path):
    html = f"<img width=300px; src='{image_path}'/><img src='lawn_histogram.jpg'/><br><table>"
    for row in grid:
        html += "<tr>"
        for color in row:
            # color_name, matched_color = classify_color(color)
            html += (
                f'<td height=10px; width=10px; style="background-color: {color};"></td>'
            )
        html += "</tr>"
    html += "</table>"
    return html


def rotate_grid(grid):
    transposed_grid = list(map(list, zip(*grid)))

    mirrored_grid = [row for row in transposed_grid]

    return mirrored_grid


def analyze_lawn(image_path, width: int, grouping: int):
    # Load the image
    image = Image.open(image_path)
    image = ImageOps.exif_transpose(image)
    print(image.size)
    aspect_ratio = image.size[0] / image.size[1]
    print(aspect_ratio)

    height = int(width / aspect_ratio)
    grid_size = (width, height)

    # Resize the image
    image = image.resize(grid_size)

    # Convert the image to RGB
    image = image.convert("RGB")

    # Create the grid
    grid_width = image.width // grid_size[0]
    grid_height = image.height // grid_size[1]
    grid = [[None for _ in range(grid_size[1])] for _ in range(grid_size[0])]

    # Iterate through each grid cell
    for x in range(grid_size[0]):
        for y in range(grid_size[1]):
            # Define the coordinates of the current grid cell
            left = x * grid_width
            upper = y * grid_height
            right = (x + 1) * grid_width
            lower = (y + 1) * grid_height

            # Crop the image to the current grid cell
            cell_image = image.crop((left, upper, right, lower))

            # Calculate the dominant color in the cell
            dominant_color = get_dominant_color(cell_image, grouping)

            # # Convert RGB to normalized color
            # normalized_color = normalize_color(dominant_color, num_bins)

            # Store the normalized color in the grid
            grid[x][y] = dominant_color

    # Generate HTML table with color-coded cells
    rotated_grid = rotate_grid(grid)
    html_table = generate_html_table(rotated_grid, image_path)

    # Print or save the HTML table
    with open("lawn.html", "w") as file:
        file.write(html_table)

    # Flatten the grid to create a list of HTML color codes
    flattened_grid = np.array(rotated_grid).flatten()

    # Calculate the histogram of HTML color codes
    histogram, bins = np.histogram(flattened_grid, bins=np.unique(flattened_grid))

    # Plot the histogram
    plt.bar(bins[:-1], histogram, color=bins[:-1])
    plt.xlabel("HTML Color Code")
    plt.ylabel("Count")
    plt.ylim(0, 2500)
    plt.title("Histogram of Dominant Color Codes")
    plt.xticks(rotation=45)
    plt.savefig("lawn_histogram.jpg")


# Usage example
image_path = "lawn_5.jpg"  # Replace with the path to your image
analyze_lawn(image_path, 75, 100)
