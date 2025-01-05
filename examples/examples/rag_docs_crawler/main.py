from firecrawl import Firecrawl
from langchain.vectorstores import Chroma
from langchain.embeddings import OpenAIEmbeddings
from langchain.chains import RetrievalQA
from langchain.chat_models import ChatOpenAI
import os

class RagDocsCrawler:
    def __init__(self, api_key):
        """Initialize the RAG docs crawler with firecrawl API key"""
        self.firecrawl = Firecrawl(api_key=api_key)
        self.embeddings = OpenAIEmbeddings()
        
    def crawl_documentation(self, root_url, max_pages=50):
        """Crawl documentation site and return structured markdown content"""
        print(f"Crawling documentation at {root_url}")
        
        # Use firecrawl to gather content recursively
        result = self.firecrawl.markdown_crawl(
            url=root_url,
            params={
                "max_pages": max_pages,
                "follow_links": True,
                "content_type": "documentation"
            }
        )
        
        return result

    def create_knowledge_base(self, docs):
        """Create a vector store from the crawled documentation"""
        # Convert markdown documents to text chunks
        texts = []
        sources = []
        
        for doc in docs:
            texts.append(doc['markdown'])
            sources.append(doc['metadata']['sourceURL'])
            
        # Create vector store
        vectorstore = Chroma.from_texts(
            texts=texts,
            embedding=self.embeddings,
            metadatas=[{"source": s} for s in sources]
        )
        
        return vectorstore

    def create_qa_chain(self, vectorstore, temperature=0):
        """Create a question-answering chain using the vector store"""
        # Initialize language model
        llm = ChatOpenAI(temperature=temperature)
        
        # Create retrieval chain
        qa_chain = RetrievalQA.from_chain_type(
            llm=llm,
            chain_type="stuff",
            retriever=vectorstore.as_retriever(),
            return_source_documents=True
        )
        
        return qa_chain

def main():
    # Initialize with your API keys
    firecrawl_api_key = os.getenv('FIRECRAWL_API_KEY')
    os.environ['OPENAI_API_KEY'] = os.getenv('OPENAI_API_KEY')
    
    # Create crawler instance
    crawler = RagDocsCrawler(api_key=firecrawl_api_key)
    
    # Crawl a documentation site
    docs = crawler.crawl_documentation("https://docs.example.com")
    
    # Create knowledge base
    vectorstore = crawler.create_knowledge_base(docs)
    
    # Create QA chain
    qa_chain = crawler.create_qa_chain(vectorstore)
    
    # Example question
    question = "How do I install the package?"
    result = qa_chain({"query": question})
    
    print("\nQuestion:", question)
    print("\nAnswer:", result["result"])
    print("\nSources:", [doc.metadata["source"] for doc in result["source_documents"]])

if __name__ == "__main__":
    main()