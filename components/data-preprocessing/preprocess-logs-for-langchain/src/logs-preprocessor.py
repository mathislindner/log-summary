#TODO: save the logs to a dataframe and then add them to a chroma db to be able to retrieve them easily
import argparse
import json
import os
import pandas as pd
from langchain.document_loaders import DirectoryLoader
from langchain.document_loaders.csv_loader import CSVLoader
from langchain.vectorstores import Chroma
from langchain.embeddings.sentence_transformer import HuggingFaceEmbeddings


#options is a list of strings that are the keys of the json file
def keep_only(json_log, options):
    hits = json_log["hits"]["hits"]
    columns_to_keep = []
    for hit in hits:
        source = hit["_source"]
        keep_only_dict = {}
        for option in options:
            keep_only_dict[option] = source[option]
        columns_to_keep.append(keep_only_dict)
    df = pd.DataFrame(columns_to_keep)
    #fix host column
    try:
        df["host"] = df["host"].apply(lambda x: x['hostname'])
    except:
        pass
    return df

def create_preprocessed_folder(raw_logs_path):
    preprocessed_logs_path = raw_logs_path.replace("raw", "preprocessed")
    os.makedirs(preprocessed_logs_path, exist_ok=True)
    return preprocessed_logs_path

def save_json_log_to_df(path_to_json_log):
    options = ["host", "message", "@timestamp"]
    #load the json file
    with open(path_to_json_log) as json_file:
        json_log = json.load(json_file)
    #keep only the message, server and time
    df_keep_only = keep_only(json_log, options)
    #convert the timestamp to datetime if empty logs just ignore
    try:
        #convert the timestamp to datetime
        df_keep_only["@timestamp"] = pd.to_datetime(df_keep_only["@timestamp"])
        #sort by timestamp
        df_keep_only = df_keep_only.sort_values(by=['@timestamp'])
    except KeyError:
        pass
    #save the json file in the preprocessed folder
    preprocessed_df_path = path_to_json_log.replace("raw", "preprocessed").replace(".json", ".csv")
    df_keep_only.to_csv(preprocessed_df_path, index=False)

def load_csv_as_langchain_docs(path_to_csvs):
    loader = DirectoryLoader(path_to_csvs, glob='**/*.csv', loader_cls=CSVLoader)
    documents = loader.load()
    return documents


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument("--log_path", help="path to the logs folder", required=True)
    args = parser.parse_args()

    #get the list of logs
    logs = os.listdir(args.log_path)
    #create the preprocessed folder
    preprocessed_logs_path = create_preprocessed_folder(args.log_path)

    #for each log
    for log in logs:
        #save the json log to a dataframe
        json_log_path = os.path.join(args.log_path, log)
        save_json_log_to_df(json_log_path)
        #save the dataframe in the preprocessed folder
    
    #TODO: for all the logs create embeddings for better retrieval
    #load csv as docs
    print(preprocessed_logs_path)
    docs = load_csv_as_langchain_docs(preprocessed_logs_path)
    #docs = [doc for doc in docs if doc!=None]

    #embedding_model = INSTRUCTOR(model_name="hkunlp/instructor-xl", device="cuda")
    #create the embedding function
    #sembedding_function = InstructorEmbeddingFunction(model=embedding_model)
    #embedding_function = InstructorEmbeddingFunction(model_name="hkunlp/instructor-xl", device="cuda")
    model_kwargs = {'device': 'cuda'}
    def_embedding_function = HuggingFaceEmbeddings(
                                                   model_name="all-MiniLM-L6-v2",
                                                   model_kwargs=model_kwargs
                                                   )

    db = Chroma.from_documents(docs, def_embedding_function, persist_directory="/data/preprocessed/chromadb")
    db.persist()
