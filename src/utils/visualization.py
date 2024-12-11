from PIL import Image, ImageDraw
from ultralytics.engine.results import Results


def draw_detections(
    image: Image.Image,
    detections: Results,
    confidence: float = 0.5,
    box_thickness: int = 3,
    font_size: int = 16,
) -> Image.Image:
    """Draw detection boxes and labels on image."""
    draw = ImageDraw.Draw(image)

    for detection in detections.boxes.data:
        x1, y1, x2, y2, score, class_id = detection

        # Only show predictions above confidence threshold
        if score > confidence:
            # Convert tensor values to integers
            box_coords = [int(x1), int(y1), int(x2), int(y2)]

            # Draw box
            draw.rectangle(box_coords, outline="red", width=2)

            # Add label
            label = f"{detections.names[int(class_id)]} {score:.2f}"
            draw.text((box_coords[0], box_coords[1] - 10), label, fill="red")

    return image
