from gensim.models import Word2Vec, Doc2Vec
from sklearn.cluster import KMeans
import pandas as pd
import nltk.data
from sklearn.feature_extraction.text import TfidfVectorizer
from gensim.models.doc2vec import LabeledSentence
from textblob import TextBlob


def case_html_to_sent_tokens(case_html):
    '''
    Parses and converts an entire case html page to a list of tokenized sentences.

    The output tokenized sentences are Wordlist objects from TextBlob.
    '''
    sentences = []

    for para in case_html.findAll('p'):
        para = para.text.encode("utf8")
        para = para.decode("utf8")
        para = TextBlob(para)
        sents = para.sentences

        for sent in sents:
            sentences.append(sent.words)

    return sentences




# def case_to_sents(case):
#     paras = case.split('\n')
#
#     sents = case.split('  ')
#
#     tokenizer = nltk.data.load('tokenizers/punkt/english.pickle')
#     token_sents = '\n**\n'.join(tokenizer.tokenize(case))
#
#     sents_as_strs = token_sents.split('\n**\n')
#
#     def sent_list_gen(sent_strings):
#         for sent in sent_strings:
#             sent = sent.split('\n')
#             for word in sent:
#                 yield word
#
#     sents_generator = sent_list_gen(sents_as_strs)
#
#     return [sent.split(' ') for sent in sents_generator]

def case_to_sents(case):
    '''
    Takes a case a string and returns each sentence of the case as a blob.
    TextBlob's Sentence objects have the same properties and methods as TextBlobs and regular Python strings.
    '''
    case_blob = TextBlob(case)
    return case_blob.sentences


def case_to_word_list(case):
    '''Takes a case a string and returns TextBlob Wordlists objects for each sentence'''
    case_blob = TextBlob(case)
    return [sent.words for sent in case_blob.sentences]


def classify_sents_in_case(case, labels):
    return zip(case_to_sents(case), labels)


def label_sent(case_num, sent_num, sent_vec):
    return LabeledSentence(sent_vec, (["CASE_" + str(case_num) + "_SENT_" + str(sent_num)]))


def case_to_sentvecs(case_num, raw_case):
    sent_vecs = []

    case = case_to_sents(raw_case)

    for sent_num, sent_vec in enumerate(case):
        sent_vecs.append(label_sent(case_num, sent_num, sent_vec))

    return sent_vecs


def case_spreadsheet(case):
    '''
    Input:
        case_as_sents - a list of lists; each nested list is a sentence split into individual words

    Output:
        human readable form of the case where each sentence is separated by a newline
    '''

    for i, sent in enumerate(case_to_sents(case)):
    #     print str(i+1) + "::  "+ ' '.join(sent)
    #     print

        print " ".join(sent)


if __name__ == '__main__':
    # cases = pd.read_csv('../data/2006_justia.csv', delimiter='|')
    # first = cases.ix[0]['opinion']
    # case_vec = case_to_sentvecs(1, first)
    pass
