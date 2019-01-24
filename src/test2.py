import pickle
spec_path = '/home/fkubota/Downloads/aaa.pkl'

with open(spec_path, mode='rb') as f:
    spec = pickle.load(f)

print(spec)