from PIL import Image


def preprocess_image(image: Image.Image, target_size: int = 640) -> Image.Image:
    """
    Resize image to target size while maintaining aspect ratio.
    Returns the resized image.
    """
    # Get original dimensions
    orig_width, orig_height = image.size

    # Calculate scale
    scale = target_size / max(orig_width, orig_height)

    # Calculate new dimensions
    new_width = int(orig_width * scale)
    new_height = int(orig_height * scale)

    # Resize image
    resized_image = image.resize((new_width, new_height))

    return resized_image
