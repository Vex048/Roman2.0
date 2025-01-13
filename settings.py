import os


def init():
    global handValue,pause,started,stop_threads,currToken
    global client_id,client_secret,redirect_uri,auth_url,token_url,api_base_url,currentPlaylist,device_id
    handValue = None
    pause=False
    started=False
    client_id = os.getenv("CLIENT_ID")
    client_secret = os.getenv("CLIENT_SECRET")
    redirect_uri = os.getenv("REDIRECT_URI")
    auth_url = os.getenv("AUTH_URL")
    token_url = os.getenv("TOKEN_URL")
    api_base_url = os.getenv("API_BASE_URL")
    currentPlaylist = ####
    device_id = ####
    stop_threads=False
    currToken = None



