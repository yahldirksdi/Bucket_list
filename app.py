from flask import Flask, render_template, request, jsonify
from pymongo import MongoClient

client = MongoClient('mongodb://test:sparta@ac-6fty83g-shard-00-00.1q65sre.mongodb.net:27017,ac-6fty83g-shard-00-01.1q65sre.mongodb.net:27017,ac-6fty83g-shard-00-02.1q65sre.mongodb.net:27017/?ssl=true&replicaSet=atlas-10zzql-shard-0&authSource=admin&retryWrites=true&w=majority')
db = client.bucket_list

app = Flask(__name__)

@app.route('/')
def home():
   return render_template('index.html')

@app.route("/bucket", methods=["POST"])
def bucket_post():
    bucket_receive = request.form["bucket_give"]
    count = db.bucket.count_documents({})
    num = count + 1
    doc = {
        'num': num,
        'bucket': bucket_receive,
        'done': 0
    }
    db.bucket.insert_one(doc)
    return jsonify({'msg': 'data saved!'})

@app.route("/bucket/done", methods=["POST"])
def bucket_done():
    num_receive = request.form["num_give"]
    db.bucket.update_one(
        {'num': int(num_receive)},
        {'$set': {'done': 1}}
    )
    return jsonify({'msg': 'Done!'})

@app.route("/bucket/delete", methods=["POST"])
def bucket_delete():
    num_delete = request.form["num_delete"]
    db.bucket.delete_one(
        {'num': int(num_delete)}
    )
    return jsonify({'msg': 'delete done!'})

@app.route("/bucket", methods=["GET"])
def bucket_get():
    buckets_list = list(db.bucket.find({},{'_id':False}))
    return jsonify({'buckets':buckets_list})

if __name__ == '__main__':
   app.run('0.0.0.0', port=5000, debug=True)