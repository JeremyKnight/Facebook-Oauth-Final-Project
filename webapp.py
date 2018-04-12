from flask import Flask, url_for, render_template, request
from flask_oauthlib.client import OAuth
from flask import render_template

app = Flask(__name__) #__name__ = "__main__" if this is the file that was run.  Otherwise, it is the name of the file (ex. webapp)

facebook = oauth.remote_app('facebook',
    base_url='https://graph.facebook.com/',
    request_token_url=None,
    access_token_url='/oauth/access_token',
    authorize_url='https://www.facebook.com/dialog/oauth',
    consumer_key= os.environ['FACEBOOK_APP_ID'],
    consumer_secret= os.environ['FACEBOOK_APP_SECRET'],
    request_token_params={'scope': 'email'}
)

@app.route("/")
def render_main():
    return render_template('home.html')

@app.route('/login')
def login():
    return facebook.authorize(callback=url_for('authorized', _external=True, _scheme='https')) #callback URL must match the pre-configured callback URL


if __name__=="__main__":
    app.run(debug=False)
