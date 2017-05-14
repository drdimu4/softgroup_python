from flask import Flask, render_template, url_for, request, session, redirect, jsonify, Blueprint
from flask_pymongo import PyMongo
import bcrypt
import pymongo
from threading import Thread
import os
import schedule
import time
import datetime
import pytz
from flask_restful import reqparse, abort, Api, Resource
from flask_httpauth import HTTPBasicAuth
from flask_restplus import Api,apidoc,Resource
from flask_wtf.csrf import CSRFProtect


# auth = HTTPBasicAuth()
from flask_restplus.cors import crossdomain

app = Flask(__name__)
csrf = CSRFProtect(app)

blueprint = Blueprint('api', __name__, url_prefix='/api')
api = Api(blueprint, doc='/doc/')

@api.documentation
def swagger_ui():
    return apidoc.ui_for(api)

app.register_blueprint(blueprint)

app.config['MONGO_DBNAME'] = 'bitcoin'
app.config['MONGO_URI'] = 'mongodb://localhost:27017/bitcoin'

mongo = PyMongo(app)

@app.route('/api/asd', methods=['GET'])
def asd():
    return jsonify({'message':'work'})

@app.route('/api/names', methods=['GET','POST'])
@crossdomain(origin='*')
def names():
    posts = mongo.db.posts
    logs = mongo.db.log
    old = logs.find_one(sort=[("date", pymongo.DESCENDING)])
    dates = []
    names = []
    for log in logs.find():
        dates.append(log.get("date"))
    for post in posts.find():
        if post.get('date') == old.get('date'):
            names.append(post.get('name'))
    return jsonify({'names':names})

@app.route('/api/all_posts', methods=['GET','POST'])
def all():
    posts = mongo.db.posts
    result = []
    for post in posts.find():
        item = {"name": post.get('name'),
                "symbol": post.get('symbol'),
                "market_cap": post.get('market_cap'),
                "price": post.get('price'),
                "supply": post.get('supply'),
                "volume": post.get('volume'),
                "h1": post.get('h1'),
                "h24": post.get('h24'),
                "d7": post.get('d7'),
                "date": post.get('date')}
        result.append(item)
    return jsonify(result)


@app.route('/api/all_logs', methods=['GET','POST'])
def all_logs():
    logs = mongo.db.log
    dates = []
    for log in logs.find():
        dates.append(log.get("date"))
    return jsonify(dates)


@app.route('/api/all_user', methods=['GET','POST'])
def users():
    users = mongo.db.users
    result = []
    for user in users.find():
        item = {'name': user.get("name"),'password':user.get("password").decode('utf-8')}
        result.append(item)
    return jsonify(result)


@app.route('/api/base/<string:field>', methods=['GET'])
def field(field):
    return jsonify({'field':field})

@app.route('/api/search', methods=['GET'])
def api_search():
    if request.method == 'GET':
        searchword = request.args.get('search', '')
        posts = mongo.db.posts
        logs = mongo.db.log
        result = []
        dates = []
        for log in logs.find():
            dates.append(log.get("date"))
        if len(searchword) == 0:
            return abort(404)
        for post in posts.find({'$or':[{"name":{"$regex":'\w*{}\w*'.format(searchword.capitalize())}},{"symbol":{"$regex":'\w*{}\w*'.format(searchword.upper())}}]}):
            item = {"name": post.get('name'),
                    "symbol": post.get('symbol'),
                    "market_cap": post.get('market_cap'),
                    "price": post.get('price'),
                    "supply": post.get('supply'),
                    "volume": post.get('volume'),
                    "h1": post.get('h1'),
                    "h24": post.get('h24'),
                    "d7": post.get('d7'),
                    "date": post.get('date')}
            result.append(item)
        return jsonify({'result':result})



@app.route('/', methods=['GET','POST'])
def index():
    if request.method == 'POST':
        # prevent malformed post request and useless DB hits
        if request.form.get('username', None) and request.form.get('password', None):
            users = mongo.db.users
            login_user = users.find_one({'name': request.form['username']})
            if login_user:
                if bcrypt.hashpw(request.form['password'].encode('utf-8'), login_user['password']) == login_user['password']:
                    session['username'] = request.form['username']
                    return redirect(url_for('index'))

        return render_template('index.html', message='Invalid login/password')
    if 'username' in session:
        posts = mongo.db.posts
        result = []
        logs = mongo.db.log
        old = logs.find_one(sort=[("date", pymongo.DESCENDING)])
        dates = []
        for log in logs.find():
            dates.append(log.get("date"))
        for post in posts.find():
            if post.get('date') == old.get('date'):
                item = {"name": post.get('name'),
                        "symbol": post.get('symbol'),
                        "market_cap": post.get('market_cap'),
                        "price": post.get('price'),
                        "supply": post.get('supply'),
                        "volume": post.get('volume'),
                        "h1": post.get('h1'),
                        "h24": post.get('h24'),
                        "d7": post.get('d7'),
                        "date": post.get('date')}
                result.append(item)
        return render_template('index.html', user = session['username'] , results = result, logs = dates)
    return render_template('index.html')


@app.route('/register', methods=['POST', 'GET'])
def register():
    if request.method == 'POST':
        users = mongo.db.users
        existing_user = users.find_one({'name': request.form['username']})

        if existing_user is None:
            hashpass = bcrypt.hashpw(request.form['password'].encode('utf-8'), bcrypt.gensalt())
            users.insert({'name': request.form['username'], 'password': hashpass})
            session['username'] = request.form['username']
            return redirect(url_for('index'))

        return render_template('register.html', message='This username is already exist')

    return render_template('register.html')


@app.route('/logout')
def logout():
    session.pop('username', None)
    return redirect(url_for('index'))


@app.route('/search',methods=['GET'])
def search():
    if request.method == 'GET':
        searchword = request.args.get('search', '')

        logs = mongo.db.log
        result = []
        dates = []
        for log in logs.find():
            dates.append(log.get("date"))
        if len(searchword) == 0:
            return render_template('index.html', user=session['username'], results=result, logs = dates)
        posts = mongo.db.posts
        for post in posts.find({'$or':[
            {"name":{"$regex":'\w*{}\w*'.format(searchword),
                     '$options' : 'i'}},
            {"symbol":{"$regex":'\w*{}\w*'.format(searchword),
                       '$options' : 'i'}}]}):
                        item = {"name": post.get('name'),
                                "symbol": post.get('symbol'),
                                "market_cap": post.get('market_cap'),
                                "price": post.get('price'),
                                "supply": post.get('supply'),
                                "volume": post.get('volume'),
                                "h1": post.get('h1'),
                                "h24": post.get('h24'),
                                "d7": post.get('d7'),
                                "date": post.get('date')}
                        result.append(item)
        return render_template('index.html', user=session['username'], results=result, logs = dates)


@app.route('/filter',methods=['GET'])
def filter():
    if request.method == 'GET':
        posts = mongo.db.posts
        logs = mongo.db.log
        name = request.args.get('currency', '')
        log_from = request.args.get('log_from', None)
        log_to = request.args.get('log_to', None)

        if log_from and log_to:
            log_from = pytz.utc.localize(datetime.datetime.strptime(log_from[:-6], '%Y-%m-%d %H:%M:%S.%f'))
            log_to = pytz.utc.localize(datetime.datetime.strptime(log_to[:-6], '%Y-%m-%d %H:%M:%S.%f'))
        else:
            log_from, log_to = [datetime.datetime.now(pytz.UTC)] * 2

        result = []
        dates = []
        for log in logs.find():
            dates.append(log.get("date"))
        for post in posts.find({"name":name}):
            '''
            # if (str(post.get('date')) >= log_from) and (str(post.get('date')) <= log_to):

            Not reliable comparison. Try str(11) > str(2) to catch idea.
            See this - http://stackoverflow.com/questions/4806911/string-comparison-technique-used-by-python
            '''
            dt = post.get('date')
            if (dt >= log_from) and (dt <= log_to):
                item = {"name": post.get('name'),
                        "symbol": post.get('symbol'),
                        "market_cap": post.get('market_cap'),
                        "price": post.get('price'),
                        "supply": post.get('supply'),
                        "volume": post.get('volume'),
                        "h1": post.get('h1'),
                        "h24": post.get('h24'),
                        "d7": post.get('d7'),
                        "date": post.get('date')}
                result.append(item)
        return render_template('index.html', user=session['username'], results=result, logs = dates)



def scrapper():
    os.system('python scrapper.py')


def run_schedule():
    while 1:
        schedule.run_pending()
        time.sleep(1)

if __name__ == '__main__':
    app.secret_key = 'secret'
    schedule.every(10).minutes.do(scrapper)
    t = Thread(target=run_schedule)
    t.start()
    app.run(debug=True, use_reloader=False)

