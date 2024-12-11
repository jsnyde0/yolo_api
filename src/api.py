import io

from fastapi import FastAPI, HTTPException, UploadFile
from fastapi.responses import StreamingResponse
from PIL import Image

# Create a FastAPI application instance
app = FastAPI()


@app.get("/")
async def hello_world():
    return {"message": "Hello, World!"}


@app.post("/process")
async def upload_image(
    file: UploadFile,
    size: int = 640,
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
        image = Image.open(io.BytesIO(contents))

        # Process image
        # Resize while maintaining aspect ratio
        image.thumbnail((size, size))

        # Convert the processed image to bytes
        img_byte_arr = io.BytesIO()
        image.save(img_byte_arr, format=image.format or "JPEG")
        img_byte_arr.seek(0)  # Move to start of byte array

        # Return the processed image
        return StreamingResponse(
            img_byte_arr,
            media_type=file.content_type,
        )

    except Exception as e:
        raise HTTPException(
            status_code=500, detail=f"Image processing failed: {str(e)}"
        ) from e


# This is for running the server directly from this file
if __name__ == "__main__":
    import uvicorn

    uvicorn.run(app, host="127.0.0.1", port=8000)
