import os
import pymupdf
from typing import List, Dict
from pinecone import Pinecone
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain_openai import OpenAIEmbeddings
import deepl
from dotenv import load_dotenv
import time
from deepl.exceptions import DeepLException

load_dotenv()

# Initialize Pinecone
pc = Pinecone(api_key=os.getenv("PINECONE_API_KEY"))
index = pc.Index(os.getenv("PINECONE_INDEX"))

# Initialize DeepL translator
translator = deepl.Translator(os.getenv("DEEPL_API_KEY"))

def extract_text_from_pdf(file_path: str) -> str:
    doc = pymupdf.open(file_path)
    text = ""
    for page in doc:
        text += page.get_text()
    return text

def translate_text(text: str, target_lang: str, max_retries=3) -> str:
    if target_lang == "EN-GB":
        return text
    
    for attempt in range(max_retries):
        try:
            result = translator.translate_text(text, target_lang=target_lang)
            return result.text
        except DeepLException as e:
            if attempt < max_retries - 1:
                print(f"Translation attempt {attempt + 1} failed. Retrying in 5 seconds...")
                time.sleep(5)
            else:
                print(f"Failed to translate after {max_retries} attempts. Using original text.")
                return text

def process_and_index_documents(directory: str, jurisdictions: Dict[str, str], languages: List[str]):
    text_splitter = RecursiveCharacterTextSplitter(chunk_size=1000, chunk_overlap=200)
    embeddings = OpenAIEmbeddings()

    for jurisdiction, filename in jurisdictions.items():
        file_path = os.path.join(directory, filename)
        if os.path.exists(file_path):
            print(f"Processing file: {file_path}")
            text = extract_text_from_pdf(file_path)
            chunks = text_splitter.split_text(text)
            print(f"Number of chunks for {jurisdiction}: {len(chunks)}")

            for lang in languages:
                translated_chunks = [translate_text(chunk, lang) for chunk in chunks]
                
                for i, chunk in enumerate(translated_chunks):
                    vector = embeddings.embed_query(chunk)
                    metadata = {
                        "jurisdiction": jurisdiction,
                        "language": lang,
                        "chunk_id": i
                    }
                    index.upsert([(f"{jurisdiction}_{lang}_{i}", vector, metadata)])
                print(f"Indexed {len(translated_chunks)} chunks for {jurisdiction} in {lang}")

    print("Documents processed and indexed successfully.")

if __name__ == "__main__":
    jurisdictions = {
        "England_Wales": "england&wales.pdf",
        "Scotland": "scotland.pdf",
        "Northern_Ireland": "n_ireland.pdf"
    }
    languages = ["EN-GB", "FR"]  # English and French
    process_and_index_documents("legal_files", jurisdictions, languages)