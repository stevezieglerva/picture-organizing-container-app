from collections import Counter

import matplotlib.pyplot as plt
from PIL import Image, ImageOps


def posterize(image_path: str, size: tuple = (8, 8)) -> Image:
    # Open the image
    im = Image.open(image_path)
    small = im.resize(size)
    im_posterize = ImageOps.posterize(small, 2)
    return im_posterize


def generate_color_palette(img):
    # Convert the image to RGB mode
    img_rgb = img.convert("RGB")

    # Get the image histogram
    histogram = img_rgb.histogram()
    # Get a flat list of RGB values for all pixels
    rgb_values = list(image.getdata())

    # Print the RGB values
    for rgb in rgb_values:
        r, g, b = rgb
        print(f"RGB values: R={r}, G={g}, B={b}")

    # Convert RGB values to HTML hex colors
    hex_colors = [f"#{r:02x}{g:02x}{b:02x}" for r, g, b in rgb_values]

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
    plt.show()

    # # Initialize a Counter to count color occurrences
    # color_counts = Counter()

    # # Iterate over the histogram bins (0-255)
    # for count, i in enumerate(histogram):
    #     # Skip empty bins
    #     if count == 0:
    #         continue
    #     print(f"count: #{count}")
    #     # Convert bin index to RGB values
    #     r = i // 256 // 256
    #     g = (i // 256) % 256
    #     b = i % 256
    #     print(count, r, g, b)

    #     # Convert RGB values to HTML hex color
    #     hex_color = f"#{r:02x}{g:02x}{b:02x}"

    #     # Update color count
    #     color_counts[hex_color] += count

    # # Extract the HTML hex colors and their frequencies
    # hex_colors = list(color_counts.keys())

    # # Create a color palette image
    # num_colors = len(hex_colors)
    # palette_width = 50
    # palette_height = 50
    # palette_image = Image.new("RGB", (palette_width * num_colors, palette_height))

    # # Draw color swatches on the palette image
    # for i, color in enumerate(hex_colors):
    #     swatch_start = i * palette_width
    #     swatch_end = (i + 1) * palette_width
    #     palette_image.paste(color, (swatch_start, 0, swatch_end, palette_height))

    # # Display the color palette
    # plt.imshow(palette_image)
    # plt.axis("off")
    # plt.title("Color Palette")


# plt.show()


image_path = "lawn_2.jpg"
size = (200, 200)
image = posterize(image_path, size)
new_path = f"posterize_{image_path}.jpg"
image.save(new_path)
generate_color_palette(image)
