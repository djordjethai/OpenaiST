# inmemory store
from langchain.embeddings.openai import OpenAIEmbeddings
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain.vectorstores.docarray.in_memory import DocArrayInMemorySearch
from langchain.document_loaders import TextLoader

documents = TextLoader("pravilnik.txt", encoding="utf-8").load()
text_splitter = RecursiveCharacterTextSplitter(chunk_size=500, chunk_overlap=0)
docs = text_splitter.split_documents(documents)

embeddings = OpenAIEmbeddings()

vectorstore = DocArrayInMemorySearch.from_documents(docs, embeddings)

retriever = vectorstore.as_retriever()

query = "ko ispostavlja fakture?"
docs1 = retriever.get_relevant_documents(query, k=2)

print(docs1)