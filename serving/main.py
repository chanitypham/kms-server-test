from fastapi import FastAPI, Query
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import StreamingResponse
from pydantic import BaseModel
import time
from typing import List
import synaptic_ai
from google.cloud import firestore

# run with: uvicorn main:app --reload

class Note(BaseModel):
    name: str
    neighbor: List[str]
    def __str__(self):
        return f"\"<a href='{url+self.name}'>{self.name}</a>\"" 
    
app = FastAPI(description="SynapticVault API", version="0.0.1", title="SynapticVault API", openapi_url="/openapi.json", docs_url="/docs", redoc_url="/redoc")
app.add_middleware(
    CORSMiddleware,
    allow_origins=["synapticvault.com"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


#TODO: get URL from secret manager
url = "https://synapticvault.com/"
firestore_client = firestore.Client()

@app.get("/SynapticAI", description = "Get a question and stream the answer back, then return the latency.", response_description = "The answer to the question is streamed back alongwith notes written as HTML href and the last chunk is the response object.")
async def SynapticAI(
    question: str = Query(None, description="Question asked by the user"), 
    user_hash: str = Query(None, description="User hash to track user's chat history, generated with SHA256"), 
    note: str = Query(None, description="Note name in the database"),
    endchat: bool = Query(False, description= "include it if user wish to end the conversation")) -> StreamingResponse:
    async def inner():
        # TODO: use user_hash to get the conversation history from the firestore database
        # TODO: filter only to the latest set of messages
        # TODO: Use it to get the messages and put into the conversation_list
        conversation_list = []
        # TODO: Upload the newest message pair


        
        async for chunk in synaptic_ai.get_chat_response_stream(conversation = conversation_list, question = question):
            # TODO: chunk is a few words of the response, find the words that mean a note then convert it to the html format
            # TODO: Check if it has a note or start of a note
            # Add to message pair to database with time
            
            yield chunk
    return StreamingResponse(content=inner(), media_type="text/plain")