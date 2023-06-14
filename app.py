from flask import Flask, redirect, url_for, render_template, request, make_response, session
from flask_session import Session
from scripts import db

import secrets
import json

db = db.OPERATIONS()

app = Flask(__name__)

app.config['SECRET_KEY'] = secrets.token_hex()

# --- Update the following: --- #
app.config['SESSION_TYPE'] = 'mongodb'
app.config['SESSION_MONGODB'] = db.client
app.config['SESSION_MONGODB_DB'] = ''
app.config['SESSION_MONGODB_COLLECTION'] = ''

Session(app)

@app.route('/', methods=['GET'])
def home():
    if not 'img_ids' in session:
        session['img_ids'] = []
    return render_template("index.html")

@app.route('/upload',methods=['POST'])
def upload():
    data: dict = dict(request.form)
    
    img: bytes = request.files.get("image").read()
    img_b64: bytes = db.img_b64(img)
    
    timezone: str = data['tz']
    datetime: str = data['datetime'].replace('T',' ')
    
    cookie_payload: list = []
    
    _id: str = str(db.upload(img_b64, timezone, datetime))
    
    if 'img_ids' in request.cookies:
        
        ids: list = eval(request.cookies.get("img_ids"))
        ids.append(_id)
        
        cookie_payload = ids
    
    else:
        cookie_payload.append(_id)
    
    resp: object = make_response(redirect(url_for('results'), code=302))
    resp.set_cookie('img_ids', json.dumps(cookie_payload), max_age = 60*60*24*365*2)
    
    session['img_ids'] = cookie_payload

    return resp

@app.route('/results', methods=["GET"])
def results():
    context: list[dict] = []
    ids: list = request.cookies.get("img_ids") if 'img_ids' in request.cookies else session.get('img_ids')
    docs = db.get_all()
    if docs:
        for doc in docs:
            if doc['_id'].__str__() in ids:
                context.append(doc)
    return render_template("results.html", context=context)
