from flask import Flask, url_for, render_template, request
from flask_oauthlib.client import OAuth
from flask import render_template
from flask import session

import os

app = Flask(__name__) #__name__ = "__main__" if this is the file that was run.  Otherwise, it is the name of the file (ex. webapp)

app.secret_key = os.environ['SECRET_KEY'] #used to sign session cookies

oauth = OAuth()

facebook = oauth.remote_app(
    'facebook',
    base_url='https://graph.facebook.com/',
    request_token_url=None,
    access_token_url='/oauth/access_token',
    authorize_url='https://www.facebook.com/dialog/oauth',
    consumer_key= os.environ['FACEBOOK_APP_ID'],
    consumer_secret= os.environ['FACEBOOK_APP_SECRET']
    request_token_params={'scope': 'email'}
)

@app.route("/")
def render_main():
    return render_template('home.html')

@app.route('/login')
def login():
    return facebook.authorize(callback=url_for('facebook_translate', _external=True, _scheme='https')) #callback URL must match the pre-configured callback URL

@app.route('/translate', methods=['GET'])
def facebook_translate():
  # Facebook responds with the access token as ?#access_token,
  # rather than ?access_token, which is only accessible to the browser.
  # This part is where things get really, really dumb.
  return '''  <script type="text/javascript">
    var token = window.location.href.split("access_token=")[1];
    window.location = "/callback?access_token=" + token;
  </script> '''

@app.route('/callback', methods=['GET', 'POST'])
def facebook_callback():
    print("Got Here")
    access_token = request.args.get("access_token")

    if access_token == "undefined":
        print("You denied the request to sign in.")

    session['facebook_oauth_token'] = access_token
    #
    # graph = facebook.GraphAPI(access_token)
    # profile = graph.get_object("me")
    # print(profile)

# @app.route('/authorized')
# def authorized():
#     #the facebook lines might not work
#     # next_url = request.args.get('next') or url_for('index')
#     # if resp is None:
#     #     flash(u'You denied the request to sign in.')
#     #     session.clear()
#     #     return redirect(next_url)
#     #
#     # session['facebook_token'] = (
#     #     resp['oauth_token'],
#     #     resp['oauth_token_secret']
#     # )
#     # session['facebook_user'] = resp['screen_name']
#     #
#     # flash('You were signed in as %s' % resp['screen_name'])
#     # return redirect(next_url)
#     resp = None
#     try:
#         resp = facebook.authorized_response()
#     except Exception as inst:
#         print(inst)
#
#     if resp is None:
#         session.clear()
#         message = 'Access denied: reason=' + request.args['error'] + ' error=' + request.args['error_description'] + ' full=' + pprint.pformat(request.args)
#         print(message)
#     else:
#         try:
#             session['facebook_oauth_token'] = (resp['access_token'], '')
#             session['facebook_oauth_token_secret'] = resp['oauth_token_secret']
#
#             session['facebook_user'] = resp['screen_name']
#
#             ('You were signed in as %s' % resp['screen_name'])
#
#         except Exception as inst:
#             session.clear()
#             print(inst)
#             message='Unable to login, please try again.  '
#     return render_template('home.html', message=message)

#the tokengetter is automatically called to check who is logged in.
@facebook.tokengetter
def get_facebook_oauth_token():
    return session.get('facebook_oauth_token')

if __name__=="__main__":
    app.run(debug=True)
