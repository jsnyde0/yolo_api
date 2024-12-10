from fastapi import FastAPI

# Create a FastAPI application instance
app = FastAPI()


# This decorator tells FastAPI that this function handles
# GET requests to the "/" URL (root path)
@app.get("/")
async def hello_world():
    return {"message": "Hello, World!"}


# This is for running the server directly from this file
if __name__ == "__main__":
    import uvicorn

    uvicorn.run(app, host="127.0.0.1", port=8000)
