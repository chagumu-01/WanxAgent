import asyncio
import random
from typing import Union, List

from openai import AsyncOpenAI
from agentchat.settings import app_settings, initialize_app_settings

embedding_model = app_settings.multi_models.embedding.model_name
embedding_client = AsyncOpenAI(base_url=app_settings.multi_models.embedding.base_url,
                               api_key=app_settings.multi_models.embedding.api_key)

def generate_mock_embedding(dimensions: int = 1024):
    return [random.uniform(-1, 1) for _ in range(dimensions)]

async def get_embedding(query: Union[str, List[str]]):
    api_key = app_settings.multi_models.embedding.api_key
    
    if api_key in ("your_api_key_here", ""):
        if isinstance(query, str):
            return generate_mock_embedding()
        else:
            return [generate_mock_embedding() for _ in query]
    
    try:
        if isinstance(query, str) or (isinstance(query, list) and len(query) <= 10):
            responses = await embedding_client.embeddings.create(
                model=embedding_model,
                input=query,
                encoding_format="float")

            if isinstance(query, str):
                return responses.data[0].embedding
            else:
                return [response.embedding for response in responses.data]

        semaphore = asyncio.Semaphore(5)

        async def process_batch(batch):
            async with semaphore:
                responses = await embedding_client.embeddings.create(
                    model=embedding_model,
                    input=batch,
                    encoding_format="float")
                return [response.embedding for response in responses.data]

        batches = [query[i:i + 10] for i in range(0, len(query), 10)]

        tasks = [process_batch(batch) for batch in batches]
        results = await asyncio.gather(*tasks)

        return [embedding for batch_result in results for embedding in batch_result]
    except Exception as e:
        print(f"Embedding API error: {e}, using mock embedding")
        if isinstance(query, str):
            return generate_mock_embedding()
        else:
            return [generate_mock_embedding() for _ in query]


if __name__ == "__main__":
    asyncio.run(initialize_app_settings("../../config.yaml"))

    asyncio.run(get_embedding(["大模型"]))
