"""
Cosine Similarity Test
"""

import openai
import numpy as np
import os
from openai import OpenAI

def get_embedding(text, model="text-embedding-3-small"):
    """
    Get the embedding for the given text.

    Args:
        text (str): The input text.
        model (str, optional): The name of the embedding model (default is "text-embedding-3-small").

    Returns:
        np.array: The embedding vector.
    """
    api_key = os.getenv("OPENAI_API_KEY", None)
    print(f" Key: {api_key}")
    client = OpenAI(api_key=api_key)
    text = text.replace("\n", " ")
    return client.embeddings.create(input=[text], model=model).data[0].embedding


def cosine_similarity_test(prompt, response, model="text-embedding-3-small", threshold=0.4):
    """
    Provides the cosine similarity score.

    Args:
        prompt (str): The prompt text.
        response (str): The response text.
        model (str, optional): The name of the embedding model (default is "text-embedding-3-small").
        threshold(float, optional): The threshold for cosine similarity score (default is 0.4)

    Returns:
        float: The cosine similarity between prompt and response.
    """
    prompt_embedding = get_embedding(prompt, model)
    response_embedding = get_embedding(response, model)

    # Calculating the similarity
    similarity = np.dot(prompt_embedding, response_embedding) / (
        np.linalg.norm(prompt_embedding) * np.linalg.norm(response_embedding)
    )

    is_similar = "Passed" if (similarity >= threshold) else "Failed"

    result = {
        "prompt": prompt,
        "response": response,
        "score": similarity,
        "is_passed": is_similar,
        "threshold": threshold,
    }
    return result
