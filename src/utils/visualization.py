import colorsys

from PIL import Image, ImageDraw
from ultralytics.engine.results import Results


def generate_colors(n: int) -> list[tuple[int, int, int]]:
    """Generate n distinct colors using HSV color space."""
    colors = []
    golden_ratio_conjugate = 0.618033988749895  # More distinct spacing

    for i in range(n):
        # Use golden ratio conjugate for better hue distribution
        hue = (i * golden_ratio_conjugate) % 1
        # Higher saturation for more vibrant colors
        sat = 0.95
        # Alternate value to create more contrast
        val = 0.95 if i % 2 == 0 else 0.8

        rgb = colorsys.hsv_to_rgb(hue, sat, val)
        color = (int(rgb[0] * 255), int(rgb[1] * 255), int(rgb[2] * 255))
        colors.append(color)

    return colors


def draw_detections(
    image: Image.Image,
    detections: Results,
    confidence: float = 0.5,
    box_thickness: int = 3,
    font_size: int = 16,
) -> Image.Image:
    """Draw detection boxes and labels on image."""
    draw = ImageDraw.Draw(image)

    # Generate a color for each class
    num_classes = len(detections.names)
    colors = generate_colors(num_classes)

    for detection in detections.boxes.data:
        x1, y1, x2, y2, score, class_id = detection

        # Only show predictions above confidence threshold
        if score > confidence:
            # Convert tensor values to integers
            box_coords = [int(x1), int(y1), int(x2), int(y2)]
            class_id_int = int(class_id)

            # Get color for this class
            color = colors[class_id_int]

            # Draw box
            draw.rectangle(box_coords, outline=color, width=2)

            # Add label
            label = f"{detections.names[int(class_id)]} {score:.2f}"
            draw.text((box_coords[0], box_coords[1] - 10), label, fill=color)

    return image
