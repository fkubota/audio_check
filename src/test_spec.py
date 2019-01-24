import pickle
import numpy as np

spec_path = '/home/fkubota/Python/app/audio_check/data/fromHoshinosan/sample_for_testing01_20181214_113823_002301-002317_right_ssft.pkl'


with open(spec_path, mode='rb') as f:
    spec = pickle.load(f).T

print(spec.shape)
print(type(spec))




