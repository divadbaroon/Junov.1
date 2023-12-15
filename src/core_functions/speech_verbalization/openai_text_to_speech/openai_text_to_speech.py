from openai import OpenAI
from concurrent.futures import ThreadPoolExecutor
from pydub import AudioSegment
from pydub.playback import play
import io
import asyncio

class OpenAITextToSpeech:
    
    def __init__(self, api_keys:dict):
        self.client = OpenAI(api_key = api_keys['OPENAI-API-KEY'])
        
    def fetch_audio_sync(self, text):
        """
        Synchronously fetch audio for a given text using the OpenAI client.
        """
        response = self.client.audio.speech.create(
        model="tts-1",
        voice="alloy",
        input=text
        )
        return io.BytesIO(response.content)

    async def fetch_audio(self, text):
        """
        Asynchronously fetch audio by running the synchronous OpenAI call in a thread.
        """
        loop = asyncio.get_event_loop()
        with ThreadPoolExecutor() as pool:
            audio_stream = await loop.run_in_executor(pool, self.fetch_audio_sync, text)
            return audio_stream

    async def main(self, input):
        # Split the input text into sentences
        sentences = input.split('. ')

        # Fetch audio for each sentence
        audio_responses = await asyncio.gather(*[self.fetch_audio(sentence) for sentence in sentences])

        # Play each audio response sequentially
        for audio_stream in audio_responses:
            audio_segment = AudioSegment.from_file(audio_stream, format="mp3")
            play(audio_segment)
    
    def text_to_speech(self, input, language_country_code):
        asyncio.run(self.main(input))