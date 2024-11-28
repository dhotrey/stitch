import qrcode
from PIL import Image
import numpy as np
# yellow - purple
# blue - red


def create_colored_qr(data, fill_color="purple", background_color="yellow", size=10):
    """
    Create a QR code with custom colors
    """
    qr = qrcode.QRCode(
        version=1,
        error_correction=qrcode.constants.ERROR_CORRECT_L,
        box_size=size,
        border=0,
    )

    qr.add_data(data)
    qr.make(fit=True)
    qr_image = qr.make_image(fill_color=fill_color, back_color=background_color)
    return qr_image


def get_color_value(pixel):
    """
    Convert pixel RGB to color name with more flexible matching
    """
    # print(f"Processing pixel: {pixel}")  # Debug print

    # Convert pixel to RGB if it's not already a tuple
    if not isinstance(pixel, tuple):
        pixel = tuple(pixel)

    # Define color ranges for more flexible matching
    if pixel[0] > 200 and pixel[1] > 200 and pixel[2] < 100:  # Yellow-ish
        return "yellow"
    elif pixel[0] > 200 and pixel[1] < 100 and pixel[2] < 100:  # Red-ish
        return "red"
    elif pixel[0] < 100 and pixel[1] < 100 and pixel[2] > 200:  # Blue-ish
        return "blue"
    elif pixel[0] > 100 and pixel[1] < 100 and pixel[2] > 100:  # Purple-ish
        return "purple"

    print(f"Unknown color for pixel: {pixel}")  # Debug print
    return "unknown"


def color_name_to_rgb(color_name):
    """
    Convert color name to RGB tuple with standard web colors
    """
    color_map = {
        "purple": (128, 0, 128),  # Standard purple
        "yellow": (255, 255, 0),  # Standard yellow
        "red": (255, 0, 0),  # Standard red
        "blue": (0, 0, 255),  # Standard blue
        "green": (0, 255, 0),  # Blend result
        "orange": (255, 165, 0),  # Blend result
        "indigo": (75, 0, 130),  # Blend result
        "magenta": (255, 0, 255),  # Blend result
        "black": (0, 0, 0),  # Default
    }
    return color_map.get(color_name, (0, 0, 0))


def blend_images(img1, img2, blend_rules):
    """
    Blend two images based on provided color combination rules
    """
    # Convert images to RGB mode
    img1 = img1.convert("RGB")
    img2 = img2.convert("RGB")

    # Get image dimensions
    width = img1.size[0]
    height = img1.size[1]

    # Create new image
    blended = Image.new("RGB", (width, height))

    # Convert images to numpy arrays for easier processing
    arr1 = np.array(img1)
    arr2 = np.array(img2)

    # Create output array
    output = np.zeros((height, width, 3), dtype=np.uint8)

    # Process each pixel
    for y in range(height):
        for x in range(width):
            color1 = get_color_value(tuple(arr1[y, x]))
            color2 = get_color_value(tuple(arr2[y, x]))

            # Create sorted tuple for consistent dictionary lookup
            color_key = tuple(sorted([color1, color2]))
            result_color = blend_rules.get(color_key, "black")

            # Set pixel in output array
            output[y, x] = color_name_to_rgb(result_color)

    # Convert numpy array back to PIL Image
    blended = Image.fromarray(output)
    return blended


if __name__ == "__main__":
    # Create QR codes
    data1 = "yellow purple qrcode data"
    data2 = "red blue qrcode data"

    qr1 = create_colored_qr(data1)
    qr2 = create_colored_qr(data2, fill_color="red", background_color="blue")

    # Save and print information about individual QR codes
    qr1.save("imgs/purple_yellow_qrcode.png")
    qr2.save("imgs/red_blue_qrcode.png")

    print("QR Code 1 size:", qr1.size)
    print("QR Code 2 size:", qr2.size)

    # Define blend rules with both orderings
    blend_rules = {
        ("yellow", "blue"): "green",
        ("blue", "yellow"): "green",
        ("yellow", "red"): "orange",
        ("red", "yellow"): "orange",
        ("purple", "blue"): "indigo",
        ("blue", "purple"): "indigo",
        ("purple", "red"): "magenta",
        ("red", "purple"): "magenta",
    }

    # Create and save blended image
    blended_qr = blend_images(qr1, qr2, blend_rules)
    blended_qr.save("imgs/blended_qrcode.png")

    print("Blending complete. Check blended_qrcode.png")
