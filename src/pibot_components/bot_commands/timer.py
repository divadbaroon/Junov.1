
class StartTimer:
    """A class to start a timer for a given amount of time."""
        
    def start_timer(self, user_time, metric):
        """Starts a timer for a given amount of time."""
        # Convert user_time to seconds
        if metric == 'seconds' or metric == 'second':
            pass
        elif metric == 'minutes' or metric == 'minute':
            user_time *= 60
        elif metric == 'hours' or metric == 'hour':
            user_time *= 3600

        return {'action': 'start_timer', 'user_time': user_time, 'response': f'Ok, I will start a timer for {user_time} {metric[0]}'}
    
    
    

