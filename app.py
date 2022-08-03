from flask import Flask, render_template, request, redirect
from flask_sqlalchemy import SQLAlchemy
from shorten_service import shortenUrl

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///urls.db'
db = SQLAlchemy(app)

base_url = 'http://127.0.0.1:5000/'

class URLDB(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    long_url = db.Column(db.String(500), nullable=False)
    short_url = db.Column(db.String(50), nullable=False)

    def __repr__(self):
        return 'Url ' + str(self.id)


@app.route('/')
def index():
    return render_template('index.html')


@app.route('/url', methods=['GET', 'POST'])
def url():

    if request.method == 'POST':
        new_url = request.form['URL']
        new_shorter = shortenUrl(new_url)
        new_shorter = base_url+new_shorter
        url = URLDB(long_url=new_url, short_url=new_shorter)
        db.session.add(url)
        db.session.commit()
        return render_template('index.html', last_url=url)

    else:
        all_url = URLDB.query.all()
        return render_template('all_urls.html', urls=all_url)

if __name__ == '__name__':
    app.run(debug=True)