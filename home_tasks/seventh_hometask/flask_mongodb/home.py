from flask import Flask, render_template, url_for, request, session, redirect
from flask_pymongo import PyMongo
import bcrypt
app = Flask(__name__)

app.config['MONGO_DBNAME'] = 'new_base'
app.config['MONGO_URI'] = 'mongodb://localhost:27017/new_base'

mongo = PyMongo(app)


@app.route('/')
def index():

    if 'username' in session:

        posts = mongo.db.posts
        result = []
        for post in posts.find():
            # print(post.get('author'))
            name = post.get('topic_name'),
            author = post.get('author'),
            price = post.get('price'),
            currency = post.get('currency'),
            url = post.get('url')
            post_text = post.get('post_text')
            dict = {'name': name, 'author': author, "price": price, 'currency': currency, 'url': url, 'post_text':post_text}
            result.append(dict)
        return render_template('table.html',user = session['username'],results=result)
    return render_template('no_user.html')

@app.route('/login', methods=['GET','POST'])
def login():
    if request.method == 'GET':
        return render_template('login.html')
    if request.method == 'POST':
        users = mongo.db.users
        login_user = users.find_one({'name' : request.form['username']})

        if login_user:
            if bcrypt.hashpw(request.form['password'].encode('utf-8'), login_user['password']) == login_user['password']:
                session['username'] = request.form['username']
                return redirect(url_for('index'))

        return render_template('login.html',message = 'Invalid login/password')


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

        return 'That username already exists!'

    return render_template('register.html')

@app.route('/logout')
def logout():
    session.pop('username', None)
    return redirect(url_for('index'))

@app.route('/description', methods=['POST'])
def description():
    url = request.form['url']
    price = request.form['price']
    currency = request.form['currency']
    author = request.form['author']
    name = request.form['name']
    post_text = request.form['post_text']
    return render_template('description.html', url = url, price = price, currency = currency, author = author, name = name, post_text = post_text)

@app.route('/search',methods=['GET'])
def search():
    if request.method == 'GET':
        searchword = request.args.get('search', '')
        posts = mongo.db.posts
        result = []
        for post in posts.find({'$or':[{"topic_name":{"$regex":'\w*{}\w*'.format(searchword)}},{"post_text":{"$regex":'\w*{}\w*'.format(searchword)}}]}):
            # print(post.get('author'))
            name = post.get('topic_name'),
            author = post.get('author'),
            price = post.get('price'),
            currency = post.get('currency'),
            url = post.get('url')
            post_text = post.get('post_text')
            dict = {'name': name, 'author': author, "price": price, 'currency': currency, 'url': url,
                    'post_text': post_text}
            result.append(dict)
        return render_template('table.html', user=session['username'], results=result)

if __name__ == '__main__':
    app.secret_key = 'secret'
    app.run()
