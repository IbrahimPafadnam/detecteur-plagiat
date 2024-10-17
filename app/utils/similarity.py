#import tensorflow as tf
#import tensorflow_hub as hub

#Chargement de google encodeur universel pré-entraîné
#use_model = hub.load("https://tfhub.dev/google/universal-sentence-encoder/4")

#def calculate_similarity(text1, text2):
    # Encode texts
    #embeddings = use_model([text1, text2])
    
    # Calcul de similarité
    #similarity = tf.tensordot(embeddings[0], embeddings[1], axes=1).numpy()
    
    #return similarity



from sentence_transformers import SentenceTransformer
from scipy.spatial.distance import cosine

# Charger un modèle plus léger, comme paraphrase-MiniLM-L6-v2
model = SentenceTransformer('sentence-transformers/paraphrase-MiniLM-L6-v2')

def calculate_similarity(text1, text2):
    # Encode les textes en vecteurs
    embeddings = model.encode([text1, text2])

    # Calcul de la similarité cosinus entre les deux vecteurs
    similarity = 1 - cosine(embeddings[0], embeddings[1])

    return similarity
