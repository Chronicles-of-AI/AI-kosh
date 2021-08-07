from fastapi import FastAPI
import uvicorn

# Declare a FastAPI instance
app = FastAPI()

# Create a POST type of router with a URL end point name of your choice
@app.post("/test_router")
def test_function():
    return {"Success": "I did it"}


# Run the script
if __name__ == "__main__":
    uvicorn.run(app)
