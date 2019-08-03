import numpy

def computePWMD(doc0, doc1, tau):

    wset0 = set([tok.text.strip() for tok in flatten(doc0)])
    wset1 = set([tok.text.strip() for tok in flatten(doc1)])

    words = list(wset0.union(wset1))
    words = [w for w in words if len(w) > 0]
    numwords = len(words)
    
    if numwords == 0:
        return 0
    
    x0 = numpy.zeros(numwords)
    x1 = numpy.zeros(numwords)
    
    for i in range(len(doc0)):
        for w in doc0[i]:
            if len(w.text.strip()) > 0:
                x0[words.index(w.text.strip())] += numpy.power(1.0/(1.0+i), tau)

    for i in range(len(doc1)):
        for w in doc1[i]:
            if len(w.text.strip()) > 0:
                x1[words.index(w.text.strip())] += numpy.power(1.0/(1.0+i), tau)

    normalize(x0.reshape(1, -1), norm='l1', copy=False)
    normalize(x1.reshape(1, -1), norm='l1', copy=False)
    
    W_ = [nlp(w).vector for w in words]
    D_ = euclidean_distances(W_)
    D_ = D_.astype(numpy.double)
    
    return emd(x0, x1, D_.copy(order='C'))