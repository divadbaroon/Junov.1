from fastapi import FastAPI
from pydantic import BaseModel
from src.juno import Juno

app = FastAPI()
new_bot = Juno()

class TextData(BaseModel):
    text: str

@app.post("/process/")
def process_text(data: TextData):
    processed_text = start_session(data.text)
    return {"processed_text": processed_text}

def start_session(text):

    speech = new_bot.listen()
    text = speech + text
    response = new_bot.process(text)
    new_bot.verbalize(response)
