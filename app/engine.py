import os
import shutil
import tempfile
from langchain.document_loaders import PyPDFLoader
from langchain_huggingface import HuggingFaceEmbeddings
from langchain.chains import RetrievalQA
from langchain.prompts import PromptTemplate
from langchain.text_splitter import RecursiveCharacterTextSplitter
from huggingface_hub import login 
from typing import List, Optional
from fastapi import UploadFile
from langchain_community.vectorstores import Chroma
from transformers import pipeline
from langchain_community.llms import HuggingFacePipeline
from dotenv import load_dotenv
load_dotenv()


# Important requirments
HF_TOKEN = os.getenv("HF_TOKEN")
PERSIST_DIRECTORY = os.getenv("PERSIST_DIRECTORY", "chroma_db") 
EMBEDDING_MODEL = os.getenv("EMBEDDING_MODEL", "sentence-transformers/all-MiniLM-L6-v2")    
LLM_MODEL = os.getenv("LLM_MODEL", "google/flan-t5-base")

# Login to Hugging Face 
if HF_TOKEN:
    login(token=HF_TOKEN)


class RetrievalEngine:
    def __init__(self):
        self.vector_store = None
        self.persist_directory = PERSIST_DIRECTORY

        # ✅ Use FLAN-T5 for generation
        generator = pipeline(
            "text2text-generation",
            model=LLM_MODEL,
            device_map="auto",
            max_new_tokens=450,
            truncation=True,          # force truncate long inputs
            model_kwargs={"max_length": 512}  # ensure <=512 tokens
        )

        self.llm = HuggingFacePipeline(pipeline=generator)
        self.embeddings = HuggingFaceEmbeddings(
            model_name=EMBEDDING_MODEL
        )
        if os.path.exists(self.persist_directory):
            self.vector_store = Chroma(
                persist_directory=self.persist_directory,
                embedding_function=self.embeddings
            )

    def ingest(self, files: List[UploadFile], replace: Optional[bool] = False):
        if replace:
            # reset vector db
            self.vector_store = None
            if os.path.exists(self.persist_directory):
                import shutil
                shutil.rmtree(self.persist_directory)

        documents = []
        for file in files:
            if file.filename.endswith(".pdf"):
                tmp_path = os.path.join(tempfile.gettempdir(), file.filename)

                with open(tmp_path, "wb") as f:
                    f.write(file.file.read())

                loader = PyPDFLoader(tmp_path)
                docs = loader.load()

                # ✅Manageing the chunk size
                splitter = RecursiveCharacterTextSplitter(
                    chunk_size=400,
                    chunk_overlap=50
                )

                chunks = splitter.split_documents(docs)
                documents.extend(chunks)
                os.remove(tmp_path)
            else:
                continue

        # ✅ Store in Chroma vector store (persistent)
        if not self.vector_store:
            self.vector_store = Chroma.from_documents(
                documents,
                embedding=self.embeddings,
                persist_directory=self.persist_directory
            )
        else:
            self.vector_store.add_documents(documents)
            
        return {"message": f"Ingested {len(documents)} chunks and saved to Chroma DB."}
    
    def retrieve(self, question: str, k: int = 3):
        if not self.vector_store:
            return {"error": "No vector store found. Please ingest documents first."}
        
        prompt_template = (
        "Answer the question using ONLY the provided context. "
        "If the answer is not in the context, say 'I don't know.'\n\n"
        "Context:\n{context}\n\nQuestion: {question}\nAnswer:"
        )
        prompt = PromptTemplate(
            input_variables=["context", "question"],
            template=prompt_template,
        )

        retrieval_qa = RetrievalQA.from_chain_type(
            llm=self.llm,
            chain_type="stuff",
            retriever=self.vector_store.as_retriever(search_kwargs={"k": k}),
            return_source_documents=True,
            chain_type_kwargs={"prompt": prompt}
        )
        # retrieval_qa = RetrievalQA.from_chain_type(
        #     llm=self.llm,
        #     chain_type="stuff",
        #     retriever=self.vector_store.as_retriever(search_kwargs={"k": k}),
        #     return_source_documents=True 
        # )
        print(f"Retrieving answer for question: {question}")
        if not question.strip():
            return {"error": "Question cannot be empty."}
        if len(question.split()) > 50:
            return {"error": "Question is too long. Please limit to 50 words."}
        result = retrieval_qa.invoke({"query": question})

        # Extract answer and sources
        answer = result.get("result", "")
        sources = []
        for doc in result.get("source_documents", []):
            sources.append({
                "content": doc.page_content,
                "metadata": doc.metadata
            })

        return {
            "answer": answer,
            "sources": sources
        }

    def reset(self):
        self.vector_store = None
        return {"message": "Engine reset successfully."}
