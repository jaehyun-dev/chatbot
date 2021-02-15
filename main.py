from konlpy.tag import Hannanum
from jaccard_similarity import Jaccard_similarity

hannanum = Hannanum()

m1 = '요소 기술로 자연어 분석, 이해, 생성 등이 있으며, 정보 검색, 기계 번역, 질의응답 등 다양한 분야에 응용된다.'
m2 = '머신 러닝 또는 기계 학습은 컴퓨터 과학 중 인공지능의 한 분야로, 패턴인식과 컴퓨터 학습 이론의 연구로부터 진화한 분야이다.'
m3 = '한국인이 사용하는 언어이며, 주로 한반도 전역과 제주도를 위시한 한반도 주변의 섬에서 사용한다.'

m1_nouns = hannanum.nouns(m1)
m2_nouns = hannanum.nouns(m2)
m3_nouns = hannanum.nouns(m3)

print( "m1 vs m2 ==> %s"%(Jaccard_similarity(m1_nouns, m2_nouns)))
print( "m1 vs m3 ==> %s"%(Jaccard_similarity(m1_nouns, m3_nouns)))
print( "m2 vs m3 ==> %s"%(Jaccard_similarity(m2_nouns, m3_nouns)))