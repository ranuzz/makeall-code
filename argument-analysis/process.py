import pickle
import os
import sys
import spacy
from transformers import pipeline
nlp = spacy.load("en_core_web_md")
classifier = pipeline('sentiment-analysis')

class CmvResult:

    def __init__(self):
        self.id = None
        self.cs_sim = [] # similarity with successful arguments
        self.cf_sim = [] # similarity with failed arguments
        self.cs_sent = [] # sentiment of successful arguments
        self.cf_sent = [] # sentiment of failed arguments

class CmvRow:

    def __init__(self):
        self.id = None
        self.title = None
        self.url = None
        self.view = None
        self.num_comments = 0
        self.num_counters = 0 # top level comments on post
        self.counters_success = []
        self.counters_failure = []

s_tot = 0
s_pos = 0
s_neg = 0
s_simi = 0

f_tot = 0
f_pos = 0
f_neg = 0
f_simi = 0

def print_stats():
    print("Success:: Avg. Simi. {0} - Pos({1}%) - Neg({2}%)".format(
        round((s_simi / s_tot), 2),
        round((s_pos / s_tot)*100, 2),
        round((s_neg / s_tot)*100, 2)
    ))
    print("Failure:: Avg. Simi. {0} - Pos({1}%) - Neg({2}%)".format(
        round((f_simi / f_tot), 2),
        round((f_pos / f_tot)*100, 2),
        round((f_neg / f_tot)*100, 2)
    ))

if __name__ == "__main__":

    pickle_file = 'data.pickle'
    result_file = 'result.pickle'

    cmvrs = []
    if os.path.exists(result_file):
        print("Reading pickled data\n")
        with open(result_file, 'rb') as f:
            # The protocol version used is detected automatically, so we do not
            # have to specify it.
            cmvrs = pickle.load(f)
        for c in cmvrs:
            mins = min(len(c.cs_sim), len(c.cs_sent))
            minf = min(len(c.cf_sim), len(c.cf_sent))
            s_tot += mins
            f_tot += minf

            for i in range(mins):
                s_simi += int(c.cs_sim[i]*100)
                if c.cs_sent[i][0]['label'] == 'NEGATIVE':
                    s_neg += 1
                else:
                    s_pos += 1
            
            for i in range(minf):
                f_simi += int(c.cf_sim[i]*100)
                if c.cf_sent[i][0]['label'] == 'NEGATIVE':
                    f_neg += 1
                else:
                    f_pos += 1

        print_stats()
        sys.exit(0)

    if os.path.exists(pickle_file):
        print("Reading pickled data\n")
        cmvs = []
        with open(pickle_file, 'rb') as f:
            # The protocol version used is detected automatically, so we do not
            # have to specify it.
            cmvs = pickle.load(f)
        #for c in cmvs:
        #    print("{0}: s: {1} f:{2}".format(c.id, len(c.counters_success), len(c.counters_failure)))
        for cmv_row in cmvs:
            print("{0}: s: {1} f:{2}".format(cmv_row.id, len(cmv_row.counters_success), len(cmv_row.counters_failure)))
            cmvr = CmvResult()
            cmvr.id = cmv_row.id
            view_doc = nlp(cmv_row.view)
            print("Processing Success")
            for cs in cmv_row.counters_success:
                csdoc = nlp(cs)
                sim = csdoc.similarity(view_doc)
                cmvr.cs_sim.append(sim)
                try:
                    sent = classifier(cs)
                    cmvr.cs_sent.append(sent)
                except:
                    print("Error : Classifier  CS")

            print("Processing Failure")
            for cf in cmv_row.counters_failure:
                cfdoc = nlp(cf)
                sim = cfdoc.similarity(view_doc)
                cmvr.cf_sim.append(sim)
                try:
                    sent = classifier(cf)
                    cmvr.cf_sent.append(sent)
                except:
                    print("Error : Classifier  CF")

            cmvrs.append(cmvr)

        with open(result_file, 'wb') as f:
            # Pickle the 'data' dictionary using the highest protocol available.
            pickle.dump(cmvrs, f, pickle.HIGHEST_PROTOCOL)   

        """
        for c in cmvrs:
            mins = min(len(c.cs_sim), len(c.cs_sent))
            minf = min(len(c.cf_sim), len(c.cf_sent))
            s_tot += mins
            f_tot += minf

            for i in range(mins):
                s_simi += int(c.cs_sim[i]*100)
                if c.cs_sent[0][i]['label'] == 'NEGATIVE':
                    s_neg += 1
                else:
                    s_pos += 1
            
            for i in range(minf):
                f_simi += int(c.cf_sent[i]*100)
                if c.cf_sent[0][i]['label'] == 'NEGATIVE':
                    f_neg += 1
                else:
                    f_pos += 1
        
        print_stats()
        """
    else:
        print("No data!!!!")