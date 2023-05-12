
class StartTimer:
        
    def start_timer(self, user_time, metric):
        
        # Convert user_time to seconds
        if metric == 'seconds' or metric == 'second':
            pass
        elif metric == 'minutes' or metric == 'minute':
            user_time *= 60
        elif metric == 'hours' or metric == 'hour':
            user_time *= 3600

        return {'start_timer': user_time, 'response': f'Ok, I will start a timer for {user_time} {metric[0]}'}
    
    
    

