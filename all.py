import os
import json

path = 'imgs'

files = [{file: os.path.join(path, file)} for file in os.listdir(path)]

with open('data.json', 'w') as f:
    json.dump(files, f)
