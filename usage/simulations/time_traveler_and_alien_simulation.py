from src.juno import Juno

def time_traveler_and_alien_simulation():
    """
    A simulation of a time traveler and alien talking to each other
    
    The agents are created using Juno and use the following methods for its core functionality:
    -------------------------------------------------------------------------------------------------
    .process() queries for and returns a response (Queries GPT with a given prompt and returns the response. Can also detect intent used for custom commands, however, that is not used in this example)                                    
    .verbalize() performs text-to-speech using Azure (very fast, good-quality) or ElevenLabs (slow, very high quality) voice engines 
    .listen() used to get user input via microphone (not used in this example)
    """
    
    # loading in profiles created using create_new_profile.py
    time_traveler = Juno(profile='time_traveler')
    alien = Juno(profile='alien')
    
    # manually starting the conversation with a beginning input (for speech input use .listen())
    beginning_input = 'I would like a cheese pizza with extra cheese please'
    time_traveler.verbalize(beginning_input)

    # alien's initial response
    alien_response = alien.process(beginning_input)
    alien.verbalize(alien_response)
    
    # endless loop of both agents exchanging dialog :) (for speech input use .listen())
    while True:
        
        # time_traveler response
        time_traveler_response = time_traveler.process(alien_response)
        time_traveler.verbalize(time_traveler_response)
        
        # alien response
        alien_response = alien.process(time_traveler_response)
        alien.verbalize(alien_response)
        
if __name__ == '__main__':  
    time_traveler_and_alien_simulation()