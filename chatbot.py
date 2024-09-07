import os
from typing import List, Dict, Any
from dotenv import load_dotenv
from langchain_openai import OpenAIEmbeddings, ChatOpenAI
from langchain_community.vectorstores import Pinecone
from langchain.chains import LLMChain
from langchain.prompts import PromptTemplate
from pinecone import Pinecone as PineconeClient

load_dotenv()

# Initialize Pinecone
pc = PineconeClient(api_key=os.getenv("PINECONE_API_KEY"))
index = pc.Index(os.getenv("PINECONE_INDEX"))

class LegalChatbot:
    def __init__(self, language: str, jurisdiction: str):
        self.language = "EN-GB" if language == "English" else "FR"
        self.jurisdiction = jurisdiction
        self.embeddings = OpenAIEmbeddings()
        self.llm = ChatOpenAI(temperature=0.7, model_name="gpt-4")
        self.vectorstore = Pinecone(index, self.embeddings.embed_query, "text")
        self.retriever = self._create_retriever()
        self.qa_chain = self._create_qa_chain()
        print(f"Chatbot initialized with language: {self.language}, jurisdiction: {self.jurisdiction}")

    def _create_retriever(self):
        filter_params = {"language": self.language}
        if self.jurisdiction != "All":
            filter_params["jurisdiction"] = self.jurisdiction.replace(" & ", "_")
        return self.vectorstore.as_retriever(
            search_kwargs={
                "filter": filter_params,
                "k": 5
            }
        )

    def update_language_and_jurisdiction(self, language: str, jurisdiction: str):
        self.language = "EN-GB" if language == "English" else "FR"
        self.jurisdiction = jurisdiction
        self.retriever = self._create_retriever()
        print(f"Chatbot updated with language: {self.language}, jurisdiction: {self.jurisdiction}")

    def _create_qa_chain(self):
        prompt_template = """You are a helpful AI legal advisor specializing in UK criminal law. 
        Use the following pieces of context to answer the question at the end. 
        If you don't know the answer, just say that you don't know, don't try to make up an answer. 
        If asked about multiple jurisdictions or if the jurisdiction is set to 'All', compare and contrast the information for different UK jurisdictions.
        Provide detailed explanations and examples when appropriate.
        Always maintain a polite and professional tone.
        
        Context: {context}
        
        Question: {question}
        Answer:"""

        PROMPT = PromptTemplate(
            template=prompt_template,
            input_variables=["context", "question"]
        )

        return LLMChain(llm=self.llm, prompt=PROMPT, verbose=True)

    def get_response(self, query: str, conversation_history: List[Dict[str, str]]) -> str:
        print(f"Processing query: {query}")
        
        docs = self.retriever.get_relevant_documents(query)
        context = "\n".join([doc.page_content for doc in docs])
        
        # Include recent conversation history in the context
        history_text = "\n".join([f"{msg['role']}: {msg['content']}" for msg in conversation_history[-3:]])
        context = f"{history_text}\n\n{context}"

        response = self.qa_chain.run(context=context, question=query)
        print(f"Raw response: {response}")
        
        # Translate response if the language is French
        if self.language == "FR":
            translated_response = self._translate_to_french(response)
            return translated_response
        return response

    def _translate_to_french(self, text: str) -> str:
        translation_prompt = f"Translate the following English text to French, maintaining the legal terminology and tone:\n\n{text}"
        translation = self.llm.predict(translation_prompt)
        return translation

    def _translate_to_english(self, text: str) -> str:
        translation_prompt = f"Translate the following French text to English, maintaining the legal terminology and tone:\n\n{text}"
        translation = self.llm.predict(translation_prompt)
        return translation

    def get_satisfaction_response(self, satisfied: bool) -> str:
        if satisfied:
            response = "I'm glad I could help. Is there anything else you'd like to know about criminal law?"
        else:
            response = "I apologize if my response wasn't satisfactory. Could you please provide more details or rephrase your question? I'll do my best to give you a more helpful answer."
        
        if self.language == "FR":
            return self._translate_to_french(response)
        return response

    def get_final_response(self) -> str:
        response = """Thank you for using our service. If you need further assistance or have more detailed questions about UK criminal law, please consider consulting with a legal professional. Here are some additional resources that might be helpful:

        1. https://www.gov.uk/browse/justice/rights-legal-system
        2. https://www.lawsociety.org.uk/public/for-public-visitors/common-legal-issues/criminal-law
        3. https://www.citizensadvice.org.uk/law-and-courts/criminal-law/

        Remember, this chatbot provides general information and should not be considered as formal legal advice."""
    
        if self.language == "FR":
            return self._translate_to_french(response)
        return response