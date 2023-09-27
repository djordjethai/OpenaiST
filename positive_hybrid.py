import os
from langchain.retrievers import PineconeHybridSearchRetriever
import pinecone

api_key = os.getenv("PINECONE_API_KEY_POS") 
env = os.getenv("PINECONE_ENVIRONMENT_POS")
openai_api_key = os.environ.get("OPENAI_API_KEY")

index_name = "positive-hybrid"

pinecone.init(api_key=api_key, environment=env)
#pinecone.whoami()
index = pinecone.Index(index_name)
from langchain.embeddings import OpenAIEmbeddings

embeddings = OpenAIEmbeddings()
from pinecone_text.sparse import BM25Encoder

# create the index
def create_hybrid():
    pinecone.create_index(
        name=index,
        dimension=1536,  # dimensionality of dense model
        metric="dotproduct",  # sparse values supported only for dotproduct
        pod_type="s1",
        metadata_config={"indexed": []},  # see explaination above
    )


# upsert data
bm25_encoder = BM25Encoder().default()
# corpus = ["football", "basketball", "worldly", "hello World"]
#     # fit tf-idf values on your corpus
# bm25_encoder.fit(corpus)



# for element in corpus:
#         sparse_vector = bm25_encoder.encode_documents(element)
#         non_zero_count = sum(1 for value in sparse_vector if value != 0)
#         print("Number of non-zero values in the sparse vector:", non_zero_count)


#     # store the values to a json file
# bm25_encoder.dump("bm25_values.json")
# # load to your BM25Encoder object
# bm25_encoder = BM25Encoder().load("bm25_values.json")


# retreive data


retriever = PineconeHybridSearchRetriever(
    embeddings=embeddings, sparse_encoder=bm25_encoder, index=index
)
# retriever.add_texts(["foo", "bar", "world", "hello"]) # it is possible to add data in this stage as well
print(" ")
pitanje = input("Unesite pitanje: ")
print(" ")
result = retriever.get_relevant_documents(pitanje)
print(result[0].page_content)
print(" ")

########
# pretraga index self-query na osnovu meta data je definisan u stapps pages pisi u stilu positive
#######
