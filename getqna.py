#-- 온라인가나다 사이트에서 질문과 답변 데이터 가져와서 키워드를 추출하고 JSON데이터에 저장


import pickle
import requests
from bs4 import BeautifulSoup


def getqna():
    find_name   = re.compile('[가-힣]{2,4}[ ]*(?:작성)')
    qna_json    = []
    okt         = Okt()
    for i in range(1,10000):
        json_data   = {}
        url = 'https://www.korean.go.kr/front/onlineQna/onlineQnaView.do?mn_id=216&qna_seq=' + str(i)
        print(url)
        question    = ''
        content = requests.get(url)
        html = content.text
        soup = BeautifulSoup(html, 'html.parser')
        qheader = soup.select_one('#content > div.boardView > div:nth-of-type(1) > h2')
        qbody   = soup.select_one('#content > div.boardView > div:nth-of-type(2)')
        answer  = soup.select_one('#content > div.boardView > div:nth-of-type(4)')
        if answer:
            answer = answer.get_text()
        else:
            answer = ''
        name    = find_name.findall(answer)
        if name:
            answer  = answer.split(name[0])[0].replace('\n','').replace('\r','').replace('\t','')
        else:
            answer  = answer.replace('\n','').replace('\r','').replace('\t','')
        if qheader :
            qheader = qheader.get_text()
        if qbody:
            qbody   = qbody.get_text()
        else:
            continue
        question = qheader.replace('"','') + ' ' + qbody.replace('\n',' ').replace('\r',' ').replace('\t',' ').replace
        idx        = i -1
        nouns       = okt.nouns(question)
        json_data = {"question": question, "answer" : answer, "idx" : idx, "nouns" : nouns}
        qna_json.append(json_data)
    with open( '/home/wizice/qna/data/qna.txt' , 'wb') as f:
        pickle.dump(qna_json,f)
