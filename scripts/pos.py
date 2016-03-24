'''
Part of speech methods analyzing cases.
'''


def percent_nouns(sent):
    '''Calculates percentage of nouns per TextBlob Sentence object in a case.'''
    return len(sent.noun_phrases) / float(len(sent.split()))



def pos_count(sent_class):
    '''
    Takes a list of tokenized sentences and returns a dictionary of part of speech tags and respective counts.
    '''
    pos = []

    for sent in sent_class:
        tags = []

        for tagged in sent.tags:
            tags.append(tagged[1])
    #         print tagged[1]
        pos.append(tags)

    flat_pos = [el for p in pos for el in p]

    most_common = Counter(flat_pos).most_common()

    return {key: (float(val) / len(flat_pos)) for key, val in most_common}


def compare_pos_count(analysis, other):
    '''
    Compares analysis vs other dictionaries based on the total counts for each part of speech.

    Prints out which sent class has more per POS tag.
    '''
    for key, val in analysis.iteritems():
        print "Analysis: %f -- Other: %f" %(analysis[key], other[key])
        if analysis[key] > other[key]:
            print "Analysis has more %s by %f" %(key, (analysis[key] - other[key]))
            print
        else:
            print "Not Analysis has more %s by %f" %(key, (other[key] - analysis[key]))
            print
