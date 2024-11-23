import streamlit as st
from PyPDF2 import PdfReader
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain.embeddings.openai import OpenAIEmbeddings
from langchain.vectorstores import FAISS
from langchain.llms import OpenAI
from langchain.chains.question_answering import load_qa_chain

# Steps
# 1. Read PDF file & Check the file is corretly readable
# 2. Split the PDF file into smaller chunks as GPT has limtied context
# 3. Create embeddings

def main():

    
    st.set_page_config(page_title="Review Resume ")                                   
    # Configuration of the webpage i.e. Title
    
    st.header("Ask questions about the Resume")                                              
    # Header text of the webpage

    pdffile = st.file_uploader("Upload your PDF file", type = "pdf")               
    # PDF file uploader

    if pdffile is not None:
        pdf_reader = PdfReader(pdffile)

        text = ""
        for page in pdf_reader.pages:
            text = page.extract_text() +text
        
        text_splitter = RecursiveCharacterTextSplitter(
            chunk_size = 1000,
            chunk_overlap = 200,
            length_function = len
        )
        chunks = text_splitter.split_text(text=text)
        
        # Create embeddings i.e. numberic value of text chunks
        embeddings = OpenAIEmbeddings()
        VectorStore = FAISS.from_texts(chunks, embedding=embeddings)
        
        query = st.text_input("Ask Me")

        if query:
            docs = VectorStore.similarity_search(query=query)

            llm = OpenAI()
            chain = load_qa_chain(llm=llm, chain_type="stuff")
            response = chain.run(input_documents = docs,question = query)
            st.write(response)

if __name__ == "__main__":
    main()