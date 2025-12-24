from PIL import Image


def read_image(filepath):
    """
    Load an image from file

    Args:
        filepath: Path to image file

    Returns:
        RGB image as 3D list [height][width][3]
    """
    img = Image.open(filepath)
    img = img.convert("RGB")
    width, height = img.size
    pixels = img.load()

    rgb_image = []
    for y in range(height):
        row = []
        for x in range(width):
            row.append(list(pixels[x, y]))
        rgb_image.append(row)

    return rgb_image


def rgb_to_grayscale(rgb_image):
    """
    Convert RGB image to grayscale using luminosity method

    Args:
        rgb_image: 3D list [height][width][3]

    Returns:
        Grayscale image as 2D list [height][width]
    """
    height = len(rgb_image)
    width = len(rgb_image[0])

    grayscale = []
    for y in range(height):
        row = []
        for x in range(width):
            r, g, b = rgb_image[y][x]
            # Luminosity method: 0.299*R + 0.587*G + 0.114*B
            intensity = int(0.299 * r + 0.587 * g + 0.114 * b)
            row.append(intensity)
        grayscale.append(row)

    return grayscale


def save_grayscale_image(grayscale, filepath):
    """
    Save a 2D grayscale array as an image.

    Args:
        grayscale: 2D list [height][width] of intensity values 0–255
        filepath: Output image path
    """
    height = len(grayscale)
    width = len(grayscale[0])

    # Create a new Pillow image in "L" mode (8-bit grayscale)
    img = Image.new("L", (width, height))

    # Flatten the 2D list → 1D list because putdata expects a sequence
    flat = [pixel for row in grayscale for pixel in row]

    img.putdata(flat)
    img.save(filepath)


def extract_3msb_from_intensity(intensity):
    """
    Extract 3 Most Significant Bits from an intensity value (0-255)
    This converts the range from 0-255 to 0-7

    Args:
        intensity: Pixel intensity value (0-255)

    Returns:
        3-MSB value (0-7)

    Example:
        186 (binary: 10111010) >> 5 = 5 (binary: 00000101)
    """
    # Shift right by 5 bits to keep only the 3 MSB
    msb_value = intensity >> 5
    return msb_value


def extract_3msb_image(grayscale_image):
    """
    Extract 3 MSB from entire grayscale image
    Converts each pixel from 0-255 range to 0-7 range

    Args:
        grayscale_image: 2D list with values 0-255

    Returns:
        3-MSB image as 2D list with values 0-7
    """
    height = len(grayscale_image)
    width = len(grayscale_image[0])

    msb_image = []
    for y in range(height):
        row = []
        for x in range(width):
            original_intensity = grayscale_image[y][x]
            msb_value = extract_3msb_from_intensity(original_intensity)
            row.append(msb_value)
        msb_image.append(row)

    return msb_image


def save_texture_map(texture_map, filepath):
    """
    Save texture map as image (0=black/smooth, 1=white/rough)

    Args:
        texture_map: 2D array with 0s and 1s
        filepath: Output file path
    """
    height = len(texture_map)
    width = len(texture_map[0])

    # Create image
    img = Image.new("L", (width, height))
    pixels = img.load()

    # Convert texture map to pixel values (0→0/black, 1→255/white)
    for y in range(height):
        for x in range(width):
            pixels[x, y] = texture_map[y][x] * 255

    img.save(filepath)
    print(f"✓ Texture map saved to: {filepath}")
