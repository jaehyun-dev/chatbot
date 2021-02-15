from krwordrank.sentence import summarize_with_sentences

stop = 0

test = "국어 질문있습니다."
st = ''
for r in range(len(test)):
    texts = test[r]
    texts = preprocessing(texts, b_idx)
    st += texts
texts = st.split('. ')
try:
    stopwords = {b_idx.split(' ')[0], b_idx.split(' ')[1]}
    keywords, sents = summarize_with_sentences(
                                            texts, 
                                            stopwords = stopwords,
                                            num_keywords=100, 
                                            num_keysents=10
                                            )
except ValueError:
    print('key가 없습니다.')
    print()
    continue
    
for word, r in sorted(keywords.items(), key=lambda x:x[1], reverse=True)[:7]:
    #print('%8s:\t%.4f' % (word, r))
    print('#%s' % word)
print()
if stop == 50:
    break