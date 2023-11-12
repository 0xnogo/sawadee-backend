from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from model import getTravelPlan

# Create an instance of the FastAPI class
app = FastAPI()

app.add_middleware(
  CORSMiddleware,
  allow_origins=['http://localhost:3000'],
  allow_credentials=True,
  allow_methods=['*'],
  allow_headers=['*'],
)

# Define a "Hello, World!" route
@app.get("/")
def read_root():
    return {"message": "Hello, World!"}

@app.get("/travel-plan")
def get_travel_plan(location: str):
  return getTravelPlan(location)