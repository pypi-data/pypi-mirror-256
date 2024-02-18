import pandas as pd
import os
from tempocnn.classifier import TempoClassifier
from tempocnn.feature import read_features
import time

cnn_model = TempoClassifier('ismir2018')
root_audio_dir = '/media/bleu/bulkdata2/deeprhythmdata'


def estimate_tempo_cnn(audio_path, model):
    features = read_features(audio_path)
    bpm = model.estimate_tempo(features, interpolate=False)
    print(bpm)
    return bpm

df = pd.read_csv('bpm_partial.csv')

df['bpm_tempocnn_ismir'] = df['filename'].apply(lambda x:estimate_tempo_cnn(os.path.join(root_audio_dir, x), cnn_model))

df.to_csv('bpm_partial_ismir.csv')