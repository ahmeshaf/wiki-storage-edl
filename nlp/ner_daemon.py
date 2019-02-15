from multiprocessing.connection import Listener
from allennlp.predictors.predictor import Predictor

class ner:

    def __init__(self):
        self.predictor = Predictor.from_path(
            "https://s3-us-west-2.amazonaws.com/allennlp/models/fine-grained-ner-model-elmo-2018.12.21.tar.gz")

    def predict(self, document):
        return self.predictor.predict(document)

    def entity2html(self, phrase, typ):
        if typ != None and typ != "":
            return '''<a type="%s">%s</a>''' %(typ, phrase)
        else:
            return phrase

    def ner_resolve(self, document):
        result = self.predict(document)
        tags = result['tags']
        print(tags)
        words = result['words']
        resolved_list = []
        span = []
        typ = None
        for word, tag in zip(words, tags):
            if tag == 'O'or str(tag).startswith('U'):
                if len(span) > 0:
                    resolved_list.append(self.entity2html(' '.join(span), typ))
                    span = []
                typ = tag[2:]
                resolved_list.append(self.entity2html(word, typ))
            else:
                typ = tag[2:]
                span.append(word)
        if len(span) > 0:
            resolved_list.append(self.entity2html(' '.join(span), typ))
        return '<p>%s</p>' % ' '.join(resolved_list)

def start_ner_daemon(port=6000):
    p2 = ner()
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
        returnthis = p2.ner_resolve(msg)
        print(returnthis)
        conn.send(returnthis)

    listener.close()

if __name__ == '__main__':
    start_ner_daemon()
