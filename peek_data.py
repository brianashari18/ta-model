import pickle
with open('./processed/master_preprocessed.pkl', 'rb') as f:
    data = pickle.load(f)
print("CLASS NAMES:", data['label_encoder_classes'])
# show an example
seqs = data['data']['raw_audio__chromagram']['sequences']
print("SEQS len:", len(seqs))
print("Y example:", seqs[0]['y'][:10])
