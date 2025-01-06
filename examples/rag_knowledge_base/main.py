"""RAG knowledge base builder using Firecrawl."""

import os
from typing import List, Dict, Any
import asyncio

import chromadb
import openai
from chromadb.config import Settings
from firecrawl import WebCrawler
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain.embeddings import OpenAIEmbeddings
from langchain.vectorstores import Chroma
from langchain.chains import RetrievalQA
from langchain.chat_models import ChatOpenAI

from config import (
    CRAWL_TARGETS,
    CHUNK_SIZE,
    CHUNK_OVERLAP,
    COLLECTION_NAME,
    PERSIST_DIRECTORY,
    EMBEDDING_MODEL,
    DEFAULT_QUERY_MODEL,
    MAX_TOKENS_PER_CHUNK,
)

class RAGKnowledgeBase:
    def __init__(self):
        """Initialize the RAG knowledge base."""
        self.crawler = WebCrawler()
        self.text_splitter = RecursiveCharacterTextSplitter(
            chunk_size=CHUNK_SIZE,
            chunk_overlap=CHUNK_OVERLAP,
            separators=["\n\n", "\n", " ", ""]
        )
        self.embeddings = OpenAIEmbeddings(model=EMBEDDING_MODEL)
        
        # Initialize vector store
        self.vectorstore = Chroma(
            persist_directory=PERSIST_DIRECTORY,
            embedding_function=self.embeddings,
            collection_name=COLLECTION_NAME
        )
        
        # Initialize LLM
        self.llm = ChatOpenAI(
            model_name=DEFAULT_QUERY_MODEL,
            temperature=0.7
        )
        
        # Initialize QA Chain
        self.qa_chain = RetrievalQA.from_chain_type(
            llm=self.llm,
            chain_type="stuff",
            retriever=self.vectorstore.as_retriever(
                search_kwargs={"k": 3}
            )
        )
        
    async def crawl_and_process(self, urls: List[str]) -> List[Dict[str, Any]]:
        """Crawl URLs and process content for RAG."""
        processed_documents = []
        
        for url in urls:
            try:
                # Crawl the URL
                result = await self.crawler.arun(url=url)
                
                if not result.markdown:
                    print(f"No content retrieved from {url}")
                    continue
                
                # Split text into chunks
                chunks = self.text_splitter.split_text(result.markdown)
                
                # Create documents with metadata
                processed_documents.extend([
                    {
                        "page_content": chunk,
                        "metadata": {
                            "source": url,
                            "chunk_index": i
                        }
                    }
                    for i, chunk in enumerate(chunks)
                ])
                
            except Exception as e:
                print(f"Error processing {url}: {str(e)}")
                continue
        
        return processed_documents
    
    async def update_knowledge_base(self, documents: List[Dict[str, Any]]):
        """Update the vector database with new documents."""
        try:
            # Add documents to vector store
            texts = [doc["page_content"] for doc in documents]
            metadatas = [doc["metadata"] for doc in documents]
            
            self.vectorstore.add_texts(
                texts=texts,
                metadatas=metadatas
            )
            
            # Persist the vector store
            self.vectorstore.persist()
            print(f"Successfully added {len(documents)} documents to the knowledge base")
            
        except Exception as e:
            print(f"Error updating knowledge base: {str(e)}")
    
    async def query(
        self,
        question: str,
    ) -> Dict[str, Any]:
        """Query the knowledge base."""
        try:
            # Get answer using QA chain
            result = await self.qa_chain.ainvoke({"query": question})
            
            # Get source documents
            source_documents = result.get("source_documents", [])
            sources = [doc.metadata["source"] for doc in source_documents]
            
            return {
                "answer": result["result"],
                "sources": list(set(sources))  # Remove duplicate sources
            }
            
        except Exception as e:
            print(f"Error querying knowledge base: {str(e)}")
            return {
                "answer": "Sorry, I encountered an error while trying to answer your question.",
                "sources": []
            }

async def main():
    """Main function to demonstrate the RAG knowledge base."""
    # Initialize the knowledge base
    kb = RAGKnowledgeBase()
    
    # Crawl and process documents
    print("Crawling and processing documents...")
    documents = await kb.crawl_and_process(CRAWL_TARGETS)
    
    if documents:
        # Update the knowledge base
        print("Updating knowledge base...")
        await kb.update_knowledge_base(documents)
        
        # Example queries
        questions = [
            "How do I use pandas DataFrame groupby function?",
            "What are the main data structures in Python?",
            "How do I create a NumPy array?"
        ]
        
        for question in questions:
            print(f"\nQuestion: {question}")
            result = await kb.query(question)
            print(f"Answer: {result['answer']}")
            print("Sources:")
            for source in result['sources']:
                print(f"- {source}")
    else:
        print("No documents were processed. Please check your crawl targets and try again.")

if __name__ == "__main__":
    asyncio.run(main())