from tempocnn.classifier import TempoClassifier
from tempocnn.feature import read_features
import pandas as pd
import os
import time
print('reading')
songs = pd.read_csv('/media/bleu/bulkdata2/deeprhythmdata/test.csv')
print(songs)
# Extract the 'filename' column from the dataframe 'songs' and convert it to a list
filenames = songs['filename'].tolist()
bpms = songs['bpm'].tolist()

print(len(filenames))
# Prepend the directory path to each filename in the list
filenames = [os.path.join('/media/bleu/bulkdata2/deeprhythmdata', filename )for filename in filenames]


print(filenames[0])
model_name = 'shallowtemp'
classifier = TempoClassifier(model_name)
start = time.time()
for filename, bpm in zip(filenames, bpms):
    features = read_features(filename)
    # estimate the global tempo
    tempo = classifier.estimate_tempo(features, interpolate=False)
    print(f"{bpm} === {tempo}")
print(f'Total time = {time.time()-start:.3f}')






input_file = 'some_audio_file.mp3'

# initialize the model (may be re-used for multiple files)


# read the file's features
