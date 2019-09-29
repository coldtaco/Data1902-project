import nltk
from nltk.stem import WordNetLemmatizer
from nltk.corpus import wordnet

lemmatizer = WordNetLemmatizer()
nltk.download('punkt')
nltk.download('averaged_perceptron_tagger')
def wordnetTag(nltk_tag):
    if nltk_tag[0] == ('J'):
        return wordnet.ADJ
    elif nltk_tag[0] == ('V'):
        return wordnet.VERB
    elif nltk_tag[0] == ('N'):
        return wordnet.NOUN
    elif nltk_tag[0] == ('R'):
        return wordnet.ADV
    else:
        return None

#covert word into suitable form
def lemmaS(text):
    paragraph = []
    for line in text:
        nltk_tagged = nltk.pos_tag(nltk.word_tokenize(line))
        lemmatized_sentence = []
        for word, tag in nltk_tagged:
            tag = wordnetTag(tag)
            if tag is None:
                lemmatized_sentence.append(word)
            else:
                lemmatized_sentence.append(lemmatizer.lemmatize(word, tag))
        paragraph.append(" ".join(lemmatized_sentence))
    return paragraph
