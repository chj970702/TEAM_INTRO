
import requests
import certifi
from pymongo import MongoClient
from flask import Flask, render_template, request, jsonify
import requests

app = Flask(__name__)
ca = certifi.where()


# 방명록 데이터베이스 연결
client = MongoClient(
    'mongodb+srv://sparta:test@cluster0.yqy4sb9.mongodb.net/?retryWrites=true&w=majority')
# 멤버 소개 데이터베이스 연결
client2 = MongoClient(
    'mongodb+srv://sparta:test@cluster0.oscsxtu.mongodb.net/?retryWrites=true&w=majority')
# 멤버 개인 댓글 데이터베이스 연결
client3 = MongoClient(
    'mongodb+srv://sepang:test@cluster0.ageawzb.mongodb.net/?retryWrites=true&w=majority')


client2 = MongoClient(
    'mongodb+srv://sparta:test@cluster0.oscsxtu.mongodb.net/?retryWrites=true&w=majority')
db = client.dbsparta
db2 = client2.dbsparta
db3 = client3.dbsparta

# 홈화면
@app.route('/')
def home():
    return render_template('index.html')

### --- 멤버 소개 서버 구성 --- ###


@app.route('/member_card')
def member_card():
    return render_template('member_card.html')


@app.route("/member_detail/<id>")
def member_detail(id):

    memberDetail = list(db2.member_detail.find({"image_num": id}))[0]
    print(memberDetail)
    detail = memberDetail["details"]
    name = memberDetail["name"]
    number = memberDetail["image_num"]

    return render_template("member_detail.html", detail=detail, name=name, number=number)


@app.route("/member_detail", methods=["GET"])
def card_get():
    all_card = list(db2.member_detail.find({}, {'_id': False}))
    return jsonify({'result': all_card})

### --- 멤버 소개 서버 구성 --- ###


### --- 방명록 서버 구성 --- ###

@app.route('/visit_comment')
def visit_comment():
    return render_template('visit_comment.html')


@app.route("/visit_comment", methods=["POST"])
def guest_post():

    name_receive = request.form['name_give']
    comment_receive = request.form['comment_give']
    time_receive = request.form['time_give']
    password_receive = request.form['password_give']

    doc = {
        'name': name_receive,
        'comment': comment_receive,
        'time': time_receive,
        'password': password_receive
    }
    db.visit_comment.insert_one(doc)
    return jsonify({'msg': '방명록 작성 완료'})


@app.route("/visit_comment_delete", methods=["POST"])
def guest_post_delete():

    name_receive = request.form['name_give']
    comment_receive = request.form['comment_give']
    time_receive = request.form['time_give']
    password_receive = request.form['pwd_give']

    doc = {
        'name': name_receive,
        'comment': comment_receive,
        'time': time_receive,
        'password': password_receive
    }
    db.visit_comment.delete_one(doc)
    return jsonify({'msg': '방명록 삭제완료'})


@app.route("/get_comment", methods=["GET"])
def guest_get():
    all_comment = list(db.visit_comment.find({}, {'_id': False}))
    return jsonify({'result': all_comment})

### --- 방명록 서버 구성 --- ###

### --- 멤버 댓글 서버 구성 --- ###


@app.route("/guestbook", methods=["POST"])
def guestbook_post():
    name_receive = request.form['name_give']
    comment_receive = request.form['comment_give']
    doc = {
        'name': name_receive,
        'comment': comment_receive
    }
    db.users.insert_one(doc)
    return jsonify({'msg': '저장 완료 !'})


@app.route("/guestbook", methods=["GET"])
def guestbook_get():
    all_comments = list(db.users.find({}, {'_id': False}))
    return jsonify({'result': all_comments})
### --- 멤버 댓글 서버 구성 --- ###


if __name__ == '__main__':
    app.run('0.0.0.0', port=5001, debug=True)
