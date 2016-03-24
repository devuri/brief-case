from textblob import TextBlob
import pandas as pd
from sklearn.feature_extraction.text import TfidfVectorizer


'''
Turning a case into a Panda's DataFrame For EDA and feature engineering.
'''


cols=['reference', 'text', 'length', 'percent_nouns', 'subjectivity', 'polarity', 'has_reason', \
'has_therefore', 'has_reject', 'has_applied', 'has_standard', 'has_fact', 'has_argue']


def cases_to_df(cases, references=None):
    '''
    Takes a list of cases that are each a string and returns them all as featurized sentences to train a model or predict upon
    '''
    df = pd.DataFrame(columns=cols)

    for case, reference in zip(cases, references):
        df = pd.concat((df, case_to_df(case, reference)))

    df = df.reset_index()
    df = df.drop('index', axis=1)

    # tfidf = TfidfVectorizer(stop_words='english', max_features=40)
    # vecs = tfidf.fit_transform(df['text'].values)
    # vecs_array = vecs.toarray()
    # tfidf_vocab = sorted(tfidf.vocabulary_.keys())
    # vocab_vecs = zip(tfidf_vocab, vecs_array.T)

    # for vocab, vec in vocab_vecs:
    #     # print vocab, vec.shape()
    #     df[vocab] = vec

    return df


def case_to_df(case, reference=None):
    '''
    Takes a case as a string and returns a case with featurized sentences that you can train a model or have a model predict upon.
    '''

    case_blob = TextBlob(case)
    sent_blobs = case_blob.sentences
    sent_strs = [str(sent) for sent in case_blob.sentences]


    references = [reference for _ in xrange(len(sent_strs))]
    ref_sents = zip(references, sent_strs)


    df = pd.DataFrame(ref_sents, columns=['reference', 'text'])

    df['length'] = df['text'].map(lambda sent: len(sent.split()))

    df['percent_nouns'] = [len(sent.noun_phrases) / float(len(sent.split())) for sent in sent_blobs]

    '''
    The sentiment property returns a named tuple of the form Sentiment(polarity, subjectivity).
    The polarity score is a float within the range [-1.0, 1.0].
    The subjectivity is a float within the range [0.0, 1.0] where 0.0 is very objective and 1.0 is very subjective.
    '''

    df['subjectivity'] = [sent.subjectivity for sent in sent_blobs]
    df['polarity'] = [sent.polarity for sent in sent_blobs]


    df['has_reason'] = df['text'].map(lambda sent: 1 if 'reason' in sent else 0)
    df['has_therefore'] = df['text'].map(lambda sent: 1 if 'therefore' in sent else 0)
    df['has_reject'] = df['text'].map(lambda sent: 1 if 'therefore' in sent else 0)
    df['has_applied'] = df['text'].map(lambda sent: 1 if 'applied' in sent else 0)
    df['has_standard'] = df['text'].map(lambda sent: 1 if 'standard' in sent else 0)
    df['has_fact'] = df['text'].map(lambda sent: 1 if 'fact' in sent else 0)
    df['has_argue'] = df['text'].map(lambda sent: 1 if 'argue' in sent else 0)

    return df

def df_to_csv(df, year):
    path = '../data/' + str(year) + '_justia_df.csv'
    df.to_csv(path_or_buf=path, sep='+')
    print "File was written to ", path


def custom_summarizer(case_df):
    pass
