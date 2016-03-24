from sklearn.metrics import confusion_matrix
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns


'''
sklearn's confusion matrix is:

             predicted
              -     +
acutal  + #[ 'TN', 'FP' ],
        - #[ 'FN', 'TP' ]

Use this to prove it:

acts =   [0, 1, 1, 1, 0, 0]
result = [1, 0, 1, 1, 1, 1]

sklearn.metrics.confusion_matrix(acts, result)

TN = 0, FP = 3
FN = 1, TP = 2
'''

def easy_cf(actuals, predicted):
    cf_matrix = confusion_matrix(actuals, predicted)

    '''
    true positive (TP); eqv. with hit
    false positive (FP); eqv. with false alarm, Type I error
    true negative (TN); eqv. with correct rejection
    false negative (FN); eqv. with miss, Type II error
    '''

    tn = cf_matrix[0, 0]
    fn = cf_matrix[1, 0]
    tp = cf_matrix[1, 1] ####
    fp = cf_matrix[0, 1]
    total = len(actuals)

    pred_pos = tp + fp
    pred_neg = tn + fn

    act_pos = tp + fn
    act_neg = tn + fp

    accuracy = (tp + tn) / float(total)

    if pred_pos == 0:
        recall = "No predicted +"
        precision = "No predicted +"
    else:
        '''
        Recall, or sensitivity (true positive rate), quantifies the avoiding of false negatives.
        '''
        recall = float(tp)/act_pos

        '''
        Precision, or positive predictive value (PPV).
        If my test predicts positive, how certain can I be that it is a true positive?
        '''
        precision = float(tp)/pred_pos


    if pred_neg == 0:
        specificity = "No predicted -"
    else:
        '''
        Specificity, or true negative rate, quantifies the avoiding of false positives.
        '''
        specificity = float(tn)/act_neg


    print "True Positive is:", tp
    print "False Positive is:", fp
    print "True Negative is:", tn
    print "False Negative is:", fn
    print

    print "Predicting + and - correctly"
    print "Acccuracy:", accuracy
    print

    print "How much can I count on my + prediction?"
    print "Precision:", precision
    print

    print "Capturing actual + and avoiding FN"
    print "Sensitivity / Hit Rate / Recall:", recall
    print

    print "Capturing actual - and avoiding FP"
    print "Specificity / True Negative Rate:", specificity
    print


def feat_importance(rfc_model, X_test):
    importances = rfc_model.feature_importances_
    std = np.std([tree.feature_importances_ for tree in rfc_model.estimators_],
                 axis=0)
    indices = np.argsort(importances)[::-1]

    columns = np.array([   'length', 'percent_nouns',
        'subjectivity',      'polarity',    'has_reason', 'has_therefore',
          'has_reject',   'has_applied',  'has_standard',      'has_fact',
           'has_argue',           'act',        'action',       'appeals',
                'case',         'cases',    'certiorari',       'circuit',
               'claim',        'claims',         'court',        'courts',
                 'did',      'district',          'does',      'evidence',
             'federal',         'filed',       'general',          'held',
         'information',        'joined',      'judgment',          'jury',
                 'law',         'legal',          'make',      'official',
             'opinion',    'petitioner',   'petitioners',            'pp',
         'respondents',          'rule',          'site',         'state',
              'states',       'supreme',           'tax',         'trial',
              'united'])

    col_importance = columns[indices]


    # Print the feature ranking
    print("Feature ranking:")

    for f in range(X_test.shape[1]):
        print("%d. feature %d: %s (%f) " % (f + 1, indices[f], col_importance[f], importances[indices[f]]))

    # Plot the feature importances of the forest
    plt.figure(num=None, figsize=(20, 6), dpi=80, facecolor='w', edgecolor='k')
    plt.title("Feature importances")
    plt.bar(range(X_test.shape[1]), importances[indices],
           color="r", yerr=std[indices], align="center")
    plt.xticks(range(X_test.shape[1]), indices)
    plt.xlim([-1, X_test.shape[1]])
    plt.show()

    #Plot feature importances of the forest in seaborn
    sns.set_style("whitegrid")
