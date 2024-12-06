import urllib.parse
from flask import Flask, render_template, url_for,flash,redirect,session,request,jsonify
import requests
import os
import urllib.parse
from datetime import datetime
import json
app = Flask(__name__)
app.config['SECRET_KEY'] ='7gf08975354hfsnkl2c39edasdd93e5mhhuyyd2765'

client_id = os.getenv("CLIENT_ID")
client_secret = os.getenv("CLIENT_SECRET")
redirect_uri = os.getenv("REDIRECT_URI")
auth_url = os.getenv("AUTH_URL")
token_url = os.getenv("TOKEN_URL")
api_base_url = os.getenv("API_BASE_URL")

currentPlaylist = "spotify:playlist:78ecbA4FHLsy0EI068AsSb"
started=False
device_id = "af3641b98ee5d8a30ae23f4af4d7f7b799f5cf23"


@app.route('/')
@app.route('/home')
def home(loggedIn=False):
    global started
    started = False
    if request.args:
        loggedIn = True
    return render_template("index.html",loggedIn=loggedIn)

@app.route('/login')
def login():
    scope = 'user-read-private user-read-email user-modify-playback-state user-read-playback-state'
    params = {
        "client_id": client_id,
        'response_type': 'code',
        'scope': scope,
        'redirect_uri': redirect_uri,
        'show_dialog': True
    }
    auth_uri = auth_url + "?" + urllib.parse.urlencode(params)
    return redirect(auth_uri)

@app.route("/callback",methods=['POST','GET'])
def callback():
    if request.method == "POST":
        return redirect(url_for("home",loggedIn=True))
    if 'error' in request.args:
        return jsonify({"error": request.args['error']})
    if 'code' in request.args:
        req_body = {
            'code': request.args['code'],
            'grant_type': 'authorization_code',
            'redirect_uri': redirect_uri,
            'client_id': client_id,
            'client_secret': client_secret
        }
        response = requests.post(token_url, data=req_body)
        token_info  = response.json()
        session['access_token'] = token_info['access_token']
        session['refresh_token'] = token_info['refresh_token']
        session['expires_at']= datetime.now().timestamp() + token_info['expires_in']
        return redirect(url_for("home",loggedIn=True))
    

def get_auth_header(token):
    return {"Authorization": "Bearer "+ token}

def playlistsFiltering(playlists):
    items = playlists['items']
    playlistsNamesId = []
    for playlist in items:
        playlistsNamesId.append({"name": playlist['name'], "id": playlist['uri']})
    return playlistsNamesId




@app.route("/playlists",methods=['POST','GET'])
def playlists():
    global currentPlaylist
    if 'access_token' not in session:
        return redirect("/login")
    
    if datetime.now().timestamp() > session['expires_at']:
        return redirect("/refresh-token")
    
    headers = get_auth_header(session['access_token'])

    result  = requests.get(api_base_url+"me/playlists",headers=headers)
    playlists = result.json()
    namesId = playlistsFiltering(playlists)

    if request.method == "POST":
        for playlist in namesId:
            if request.form['chooseButton'] == playlist['name']:
                currentPlaylist = playlist['id']
    return render_template("playlists.html",names=namesId)




@app.route("/devices")
def get_devices():
    if 'access_token' not in session:
        return redirect("/login")
    
    if datetime.now().timestamp() > session['expires_at']:
        return redirect("/refresh-token")
    
    headers = get_auth_header(session['access_token'])
    result  = requests.get(api_base_url+"me/player/devices",headers=headers)
    devices = result.json()
    return jsonify(devices)


@app.route("/playbackState")
def get_playback_state():
    if 'access_token' not in session:
        return redirect("/login")
    
    if datetime.now().timestamp() > session['expires_at']:
        return redirect("/refresh-token")
    
    headers = get_auth_header(session['access_token'])
    result  = requests.get(api_base_url+"me/player",headers=headers)
    current_state = result.json()
    return jsonify(current_state)


@app.route("/playbackTrack")
def get_playback_track():
    if 'access_token' not in session:
        return redirect("/login")
    
    if datetime.now().timestamp() > session['expires_at']:
        return redirect("/refresh-token")
    
    headers = get_auth_header(session['access_token'])
    result  = requests.get(api_base_url+"me/player/currently-playing",headers=headers)
    current_song = result.json()
    return jsonify(current_song)





@app.route("/playPlayback",methods=['POST','GET'])
def start_stop_playback(pause=False):
    global started,currentPlaylist

    if 'access_token' not in session:
        return redirect("/login")
    if datetime.now().timestamp() > session['expires_at']:
        return redirect("/refresh-token")
    if started == False:
        req_body = {
                            "context_uri": currentPlaylist,
                            "position_ms": 0 
                        }
        started=True
        headers = get_auth_header(session['access_token'])
        requests.put(api_base_url+"me/player/play"+"?device_id="+device_id,headers=headers,data = json.dumps(req_body))
        pause=False
    if request.method == "POST":   
        if 'playPause' in request.form:
            state=request.form['playPause']
            if state == "Play":
                headers = get_auth_header(session['access_token'])
                requests.put(api_base_url+"me/player/play"+"?device_id="+device_id,headers=headers)
                pause=False 
            else:
                headers = get_auth_header(session['access_token'])
                requests.put(api_base_url+"me/player/pause"+"?device_id="+device_id,headers=headers)
                pause=True
        elif 'Previous' in request.form:
            print("Previous")
            headers = get_auth_header(session['access_token'])
            requests.post(api_base_url+"me/player/previous"+"?device_id="+device_id,headers=headers)
        elif 'Next' in request.form:
            print("Next")
            headers = get_auth_header(session['access_token'])
            requests.post(api_base_url+"me/player/next"+"?device_id="+device_id,headers=headers)
    return render_template("playstop.html",pause=pause)
    




@app.route("/refresh-token")
def refresh_token():
    if "refresh_token" not in session:
        return redirect("/login")
    
    if datetime.now().timestamp() > session['expires_at']:
        req_body = {
            'grant_type': 'refresh_token',
            'refresh_token': session['refresh_token'],
            'client_id': client_id,
            'client_secret': client_secret
        }
        response = requests.post(token_url,data=req_body)
        new_token_info = response.json()

        session['access_token'] = new_token_info['access_token']
        session['refresh_token'] = new_token_info['refresh_token']
        session['expires_at'] = datetime.now().timestamp() + new_token_info['expires_in']

        return redirect("/devices")
    



if __name__ == "__main__":
    app.run(debug=True)