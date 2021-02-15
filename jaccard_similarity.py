def Jaccard_similarity( doc1, doc2):
    doc1 = set(doc1)
    doc2 = set(doc2)
    return len(doc1 & doc2) / len(doc1 | doc2)