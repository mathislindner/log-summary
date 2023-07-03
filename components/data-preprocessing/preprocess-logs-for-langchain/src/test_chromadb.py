from langchain.vectorstores import Chroma
from langchain.embeddings.sentence_transformer import HuggingFaceEmbeddings

embedding_function = HuggingFaceEmbeddings(
                                            model_name="all-MiniLM-L6-v2",
                                            model_kwargs={'device': 'cuda'}
                                            )
db_path = "/data/preprocessed/chromadb"


#load chroma db
chroma_db = Chroma(persist_directory=db_path, embedding_function=embedding_function)

test_query = f"host"

#query the db
results = chroma_db.similarity_search(test_query, k=500)

for result in results:
    print(result)