from multiprocessing.connection import Listener
import numpy as np
from allennlp.predictors.coref import CorefPredictor

class coref:

    def __init__(self):
        self.predictor = CorefPredictor.from_path(
            "https://s3-us-west-2.amazonaws.com/allennlp/models/coref-model-2018.02.05.tar.gz")

    def predict(self, document):
        return self.predictor.predict(document)

    def resolve(self, document):

        result = self.predict(document)
        doc = result['document']
        clusters = result["clusters"]

        doc_dict = {}
        for i in range(len(doc)):
            doc_dict[i] = doc[i]
        indices = []
        for i in range(len(clusters)):
            indices.append(clusters[i][0][1] - clusters[i][0][0])

        sort_indices = np.argsort(np.array(indices))

        for j in sort_indices:
            phrase = ' '.join(doc[clusters[j][0][0]:clusters[j][0][1] + 1])
            for mention in clusters[j]:
                for i in range(mention[0], mention[1] + 1):
                    doc_dict[i] = ''
                doc_dict[mention[0]] = phrase

        reg_doc = ''
        for i in range(len(doc)):
            if doc_dict[i] != '':
                if doc_dict[i] in ['.', ',']:
                    reg_doc = reg_doc + doc_dict[i]
                else:
                    reg_doc = reg_doc + ' ' + doc_dict[i]

        return reg_doc

def start_coref_daemon(port=6000):
    p2 = coref()
    address = ('localhost', port)     # family is deduced to be 'AF_INET'
    listener = Listener(address, authkey=b'secret password')

    while True:
        conn = listener.accept()
        print('connection accepted from', listener.last_accepted)
        msg = conn.recv()
        # do something with msg
        if msg == 'close':
            conn.close()
            break
        returnthis = p2.resolve(msg)
        # print(returnthis)
        conn.send(returnthis)

    listener.close()

if __name__ == '__main__':
    start_coref_daemon()
