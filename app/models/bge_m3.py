from sentence_transformers import SentenceTransformer

class BGEM3Model:
    def __init__(self, model_name: str = "app/models/all-MiniLM-L6-v2"):
        self.model = SentenceTransformer(model_name)

    def encode(self, text: str):
        return self.model.encode(text)
    
# tmp = BGEM3Model()
# tmp.encode("Hello, world!")
