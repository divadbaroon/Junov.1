import spotipy

class PlaySong():
    
    def __init__(self, command_settings:object, api_keys:dict):
        self.scope = 'user-library-read user-modify-playback-state user-read-playback-state user-read-playback-position' \
        ' user-read-email user-read-private user-read-recently-played' \
        ' streaming playlist-modify-private playlist-read-private playlist-modify-public user-library-modify '
        self.clientID = api_keys['SPOTIFY-CLIENT-ID']
        self.clientSecret = api_keys['SPOTIFY-CLIENT-SECRET']
        redirectURI = 'http://localhost:8000/callback'

        self.oauth = spotipy.SpotifyOAuth(client_id=self.clientID, client_secret=self.clientSecret, redirect_uri=redirectURI, scope=self.scope)
        
        token_info = self.oauth.get_cached_token()
        
        if not token_info:
            auth_url = self.oauth.get_authorize_url()
            print(f"Please go here and authorize: {auth_url}")
            response = input("Paste the redirected URL here:")
            code = self.oauth.parse_response_code(response)
            token_info = self.oauth.get_access_token(code)
        
        if self.oauth.is_token_expired(token_info):
            token_info = self.oauth.refresh_access_token(token_info['refresh_token'])

        self.token = token_info['access_token']
        self.sp = spotipy.Spotify(auth=self.token)

        devices = self.sp.devices()
        if devices['devices']:
            self.device = devices['devices'][0]
        else:
            print('No devices available')
            self.device = None
            
        self.command_settings = command_settings
        self.track_name = None
        
    def play_song(self, track_name, artist_name=None):
        # get uri for given song name
        track_uri = self.get_track_uri(track_name, artist_name)
        
        if not self.device:
            return 'Sorry, there was an error setting up the device. Please ensure you have self.spotify open on your device.'
        if track_uri:  
            self.sp.start_playback(device_id=self.device['id'], uris=[track_uri])
        else:
            return f'Sorry, {track_name} could not be found. Please try asking again.'
        
        self.track_name = track_name
        self.command_settings.save_property(command='command', setting='song_playing', value=self.track_name)
      
    def get_track_uri(self, track_name, artist_name=None):
        query = track_name
        if artist_name:
            query += ' artist:' + artist_name

        results = self.sp.search(q=query, type='track', limit=1)

        if results['tracks']['items']:
            track_uri = results['tracks']['items'][0]['uri']
            return track_uri
        else:
            return None
        
    def next_track(self):
        self.sp.next_track(device_id=device['id'])

    def previous_track(self):
        self.sp.previous_track(device_id=device['id'])

    def can_pause(self):
        try:
            return self.sp.currently_playing().get('actions').get('disallows').get('pausing')
        except:
            return False

    def pause(self):
        if not self.sp.can_pause():
            self.sp.pause_playback(device_id=device.get('id'))
            self.command_settings.save_property(command='command', setting='song_playing', value=self.track_name)

    def resume(self):
        if self.sp.can_pause():
            self.sp.start_playback(device_id=device.get('id'))

    def shuffle(self):
        self.sp.shuffle(True, device_id=device['id'])

    def volume_up(self, amount: int = 10):
        global device
        device = self.sp.current_playback().get('device')
        current_vol = int(device['volume_percent'])
        if current_vol < 100:
            target_vol = amount + current_vol
            if target_vol > 100:
                target_vol = 100
            self.sp.volume(target_vol, device_id=device.get('id'))

    def volume_down(self, amount: int = 10):
        global device
        device = self.sp.current_playback().get('device')
        current_vol = int(device['volume_percent'])
        if current_vol > 0:
            target_vol = current_vol - amount
            if target_vol < 0:
                target_vol = 0
            self.sp.volume(target_vol, device_id=device.get('id'))

    def volume_set(self, amount: int):
        global device
        device = self.sp.current_playback().get('device')
        if amount < 0:
            self.sp.volume(0, device_id=device.get('id'))
            print("Volume cannot go lower than 0%")
        elif amount > 100:
            self.sp.volume(100, device_id=device.get('id'))
            print("Volume cannot go higher than 100%")
        else:
            self.sp.volume(amount, device_id=device.get('id'))
            print(f"Volume set to {amount}%")

    def restart(self):
        global device
        device = self.sp.current_playback().get('device')
        self.sp.seek_track(position_ms=0, device_id=device.get('id'))

    def now_playing(self):
        try:
            useful_info = ["artists", "name"]
            track = self.sp.currently_playing().get('item')
            return {key: track[key] for key in useful_info}
        except AttributeError:
            return "No song currently playing"

    def search_song(self, keyword: str):
        song = self.sp.search(q=keyword, limit=1)['tracks']['items'][0]
        return song

    def search_playlist(self, keyword: str):
        playlist = self.sp.search(keyword, type="playlist", limit=1)['playlists']['items'][0]
        return playlist

    def get_user_name(self, user):
        return user.get("diself.splay_name")

    def get_playlist_owner(self, playlist):
        return playlist.get("owner")

    def get_playlist_uri(self, playlist):
        return playlist.get("uri")

    def get_playlist_name(self, playlist):
        return playlist.get("name")
        

    
