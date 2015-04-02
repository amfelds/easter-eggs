from hashlib import sha256
import hmac
import json
import os
import os.path
import threading
import urlparse
import random

from dropbox.client import DropboxClient, DropboxOAuth2Flow
from flask import abort, Flask, redirect, render_template, request, session, url_for
import redis
 
redis_url = os.environ['REDISTOGO_URL']
redis_client = redis.from_url(redis_url)
 
# App key and secret from the App console (dropbox.com/developers/apps)
APP_KEY = os.environ['APP_KEY']
APP_SECRET = os.environ['APP_SECRET']

app = Flask(__name__)
app.debug = True
 
# A random secret used by Flask to encrypt session data cookies
app.secret_key = os.environ['FLASK_SECRET_KEY']

# Easter variables
# TODO copy ref paths
# TODO start time

def get_url(route):
    '''Generate a proper URL, forcing HTTPS if not running locally'''
    host = urlparse.urlparse(request.url).hostname
    url = url_for(
        route,
        _external=True,
        _scheme='http' if host in ('127.0.0.1', 'localhost') else 'https'
    )

    return url

def get_flow():
    return DropboxOAuth2Flow(
        APP_KEY,
        APP_SECRET,
        get_url('oauth_callback'),
        session,
        'dropbox-csrf-token')

@app.route('/welcome')
def welcome():
    return render_template('welcome.html', redirect_url=get_url('oauth_callback'),
        webhook_url=get_url('webhook'), home_url=get_url('index'), app_key=APP_KEY)

@app.route('/oauth_callback')
def oauth_callback():
    '''Callback function for when the user returns from OAuth.'''

    access_token, uid, extras = get_flow().finish(request.args)
    session['uid'] = uid
 
    # Extract and store the access token for this user
    redis_client.hset('tokens', uid, access_token)

    process_user(uid)

    return redirect(url_for('done'))

def process_user(uid):
    '''Create folder tree, put random easter eggs in it.'''

    # OAuth token for the user
    token = redis_client.hget('tokens', uid)

    client = DropboxClient(token)

    # Set up the Easter hunt area!
    yard = client.add_copy_ref('M7Zx2DJjNXYxbjJsN3p6YQ','/Yard')
    client.file_create_folder('Easter basket')

    hide_eggs(uid)
    # start the timer

def hide_eggs(uid):
    token = redis_client.hget('tokens', uid)

    client = DropboxClient(token)

    # TODO for the play again scenario, should I delete any pre-existing egg files first? or re-create the whole yard?

    # Get flat list of paths to directories from '/Yard' TODO
    flat_list = {}
    recurse_yard('/Yard',flat_list,client)

    # Choose 5 random places to hide eggs
    hiding_places = random.sample(set(flat_list), 5)
    print hiding_places

    # copy egg images into those hiding places
    egg_refs = ['M7Zx2HpjY285MDRrbXlrdg','M7Zx2DN5Nm05M3Zqbmh3bA','M7Zx2Ho4d2w1d3B6czRubQ','M7Zx2DQ0YnFmMGwxcWZ0aA','M7Zx2HByb25hbmhvcXh0dA']
    client.add_copy_ref(egg_refs[0], hiding_places[0]+'/egg.jpg')
    client.add_copy_ref(egg_refs[1], hiding_places[1]+'/egg.jpg')
    client.add_copy_ref(egg_refs[2], hiding_places[2]+'/egg.jpg')
    client.add_copy_ref(egg_refs[3], hiding_places[3]+'/egg.jpg')
    client.add_copy_ref(egg_refs[4], hiding_places[4]+'/egg.jpg')

    # TODO set start time

def recurse_yard(path, list, client):
    contents = client.metadata(path)['contents']
    if (len(contents) > 0):
        for item in contents:
            if item['is_dir']:
                path = item['path']
                list[path] = path
                recurse_yard(path, list, client)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/login')
def login():
    return redirect(get_flow().start())

@app.route('/done')
def done(): 
    return render_template('done.html')

@app.route('/check_basket')
def check_basket():
    uid = session['uid']

    token = redis_client.hget('tokens', uid)

    client = DropboxClient(token)

    # # check if /Easter basket has all five eggs
    # # if not, say "You haven't found all the eggs yet! Keep looking."
    basket_contents = client.metadata('/Easter basket').get('contents')
    if len(basket_contents) == 5:
       # if so, stop the timer and say congrats (with play again option)     
       return render_template('found_eggs.html')
    else:
        # TODO alert that you're not done
        return render_template('done.html')

def validate_request():
    '''Validate that the request is properly signed by Dropbox.
       (If not, this is a spoofed webhook.)'''

    signature = request.headers.get('X-Dropbox-Signature')
    return signature == hmac.new(APP_SECRET, request.data, sha256).hexdigest()

@app.route('/webhook', methods=['GET'])
def challenge():
    '''Respond to the webhook challenge (GET request) by echoing back the challenge parameter.'''

    return request.args.get('challenge')

@app.route('/webhook', methods=['POST'])
def webhook():
    '''Receive a list of changed user IDs from Dropbox and process each.'''

    # Make sure this is a valid request from Dropbox
    if not validate_request(): abort(403)

    for uid in json.loads(request.data)['delta']['users']:
        # We need to respond quickly to the webhook request, so we do the
        # actual work in a separate thread. For more robustness, it's a
        # good idea to add the work to a reliable queue and process the queue
        # in a worker process.
        threading.Thread(target=process_user, args=(uid,)).start()
    return ''

if __name__=='__main__':
    app.run(debug=True)
