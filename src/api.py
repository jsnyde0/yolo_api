import io

from fastapi import FastAPI, HTTPException, UploadFile
from fastapi.responses import StreamingResponse
from PIL import Image, ImageDraw
from ultralytics import YOLO

# Create a FastAPI application instance
app = FastAPI()

model = YOLO("yolo11n.pt")


@app.get("/")
async def hello_world():
    return {"message": "Hello, World!"}


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


@app.post("/detect")
async def detect_objects(
    file: UploadFile,
    confidence: float = 0.5,
    target_size: int = 640,  # default YOLO input size
):
    # Check if a file was actually uploaded
    if not file:
        raise HTTPException(status_code=400, detail="No file uploaded")

    # Check if the uploaded file is an image
    if not file.content_type.startswith("image/"):
        raise HTTPException(status_code=400, detail="Uploaded file is not an image")

    try:
        # Read image file
        contents = await file.read()
        original_image = Image.open(io.BytesIO(contents))
        processed_image = preprocess_image(original_image, target_size)

        # Run inference
        results = model(processed_image)[0]  # [0] because we only have one image

        # Create a drawing object
        draw = ImageDraw.Draw(processed_image)

        # Draw boxes and labels
        for result in results.boxes.data:
            x1, y1, x2, y2, score, class_id = result

            # Only show predictions above confidence threshold
            if score > confidence:
                # Convert tensor values to integers
                box_coords = [int(x1), int(y1), int(x2), int(y2)]

                # Draw box
                draw.rectangle(box_coords, outline="red", width=2)

                # Add label
                label = f"{results.names[int(class_id)]} {score:.2f}"
                draw.text((box_coords[0], box_coords[1] - 10), label, fill="red")

        # Convert the processed image to bytes
        img_byte_arr = io.BytesIO()
        processed_image.save(img_byte_arr, format="JPEG", quality=95)
        img_byte_arr.seek(0)  # Move to start of byte array

        # Return the processed image
        return StreamingResponse(
            img_byte_arr,
            media_type=file.content_type,
        )

    except Exception as e:
        raise HTTPException(
            status_code=500, detail=f"Object Detection failed: {str(e)}"
        ) from e


# This is for running the server directly from this file
if __name__ == "__main__":
    import uvicorn

    uvicorn.run(app, host="127.0.0.1", port=8000)
