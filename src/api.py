from fastapi import FastAPI, HTTPException, UploadFile
from fastapi.responses import JSONResponse

# Create a FastAPI application instance
app = FastAPI()


@app.get("/")
async def hello_world():
    return {"message": "Hello, World!"}


@app.post("/upload")
async def upload_image(file: UploadFile):
    # Check if a file was actually uploaded
    if not file:
        raise HTTPException(status_code=400, detail="No file uploaded")

    # Check if the uploaded file is an image
    if not file.content_type.startswith("image/"):
        raise HTTPException(status_code=400, detail="Uploaded file is not an image")

    # Read the file contents
    contents = await file.read()
    file_size = len(contents)

    return JSONResponse(
        {
            "filename": file.filename,
            "content_type": file.content_type,
            "file_size": file_size,
        }
    )


# This is for running the server directly from this file
if __name__ == "__main__":
    import uvicorn

    uvicorn.run(app, host="127.0.0.1", port=8000)
