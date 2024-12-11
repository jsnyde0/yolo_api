import io

from fastapi import FastAPI, HTTPException, UploadFile
from fastapi.responses import StreamingResponse
from PIL import Image
from ultralytics import YOLO

from src.utils.image import preprocess_image
from src.utils.visualization import draw_detections

# Create a FastAPI application instance
app = FastAPI()

model = YOLO("yolo11n.pt")


@app.get("/")
async def hello_world():
    return {"message": "Hello, World!"}


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

        # draw detections
        processed_image = draw_detections(
            processed_image,
            results,
            confidence=confidence,
            box_thickness=2,
            font_size=16,
        )

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
