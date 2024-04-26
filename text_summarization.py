import nltk
from nltk.tokenize import sent_tokenize, word_tokenize
from nltk.corpus import stopwords
from nltk.stem import WordNetLemmatizer
from sklearn.feature_extraction.text import TfidfVectorizer

#     nltk.download('wordnet')

def extractive_summarization(text, num_sentences=5):
    # Tokenize the text into sentences
    sentences = sent_tokenize(text)

    # Tokenize each sentence into words and remove stopwords
    stop_words = set(stopwords.words('english'))
    tokenized_sentences = [word_tokenize(sentence.lower()) for sentence in sentences]
    filtered_sentences = [[word for word in words if word not in stop_words] for words in tokenized_sentences]

    # Lemmatize the words
    lemmatizer = WordNetLemmatizer()
    lemmatized_sentences = [[lemmatizer.lemmatize(word) for word in words] for words in filtered_sentences]

    # Join the lemmatized words back into sentences
    preprocessed_sentences = [' '.join(words) for words in lemmatized_sentences]

    # Calculate TF-IDF scores
    tfidf_vectorizer = TfidfVectorizer()
    tfidf_matrix = tfidf_vectorizer.fit_transform(preprocessed_sentences)

    # Get the average TF-IDF score for each sentence
    avg_tfidf_scores = tfidf_matrix.mean(axis=1).flatten().tolist()[0]

    # Sort sentences by their average TF-IDF scores
    ranked_sentences = sorted(zip(sentences, avg_tfidf_scores), key=lambda x: x[1], reverse=True)

    # Select the top N sentences as the summary
    summary_sentences = [sentence for sentence, score in ranked_sentences[:num_sentences]]

    return ' '.join(summary_sentences)
