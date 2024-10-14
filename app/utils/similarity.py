import tensorflow as tf
import tensorflow_hub as hub

#Chargement de google encodeur universel pré-entraîné
use_model = hub.load("https://tfhub.dev/google/universal-sentence-encoder/4")

def calculate_similarity(text1, text2):
    # Encode texts
    embeddings = use_model([text1, text2])
    
    # Calcul de similarité
    similarity = tf.tensordot(embeddings[0], embeddings[1], axes=1).numpy()
    
    return similarity