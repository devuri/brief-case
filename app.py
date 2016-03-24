from flask import Flask, request, render_template
from gensim.summarization import keywords, summarize
from scripts.keyword_helper import unique_by_stem
from sklearn.externals import joblib
import numpy as np
from scripts.casedf import case_to_df
from textblob import TextBlob



app = Flask(__name__)
complexity_rfc = joblib.load("scripts/pickles/rfc.pkl")


# home page
@app.route('/')
def index():
    return render_template('index.html')


# about page
@app.route('/about')
def about():
    return render_template('about.html')


# briefing a case
@app.route('/brief_case', methods=['POST'] )
def brief_case():
    original = request.form['case_text'].encode("utf8").decode("utf8")

    '''
    Classify sentences in text before passing to summarizers and keyword finders.
    '''

    # case_to_df(text)

    # complexity_rfc.fit(case_to_df(text))

    select_cols = ['length', 'percent_nouns', 'subjectivity', 'polarity', 'has_reason', 'has_therefore', 'has_reject', 'has_applied', 'has_standard', 'has_fact', 'has_argue']

    case_X = case_to_df(original)[select_cols]

    preds = np.array(complexity_rfc.predict(case_X), dtype=bool)

    selected_text = np.array(TextBlob(original).sentences)[preds]
    selected_text = ' '.join([sent.string for sent in selected_text])

    kwords_list = np.array(keywords(original, ratio=0.10, split=True))
    kwords = unique_by_stem(kwords_list)

    if len(summarize(selected_text, split=True)) < 3:
        summary_sents = summarize(selected_text, split=True)[:5]
    elif len(summarize(selected_text, split=True)) > 5:
        summary_sents = summarize(selected_text, split=True)[:5]
    else:
        summary_sents = summarize(selected_text, split=True)

    highlighted = []

    for summary_sent in summary_sents:
        for case_sent in summarize(original, ratio=1.00, split=True):
            if summary_sent[1: 6] in case_sent:
                highlighted.append([1, case_sent])
            else:
                highlighted.append([0, case_sent])


    if len(summarize(original, split=True)) > 5:
        gensim_summary_sents = summarize(original, split=True)[:5]
    else:
        gensim_summary_sents = summarize(original, split=True)

    # gensim_highlighted = []
    #
    # for gensim_summary_sent in gensim_summary_sents:
    #     for case_sent in summarize(original, ratio=1.00, split=True):
    #         if gensim_summary_sent[1: 6] in case_sent:
    #             gensim_highlighted.append([1, case_sent])
    #         else:
    #             gensim_highlighted.append([0, case_sent])



    # highlighted = [[0, '''Highlighted case will be here: %s The Indemnified Contributor must: a) promptly notify the Commercial Contributor to the maximum extent possible, whether at the expiration of the rights and licenses granted hereunder, each Recipient hereby assumes sole responsibility to secure any other intellectual property of third parties'''], [1, '''If you do at least six (6) months after the cause of action arose.'''], [1, '''Each party waives its rights to use it under the terms of any Contributor to the terms of this license.'''], [0, '''Do not use, modify, or distribute the Executable version does not cure such breach within thirty days after you make any Modifications that you may choose to grant more extensive warranty protection in exchange for a fee.'''], [1, '''You may Distribute a Modified Version must bear the fee.) "Freely Available" means that no fee is charged for the Work. If a Derived Work is distributed in conjunction with PHP by saying "Foo for PHP" instead of calling it "PHP Foo" or "phpfoo" 5.'''], [0, '''The PHP Group has the status `author-maintained' if the Electronic Distribution Mechanism to anyone other than such Participant's Contributor Version (or portions thereof).'''], [0, '''License, however, you must provide sufficient documentation as part of the Work as you received as to name you as the (new) Current Maintainer.'''], [0, '''If the Current Maintainer who has indicated in the Appendix below).'''], [1, '''Works" shall mean a computer program containing, or used to control the behavior of that component is constrained by the terms of, this License Agreement.'''], [0, '''ACCEPT CWI LICENSE AGREEMENT is between BeOpen.com ("BeOpen"), having an office at 1895 Preston White Drive, Reston, VA 20191 ("CNRI"), and the definitions are repeated for your use of the State of California, excluding conflict of law provisions.'''], [0, '''Nothing in this License.''']]


    return render_template('brief.html', kwords=kwords, summary_sents=summary_sents, gensim_summary_sents=gensim_summary_sents, highlighted=highlighted)

# ussc summaries
@app.route('/ussc')
def ussc():
    return render_template('ussc.html')

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8080, debug=True)
