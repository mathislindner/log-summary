import langchain
from langchain.document_loaders import DirectoryLoader, TextLoader
import argparse

def get_loader():
    alarms_json_by_receiver = os.path.join('/data', 'raw', 'alarms', 'by_receiver')
    loader = DirectoryLoader(alarms_json_by_receiver, glob='**/*.json', show_progress=True, loader_cls=TextLoader)
    return loader



if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    args = parser.parse_args()

    loader = get_loader()