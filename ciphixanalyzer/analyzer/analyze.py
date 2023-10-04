import spacy
import asent


def analyze(text):
    """Analyse tonality of passed text.
    :param text: text to be analysed
    :return: dictionary with analysed results
    """
    # load spacy pipeline for sentiment analysis: split to sentences and sentiment analysis
    nlp = spacy.blank('en')
    nlp.add_pipe('sentencizer')
    nlp.add_pipe('asent_en_v1')

    # run analysis process
    doc = nlp(text)

    return {
        'negative': doc._.polarity.negative,
        'neutral': doc._.polarity.neutral,
        'positive': doc._.polarity.positive,
        'compound': doc._.polarity.compound,
    }
