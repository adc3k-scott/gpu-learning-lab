from fastapi import FastAPI
from fastapi.responses import FileResponse
from pydantic import BaseModel

app = FastAPI()

class MessageRequest(BaseModel):
 text: str

@app.get("/")
def root():
 return FileResponse("web/index.html")

@app.post("/message")
def message(msg: MessageRequest):
 return {"response": f"Mission Control received: {msg.text}"}
