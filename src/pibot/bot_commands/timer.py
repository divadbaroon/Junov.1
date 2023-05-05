
class StartTimer:
        
    def start_timer(self, user_time, metric):
        
        # Convert user_time to seconds
        if metric == 'seconds':
            pass
        elif metric == 'minutes':
            user_time *= 60
        elif metric == 'hours':
            user_time *= 3600

        return {'start_timer': user_time, 'response': f'Ok, I will start a timer for {user_time} {metric[0]}'}
    
    
    

