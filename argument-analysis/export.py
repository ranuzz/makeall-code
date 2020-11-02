import os
import pickle

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

if __name__ == "__main__":

    pickle_file = 'data.pickle'
    if os.path.exists(pickle_file):
        print("Exporting sentences for toxicity analysis")
        cmvs = []
        with open(pickle_file, 'rb') as f:
            # The protocol version used is detected automatically, so we do not
            # have to specify it.
            cmvs = pickle.load(f)
        
        s_fp = open('success_sent.txt', 'w')
        f_fp = open('failure_sent.txt', 'w')

        replace = ["'", "\"", "\r\n", "\n", "\t", "`", ",", "\\", "<", ">", "*", "(", ")", "[removed]"]
        removed = 0
        totf = 0
        for c in cmvs:
            for s in c.counters_success:
                tmp = s.strip()
                for r in replace:
                    tmp = tmp.replace(r, " ")
                tmp = tmp.strip()
                if len(tmp) < 2:
                    continue
                s_fp.write("\"{}\",\n".format(tmp))
            for f in c.counters_failure:
                totf += 1
                tmp = f.strip()
                for r in replace:
                    tmp = tmp.replace(r, " ")
                tmp = tmp.strip()
                if len(tmp) < 2:
                    removed += 1
                    continue
                f_fp.write("\"{}\",\n".format(tmp))           
                
    print(removed, totf)

    s_fp.close()
    f_fp.close()