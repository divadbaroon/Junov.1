import json

class BotProperties():
    """
    A class that can be used to retrieve and save properties from "bot_properties.json"
    """
    
    def get_property(self, property):
        """
        Returns the desired property from "bot_properties.json"
        """
        try:
            with open("bot_properties.json", "r") as f:
                data = json.load(f)
                
            if property == 'voice_name':
                gender = data['chatbot'].get('gender')
                language = data['chatbot'].get('language')
                if gender == 'female':
                    voice_name =  data['female_voices'].get(language)
                elif gender == 'male':
                    voice_name =  data['male_voices'].get(language)
                return voice_name
            
            return data['chatbot'].get(property)
        
        except FileNotFoundError:
            print('The file "bot_properties.json" is missing.\nMake sure all files are located within the same folder')
    
    def save_property(self, property, value):
        """
        Saves the desired property to "bot_properties.json"
        """
        try:
            with open("bot_properties.json", "r") as f:
                data = json.load(f)
            
            data['chatbot'][property] = value.lower()
            
            with open("bot_properties.json", "w") as f:
                json.dump(data, f, indent=4)
        except FileNotFoundError:
            print('The file "bot_properties.json" is missing.\nMake sure all files are located within the same folder')