from multiprocessing.connection import Client

def ner_test():
    address = ('localhost', 6000)
    try:
        conn = Client(address, authkey=b'secret password')
        conn.send("$test$")
        conn.recv()
        conn.close()
        return True
    except ConnectionRefusedError:
        print("Please start the ner daemon service before proceeding")
        return False

def ner(doc):
    '''
    This will try to ask the running daemon
    :param doc:
    :return:
    '''
    if not ner_test():
        return None
    address = ('localhost', 6000)
    conn = Client(address, authkey=b'secret password')
    conn.send(doc)
    msg = conn.recv()
    conn.close()
    return msg

if __name__ == '__main__':
    ss = ner("hello Brack")
    print(ss)