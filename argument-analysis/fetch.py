import praw
import pickle
import os

CLIENT_ID = ''
CLIENT_SECRET = ''
USERNAME = ''
PASSWORD = ''
USERAGENT = ''

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

def print_discussion(comment_forest, depth):
    for i in range(len(comment_forest)):
        tabs = ''
        for j in range(depth):
            tabs += '--'
        print(tabs + comment_forest[i].body[:100] + '\n')
        if len(comment_forest[i].replies) != 0:
            print_discussion(comment_forest[i].replies, depth+1)

def run_sample(reddit):
    cmvs = []
    deltas = ['Δ', '!delta']
    for submission in reddit.subreddit("changemyview").top(limit=1000):
        print("subimission id: {0}".format(submission))
        #print(dir(submission))
        if submission.is_self:
            cmv = CmvRow()
            print("Title : {0}".format(submission.title))
            cmv.id = submission.id
            print("Link : {0}".format(submission.url))
            cmv.url = submission.url
            print("Text : {0}".format(submission.selftext))
            cmv.view = submission.selftext
            print("Comments : {0}".format(submission.num_comments))
            cmv.num_comments = submission.num_comments
            print("Author : {0}".format(submission.author))
            author = submission.author
            submission.comments.replace_more(limit=0)
            print("Total top level comments : {0}".format(len(submission.comments)))
            cmv.num_counters = len(submission.comments)
            for i in range(len(submission.comments)):
                if len(submission.comments[i].replies) >= 1:
                    print("Comment# {0} got {1} replies".format(i+1, len(submission.comments[i].replies)))
                    #print_discussion(submission.comments[i].replies, 0)
                    comment_forest = submission.comments[i].replies
                    delta = False
                    for k in range(len(comment_forest)):
                        if comment_forest[k].author == author:
                            print("Comment made by author {0}".format(comment_forest[k].body[:100]))
                            for d in deltas:
                                if d in comment_forest[k].body:
                                    delta = True
                                    break
                    if delta:
                        cmv.counters_success.append(str(submission.comments[i].body))
                    else:
                        cmv.counters_failure.append(str(submission.comments[i].body))    
                else:
                    cmv.counters_failure.append(str(submission.comments[i].body))
            cmvs.append(cmv)
    return cmvs

if __name__ == "__main__":

    pickle_file = 'data.pickle'

    if os.path.exists(pickle_file):
        print("Reading pickled data\n")
        cmvs = []
        with open(pickle_file, 'rb') as f:
            # The protocol version used is detected automatically, so we do not
            # have to specify it.
            cmvs = pickle.load(f)
        for c in cmvs:
            print("{0}: s: {1} f:{2}".format(c.id, len(c.counters_success), len(c.counters_failure)))
    else:
        print("Pickling data\n")
        reddit = praw.Reddit(client_id=CLIENT_ID, client_secret=CLIENT_SECRET,
                            password=PASSWORD, user_agent=USERAGENT,
                            username=USERNAME)
    
        cmvs = run_sample(reddit)
        with open(pickle_file, 'wb') as f:
            # Pickle the 'data' dictionary using the highest protocol available.
            pickle.dump(cmvs, f, pickle.HIGHEST_PROTOCOL)
