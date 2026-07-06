from agentchat.settings import app_settings
from agentchat.services.memory.vector_stores.chroma import ChromaDB


class MilvusClient:
    def __init__(self):
        self.mode = app_settings.rag.vector_db.get("mode", "chroma")
        self.clients = {}

    def _get_client(self, collection_name):
        if collection_name not in self.clients:
            self.clients[collection_name] = ChromaDB(collection_name=collection_name)
        return self.clients[collection_name]

    async def search(self, query, knowledge_id):
        if self.mode == "chroma":
            client = self._get_client(str(knowledge_id))
            return client.search(query, [query], filters={"knowledge_id": knowledge_id})
        return []

    async def search_summary(self, query, knowledge_id):
        if self.mode == "chroma":
            client = self._get_client(str(knowledge_id))
            return client.search(query, [query], filters={"knowledge_id": knowledge_id})
        return []

    async def insert(self, collection_name, chunks):
        if self.mode == "chroma":
            client = self._get_client(str(collection_name))
            if chunks:
                vectors = [chunk.get("vector") for chunk in chunks]
                payloads = [chunk.get("metadata") for chunk in chunks]
                ids = [chunk.get("id") for chunk in chunks]
                client.insert(vectors=vectors, payloads=payloads, ids=ids)
        return None

    async def delete_by_file_id(self, file_id, knowledge_id):
        if self.mode == "chroma":
            client = self._get_client(str(knowledge_id))
            client.collection.delete(where={"file_id": file_id})
        return None


milvus_client = MilvusClient()