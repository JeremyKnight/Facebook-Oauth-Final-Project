from flask import Flask, url_for, render_template, request, session
from flask_oauthlib.client import OAuth
from flask import render_template

app = Flask(__name__) #__name__ = "__main__" if this is the file that was run.  Otherwise, it is the name of the file (ex. webapp)

app.secret_key = os.environ['SECRET_KEY'] #used to sign session cookies


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

@app.route('/authorized')
def authorized(resp):
    #the facebook lines might not work
    next_url = request.args.get('next') or url_for('index')
    if resp is None:
        flash(u'You denied the request to sign in.')
        session.clear()
        return redirect(next_url)

    session['facebook_token'] = (
        resp['oauth_token'],
        resp['oauth_token_secret']
    )
    session['facebook_user'] = resp['screen_name']

    flash('You were signed in as %s' % resp['screen_name'])
    return redirect(next_url)

''''resp = github.authorized_response()
   if resp is None:
        session.clear()
        message = 'Access denied: reason=' + request.args['error'] + ' error=' + request.args['error_description'] + ' full=' + pprint.pformat(request.args)      
    else:
        try:
            session['github_token'] = (resp['access_token'], '') #save the token to prove that the user logged in
            session['user_data']=github.get('user').data
            message='You were successfully logged in as ' + session['user_data']['login']
        except Exception as inst:
            session.clear()
            print(inst)
            message='Unable to login, please try again.  '
    return render_template('message.html', message=message)''''

if __name__=="__main__":
    app.run(debug=False)
