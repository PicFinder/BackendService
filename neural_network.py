from typing import List

import numpy as np
import torch
from transformers import CLIPProcessor, CLIPModel
from abc import ABC, abstractmethod

device = torch.device("cuda" if torch.cuda.is_available() else "cpu")


class Network(ABC):
    @abstractmethod
    def find_top_k(self, text_query: str, embeddings_list: List[np.ndarray], top_k: int) -> List[int]:
        """Find most similar embeddings to text_query."""
        pass

    @abstractmethod
    def transform_images(self, images) -> List[np.ndarray]:
        """Transform images to embeddings.
        Return:
            List[np.ndarray]: List of embeddings.
        """
        pass


class OpenAIClipNetwork(Network):
    """
    Network which performs transformation of images and texts to latent space
    """

    def __init__(self, model_config="openai/clip-vit-base-patch32"):
        self.model = CLIPModel.from_pretrained(model_config).to(device)  # hugging lover
        self.model.eval()
        self.processor = CLIPProcessor.from_pretrained(model_config)

    def transform_images(self, images) -> List[np.ndarray]:
        inputs = self.processor(images=images, return_tensors="pt", padding=True, device=device)
        inputs['pixel_values'] = inputs['pixel_values'].to(device)
        with torch.no_grad():
            outputs = self.model.get_image_features(**inputs)

        return outputs.to('cpu').numpy()

    def transform_texts(self, texts):
        inputs = self.processor(text=texts, return_tensors="pt", padding=True)
        inputs['input_ids'] = inputs['input_ids'].to(device)
        inputs['attention_mask'] = inputs['attention_mask'].to(device)
        with torch.no_grad():
            outputs = self.model.get_text_features(**inputs)

        return outputs.to('cpu').numpy()

    def find_top_k(self, text_query: str, embeddings_list: List[np.ndarray], top_k: int) -> List[int]:
        inputs = self.processor(text=[text_query], return_tensors="pt", padding=True)
        inputs['input_ids'] = inputs['input_ids'].to(device)
        inputs['attention_mask'] = inputs['attention_mask'].to(device)

        with torch.no_grad():
            query_embedding = self.model.get_text_features(**inputs)

        query_embedding = query_embedding.cpu().numpy()
        embeddings = np.array(embeddings_list)

        similarities = np.dot(embeddings, query_embedding.T).flatten()
        similarities = similarities / (np.linalg.norm(embeddings, axis=1) * np.linalg.norm(query_embedding))

        top_k_indices = np.argsort(similarities)[-top_k:][::-1].tolist()
        return top_k_indices

# network: Network = OpenAINetwork()
