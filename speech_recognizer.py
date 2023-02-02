import config
import azure.cognitiveservices.speech as speechsdk

class SpeechRecognition:
    """
    A class that utilizes Azure's Cognitive Speech Service to recognize the user's speech input.
    
    Attributes:
    speech_config (SpeechConfig): A configuration object that takes a subscription key and a region as arguments
    speech_recognizer (SpeechRecognizer): The speech recogniton object that uses the above config to listen for user input
    """
    def __init__(self):
        """
        Initializes a new SpeechRecognition object
        """
        self.speech_config = speechsdk.SpeechConfig(subscription = config.retrieve_secret('PiBot-API'), region = 'eastus')
        self.speech_recognizer = speechsdk.SpeechRecognizer(speech_config=self.speech_config)
        self.speech_result = None

    def listen(self):
        """
        Listens for speech input and returns the recognized text in lowercase.
        :return: (str) The recognized speech input as a lowercase string.
        """
        print("Listening...")  
        
        # recognition_attempt is used to allow the program to loop for 30 seconds
        # before the user is notified that no speech could be recognized
        # this is to avoid spamming the user every 5 seconds 
        recognition_attempt = 0
        
        # continuously listen for speech
        while True:
            try:
                # a 5 second attempt to recognize the user's speech input
                result = self.speech_recognizer.recognize_once_async().get() 
            except Exception as e:
                print(f"Error occurred during speech recognition: {e}")
                break
            
            recognition_attempt += 1
            
            # if speech was recognized, print it and return the lowercase version
            if result.reason == speechsdk.ResultReason.RecognizedSpeech:
                recognized_speech = result.text
                print(f"\nInput:\nUser: {recognized_speech}")
                return recognized_speech.lower().replace('.', '').strip()
            
            # if the recognition was cancelled, check if it was due to an error
            elif result.reason == speechsdk.ResultReason.Canceled:
                cancellation_details = result.cancellation_details
                print(f"Speech Recognition canceled: {cancellation_details.reason}")
                
                if cancellation_details.reason == speechsdk.CancellationReason.Error:
                    print(f"Error Detais: {cancellation_details.error_details}")
                    print("Did you set the speech resource key and region values?")
            
            # if no speech was recognized after 30 seconds (6 attempts at 5 seconds each), notify the user
            elif recognition_attempt == 6:
                if result.reason == speechsdk.ResultReason.NoMatch:
                    print(f'No speech could be recognized: {result.no_match_details}')
                recognition_attempt = 0 
                 
        
        


