import nltk
from nltk.tokenize import word_tokenize
from nltk.corpus import stopwords
from nltk.stem import WordNetLemmatizer

nltk.download('punkt')
nltk.download('stopwords')
nltk.download('wordnet')
nltk.download('punkt_tab')

def preprocess_text(text):
    # Tokenisation
    tokens = word_tokenize(text.lower())
    
    # Supprimer les mots vides et la ponctuation
    stop_words = set(stopwords.words('french'))
    tokens = [token for token in tokens if token.isalnum() and token not in stop_words]
    
    # Lemmatisation
    lemmatizer = WordNetLemmatizer()
    lemmatized_tokens = [lemmatizer.lemmatize(token) for token in tokens]
    
    return ' '.join(lemmatized_tokens)