from typing import List, Tuple, AsyncGenerator
import vertexai 
from vertexai.language_models import TextEmbeddingModel
from vertexai.generative_models import GenerativeModel, Content, Part

embeding_model = TextEmbeddingModel.from_pretrained("textembedding-gecko-multilingual@latest")
chat_model = GenerativeModel("gemini-1.0-pro")

async def get_chat_response_stream(conversation: List[Tuple[str, str]], question: str) -> AsyncGenerator[str, bool]:
    history = []
    for pair in conversation:
        history.append(Content(parts = [Part(text=pair[0])], role= "User"))
        history.append(Content(parts = [Part(text=pair[1])], role= "SynapticAI"))
    responses = chat_model.start_chat(history=history).send_message(question, stream=True)
    for chunk in responses:
        yield chunk.text

def get_sentence_embeding(text: str) -> list:
    embeddings = embeding_model.get_embeddings([text])
    vector = embeddings[0].values
    return vector