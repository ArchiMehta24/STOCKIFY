#preprocess.py
import nltk
from nltk.tokenize import word_tokenize
from nltk.corpus import stopwords
from nltk.stem import WordNetLemmatizer

# Download necessary NLTK resources (only required once)
nltk.download('punkt')
nltk.download('stopwords')
nltk.download('wordnet')

# Initialize Lemmatizer
lemmatizer = WordNetLemmatizer()

def preprocess_text(text):
    """
    Preprocesses the given text by:
    1. Tokenizing
    2. Removing Stopwords
    3. Lemmatizing words
    Returns cleaned text.
    """
    # Tokenization
    tokens = word_tokenize(text.lower())  # Convert to lowercase and tokenize

    # Removing Stopwords
    stop_words = set(stopwords.words('english'))
    filtered_tokens = [word for word in tokens if word.isalnum() and word not in stop_words]

    # Lemmatization
    lemmatized_tokens = [lemmatizer.lemmatize(word) for word in filtered_tokens]

    # Join tokens back into a sentence
    cleaned_text = " ".join(lemmatized_tokens)
    
    return cleaned_text
