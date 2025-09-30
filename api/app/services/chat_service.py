import os
import logging
import asyncio
import psycopg2
from psycopg2 import sql
from psycopg2.extras import RealDictCursor

from typing import List, Optional, Dict, Any
from pinecone import Pinecone, ServerlessSpec, Index

DB_CONFIG = {
    'host': os.getenv('DB_HOST', 'localhost'),
    'port': os.getenv('DB_PORT', '5432'),
    'database': os.getenv('DB_NAME', 'rag_chat'),
    'user': os.getenv('DB_USER', 'postgres'),
    'password': os.getenv('DB_PASSWORD', 'password')
}

try:
    import torch
    from sentence_transformers import SentenceTransformer


except ImportError:
    class SentenceTransformer:
        def __init__(self, *args, **kwargs): pass
        def get_sentence_embedding_dimension(self): return 1024
        def encode(self, *args, **kwargs): return [0.0] * 1024

    class torch:
        @staticmethod
        def cuda(): return False
        @staticmethod
        def is_available(): return False

logging.basicConfig(level=logging.INFO, format='%(levelname)s: %(message)s')

EXPECTED_DIMENSIONS = 1024 
MODEL_NAME = "BAAI/bge-large-en-v1.5" 

class LocalEmbedder:
    def __init__(self):
        self.model: Optional[SentenceTransformer] = None
        self._initialize_model()

    def _initialize_model(self):
        try:
            device = "cuda" if torch.cuda.is_available() else "cpu"
            self.model = SentenceTransformer(MODEL_NAME, device=device)
            logging.info(f"Model loaded successfully on device: {device}")

        except Exception as e:
            self.model = None

    def embed_query(self, text: str) -> List[float]:
        if not self.model:
            return [0.0] * EXPECTED_DIMENSIONS
            
        logging.info(f"Generating embedding for query...")
        embedding = self.model.encode(text, convert_to_tensor=True)
        
        return embedding.tolist()


class ChatService:
    def __init__(self):
        self.pc: Optional[Pinecone] = None
        self.index: Optional[Index] = None
        self.embedder: Optional[LocalEmbedder] = None
        self.__config()

    def __config(self):
        self.api_key = os.getenv("PINECONE_API_KEY", "I wont let the key here :P, even thou its a dev enviroment")
        if not self.api_key:
            raise ValueError("PINECONE_API_KEY not found!")

        try:
            self.pc = Pinecone(api_key=self.api_key)
        except Exception as e:
            logging.error(f"Failed to initialize Pinecone client: {e}")
            raise

        index_name = "ai-powered-chatbot-challenge-omkb0qe"
        
        if not self.pc.has_index(index_name):
            logging.info(f"Creating Pinecone index: {index_name}")
            self.pc.create_index(
                name=index_name,
                dimension=1024,
                metric="cosine",
                spec=ServerlessSpec(cloud="aws", region="us-east-1")
            )
        
        self.endpoint = os.getenv("PINECONE_ENDPOINT", "https://ai-powered-chatbot-challenge-omkb0qe.svc.aped-4627-b74a.pinecone.io")

        self.index = self.pc.Index(index_name, host=self.endpoint)
        logging.info(f"Successfully connected to Pinecone index: {index_name}")

        self.embedder = LocalEmbedder()

    def embed_query(self, text: str) -> List[float]:
        if not self.embedder:
             raise RuntimeError("Embedder not initialized.")
        return self.embedder.embed_query(text)

    def _sync_query(self, query_vector: List[float]) -> Dict[str, Any]:
        results = self.index.query(
            vector=query_vector,
            top_k=3,
            include_metadata=True
        )
        return {
            "matches": [
                {"id": m.id, "score": m.score, "metadata": m.metadata}
                for m in results.matches
            ]
        }

    def save_message(self, chatUUID: str, message: str, is_response: bool = False) -> None:
        query = """
            INSERT INTO messages (chat_id, content, is_response)
            VALUES (%s, %s, %s)
        """

        conn = None
        try:
            conn = psycopg2.connect(**DB_CONFIG)
            with conn.cursor() as cur:
                cur.execute(query, (chatUUID, message, is_response))
                conn.commit()
        except psycopg2.Error as e:
            if conn:
                conn.rollback()
            print(f"Database error: {e}")
            raise
        finally:
            if conn:
                conn.close()

    def create_new_chat(self, user_id: str = None) -> Optional[str]:
        query = """
            INSERT INTO chats (user_id)
            VALUES (%s)
            RETURNING id;
        """

        conn = None
        new_chat_uuid = None
        try:
            
            conn = psycopg2.connect(**DB_CONFIG)
            with conn.cursor() as cur:
                cur.execute(query, (user_id,))
                new_chat_uuid = cur.fetchone()[0]
                conn.commit()
        
            if new_chat_uuid:
                return new_chat_uuid
                
        except psycopg2.Error as e:
            if conn:
                conn.rollback()
            print(f"Database error in create_new_chat: {e}")
            raise
            
        except Exception as e:
            print(f"An unexpected error occurred: {e}")
            raise
            
        finally:
            if conn:
                conn.close()
                
        return None

    async def send_message(self, chatUUID: str,  message: str) -> dict:
        logging.info(f"Processing message: {message}")

        print("\n\n\n\n\n")
        print(chatUUID)
        print(message)
        print("\n\n\n\n\n")
        
        self.save_message(chatUUID, message, False)

        query_vector = self.embed_query(message)

        
        try:
            query_results = await asyncio.to_thread(self._sync_query, query_vector)
           
            self.save_message(chatUUID, query_results[0]["metadata"], True)
           
            return {
                "query": message,
                "matches": query_results["matches"]
            }
        except Exception as e:
            logging.error(f"Pinecone Query Failed: {e}")
            return {"query": message, "error": f"Pinecone query failed: {e}"}
