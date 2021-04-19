#-- 카카오 챗봇과 연동될 python flask 서버

from flask import Flask, render_template, request, url_for, g, send_file

from flask import current_app, session, redirect, Response, jsonify
from flask import stream_with_context, abort, flash, send_from_directory, make_response
from konlpy.tag         import Okt

app = Flask(__name__)

LOG = Log

# 환경설정
app.config.from_pyfile('chat.cfg' , silent=True)

gKakaoCtrl.Okt        = Okt()
gKakaoCtrl.qna        = {}

@app.errorhandler(404)
def not_found(error):
    Log.error("404 error=[%s]"%(error))
    return render_template('404.html'), 404

@app.errorhandler(500)
def server_error(error):
    Log.error("500 error=[%s]"%(error))
    return render_template('500.html', err_msg=error), 500

@app.route('/kakao/recommend', methods = ['POST', 'GET'])
def fn_kakao_recommend():
    debug_mode  = True
    answer  = ""
    params  = gUtil.request_params(request, "")
    Log.debug("Params = %s"%(params))
    inData  = gKakaoChat.getInfo( params )
    if debug_mode:Log.debug("fn_recommend  inData=%s"%( json.dumps( inData, indent=4, ensure_ascii=False) ) )
    user_id             = inData.get("user_id", u"" )
    user_friend_key     = inData.get("user_friend_key", u"" )
    utterance           = inData.get("utterance", u"?" )
    subject             = inData.get("subject", u"?" )

    qna     = utterance.replace("\n","")
    if qna.find("질문등록") == 0:
        with open( '/home/wizice/chat/www/data/qna.txt' , 'rb') as f:
            qna_data    = pickle.load(f)
        qna_data.append(gKakaoCtrl.qna)
        with open( '/home/wizice/chat/www/data/qna.txt' , 'wb') as f:
            pickle.dump(qna_data,f)
        answer = {
                    "version": "2.0",
                    "template": {
                        "outputs": [
                            {
                                "simpleText": {
                                    "text": "등록되었습니다"
                                }
                            }
                        ]
                    }
                }
         elif qna.find( "답변보기") == 0:
        #-- 디비에서 가져와서 답변
        idx = qna.split(',')[1]
        with open('/home/wizice/chat/www/data/qna.txt', 'rb') as f:
            data = pickle.load(f)
        res = data[int(idx)]
        answer = {
                    "version": "2.0",
                    "template": {
                        "outputs": [
                            {
                                "simpleText": {
                                    "text": res["answer"]
                                }
                            }
                        ]
                    }
                }
    else:
        answer  = {
                  "version": "2.0",
                  "template": {
                    "outputs": [
                      {
                        "carousel": {
                          "type": "basicCard",
                          "items": [
                              ]
                            }
                            }
                          ]
                        }
                      }
        new_nouns   = gKakaoCtrl.Okt.nouns( qna )
        gKakaoCtrl.qna   = { "question" : qna, "nouns" : new_nouns, "answer" : ""}
        Log.debug("fn_kakao_recommend qna= %s\n nouns=%s"%(qna, new_nouns))
        with open( '/home/wizice/chat/www/data/qna.txt', 'rb') as f:
            qna_list = pickle.load(f)
        rcd_qna = []
        for row in qna_list:
            qna_nouns = row["nouns"]
            if len(set(new_nouns) & set(qna_nouns)) >= 1:
                rcd_qna.append(row)
            idx = row["idx"] + 1
        for row in rcd_qna:
            answer_item =  {
                              "title": "유사질문",
                              "description": "",
                              "buttons": [
                                {
                                  "action": "message",
                                  "label": "답변보기",
                                  "messageText":""
                                }
                              ]
                            }
                                          ]
                            }
            answer_item["description"] = row["question"]
            answer_item["buttons"][0]["messageText"] = '답변보기,' + str(row["idx"])
            answer["template"]["outputs"][0]["carousel"]["items"].append(answer_item)

        answer_item =  {
                          "title": "질문등록",
                          "description": "질문을 등록하고 싶으면 클릭해주세요",
                          "buttons": [
                            {
                              "action": "message",
                              "label": "질문등록",
                              "messageText":"질문등록"
                            }
                          ]
                        }
        answer["template"]["outputs"][0]["carousel"]["items"].append(answer_item)
        gKakaoCtrl.qna["idx"] = idx
        with open( '/home/wizice/chat/www/data/qna.txt', 'wb') as f:
            pickle.dump( qna_list, f)
        Log.debug(answer)
    return jsonify( answer )
