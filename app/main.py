from fastapi import FastAPI


app = FastAPI(
    title="Prism",
    description="Media Consumption Tracker",
    version="1.0.0"
)


@app.get("/")
def root():
    return {"h": "w"}
