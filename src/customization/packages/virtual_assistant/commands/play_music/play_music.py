import spotipy

class PlaySong():
    
    def __init__(self, api_keys:dict):
        
        self._load_in_secret_data(api_keys)
        
        self._authenticate()
            
        self.track_name = None
        
    def play_song(self, track_name, artist_name=None):
        """
        Plays a given song via Spotify
        """
        # get uri for given song name
        track_uri = self._get_track_uri(track_name, artist_name)
        self.track_name = track_name
        
        if not self.device:
            return 'Sorry, there was an error setting up the device. Please ensure you have spotify open on your device.'
        if track_uri:  
            self.sp.start_playback(device_id=self.device['id'], uris=[track_uri])
        else:
            return f'Sorry, {track_name} could not be found. Please try asking again.'
        
        self.track_name = track_name
        
    def pause_song(self):
        """
        Pauses the current track
        """
        if not self._can_pause():
            self.sp.pause_playback(device_id=self.device.get('id'))

    def unpause_song(self):
        """
        Unpauses the current track
        """
        if self._can_pause():
            self.sp.start_playback(device_id=self.device.get('id'))
            return f'Unpausing {self.track_name}'
        
    def next_track(self):
        """
        Skips to the next track
        """
        self.sp.next_track(device_id=device['id'])

    def previous_track(self):
        """
        Skips to the previous track
        """
        self.sp.previous_track(device_id=device['id'])

    def shuffle(self):
        """
        Toggles shuffle on or off
        """
        self.sp.shuffle(True, device_id=device['id'])

    def volume_up(self, amount: int = 10):
        """
        Increases the volume by a given amount
        """
        global device
        device = self.sp.current_playback().get('device')
        current_vol = int(device['volume_percent'])
        if current_vol < 100:
            target_vol = amount + current_vol
            if target_vol > 100:
                target_vol = 100
            self.sp.volume(target_vol, device_id=device.get('id'))

    def volume_down(self, amount: int = 10):
        """
        Decreases the volume by a given amount
        """
        global device
        device = self.sp.current_playback().get('device')
        current_vol = int(device['volume_percent'])
        if current_vol > 0:
            target_vol = current_vol - amount
            if target_vol < 0:
                target_vol = 0
            self.sp.volume(target_vol, device_id=device.get('id'))

    def volume_set(self, amount: int):
        """
        Sets the volume to a given amount
        """
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
        """
        Restarts the current track
        """
        global device
        device = self.sp.current_playback().get('device')
        self.sp.seek_track(position_ms=0, device_id=device.get('id'))

    def now_playing(self):
        """
        Returns a dictionary of the currently playing track's artist and name
        """
        try:
            useful_info = ["artists", "name"]
            track = self.sp.currently_playing().get('item')
            return {key: track[key] for key in useful_info}
        except AttributeError:
            return "No song currently playing"

    def get_playlist_uri(self, playlist):
        return playlist.get("uri")

    def get_playlist_name(self, playlist):
        return playlist.get("name")
    
    def _can_pause(self):
        try:
            return self.sp.currently_playing().get('actions').get('disallows').get('pausing')
        except:
            return False
    
    def _get_track_uri(self, track_name, artist_name=None):
        query = track_name
        if artist_name:
            query += ' artist:' + artist_name

        results = self.sp.search(q=query, type='track', limit=1)

        if results['tracks']['items']:
            track_uri = results['tracks']['items'][0]['uri']
            return track_uri
        else:
            return None
        
    def _load_in_secret_data(self, api_keys:dict) -> None: 
        self.scope = 'user-library-read user-modify-playback-state user-read-playback-state user-read-playback-position' \
        ' user-read-email user-read-private user-read-recently-played' \
        ' streaming playlist-modify-private playlist-read-private playlist-modify-public user-library-modify '
        self.clientID = api_keys['SPOTIFY-CLIENT-ID']
        self.clientSecret = api_keys['SPOTIFY-CLIENT-SECRET']
        redirectURI = 'http://localhost:8000/callback'

        # Hardcoded directory for cache
        cache_dir = "src/customization/packages/virtual_assistant/commands/play_music"

        # Construct the cache_path based on the hardcoded directory
        cache_path = f"{cache_dir}/.cache"

        # Pass the cache_path to SpotifyOAuth
        self.oauth = spotipy.SpotifyOAuth(client_id=self.clientID, 
                                        client_secret=self.clientSecret, 
                                        redirect_uri=redirectURI, 
                                        scope=self.scope,
                                        cache_path=cache_path)
            
    def _authenticate(self):
        token_info = self.oauth.get_cached_token()
        
        self._check_token(token_info)

        self.token = token_info['access_token']
        self.sp = spotipy.Spotify(auth=self.token)

        devices = self.sp.devices()
        if devices['devices']:
            self.device = devices['devices'][0]
        else:
            print('No devices available')
            self.device = None
        
    def _check_token(self, token_info) -> None:
        if not token_info:
            auth_url = self.oauth.get_authorize_url()
            print(f"Please go here and authorize: {auth_url}")
            response = input("Paste the redirected URL here:")
            code = self.oauth.parse_response_code(response)
            self.token_info = self.oauth.get_access_token(code)
        
        if self.oauth.is_token_expired(token_info):
            token_info = self.oauth.refresh_access_token(token_info['refresh_token'])
        

    
