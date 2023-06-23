import langchain
import os
from langchain.document_loaders import DirectoryLoader, TextLoader

loader = DirectoryLoader(DRIVE_FOLDER, glob='**/*.json', show_progress=True, loader_cls=TextLoader)