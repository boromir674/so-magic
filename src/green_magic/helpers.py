from nltk.stem import PorterStemmer, WordNetLemmatizer
from nltk.tokenize import word_tokenize as nltk_tokenize
from legacy.definitions import grow_info, stop_words


def gen_values(extr_output):
    """
    Expects the content of a strain item's field. In other words the data contained in the specific dataframe column.
    :param extr_output: the content of a strain item's field
    :return: the values contained
    """
    if type(extr_output) == list:
        for i in extr_output:
            yield i
    elif type(extr_output) == str:
        yield extr_output
    else:  # dictionary like
        for k, v in extr_output.items():
            yield k, v


def extract_value(strain, field):
    if field == '_id':
        return strain.name
    if field in grow_info:
        return strain['grow_info'][field]
    else:
        return strain[field]


def get_normalizer(norm_type):
    """
    Returns a lambda function that acts as a normalizer for input words/tokens.\n
    :param norm_type: the normalizer type to "construct". Recommended 'lemmatize'. If type is not in the allowed types then does not normalize (lambda just forwards the input to output as it is)
    :type norm_type: {'stem', 'lemmatize'}
    :return: the lambda callable object to perform normalization
    :rtype: lambda
    """
    if norm_type == 'stem':
        stemmer = PorterStemmer()
        return lambda x: stemmer.stem(x)
    elif norm_type == 'lemmatize':
        lemmatizer = WordNetLemmatizer()
        return lambda x: lemmatizer.lemmatize(x)
    else:
        return lambda x: x


def generate_words(text_data, normalize='lemmatize', word_filter=True):
    """
    Given input text_data, a normalize 'command' and a stopwords filtering flag, generates a normalized, lowercased word/token provided that it passes the filter and that its length is bigger than 2 characters.\n
    :param text_data: the text from which to generate (i.e. doc['text'])
    :type text_data: str
    :param normalize: the type of normalization to perform. Recommended 'lemmatize'
    :type normalize: {'stem', 'lemmatize'}, else does not normalize
    :param word_filter: switch/flag to control stopwords filtering
    :type word_filter: boolean
    :return: the generated word/token
    :rtype: str
    """
    normalizer = get_normalizer(normalize)
    for word in (_.lower() for _ in nltk_tokenize(text_data)):
        if len(word) < 2:
            continue
        if word_filter and word in stop_words:
            continue
        yield normalizer(word)
