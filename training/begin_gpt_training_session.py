import openai
import time
import requests
from configuration.utils.key_vault_handler import KeyVaultManager

training_data = "training/gpt_training_data/training_data.jsonl"

class OpenAIFineTuningJob:
    
    def __init__(self):
        openai.api_key = KeyVaultManager().retrieve_secret("OPENAI-API-KEY")
        
    def start_finetuning(self):
        """
        Begin the fine-tuning process.
        """
        # upload training data
        file_id = self._upload_training_data()
        
        # create fine-tuning job
        self._create_fine_tuning_job(file_id)
        
        self._test_trained_model()

    def _upload_training_data() -> str:
        """
        Upload the training data to OpenAI's servers.
        """

        # Upload training data
        print(f"Uploading training data...")
        file_response = openai.File.create(
            file=open(training_data, "rb"),
            purpose='fine-tune'
        )

        print(f"Training data uploaded successfully")
        print(f"File ID: {file_response['id']}")
        
        return file_response["id"]

    def _create_fine_tuning_job(file_id):
        """
        Begins a fine-tuning job.
        """
        
        print(f"Giving servers some time to process the file")
        time.sleep(20)
        
        print(f"Creating fine-tuning job...")
        while True:
            # giving the servers some more time to process the file
            time.sleep(10) 
            try:
                # Create a fine-tuning job
                fine_tuning_response = openai.FineTuningJob.create(
                    training_file=file_id,
                    model="gpt-3.5-turbo",
                    suffix="juno-test"
                )
                
                print(f"Fine-tuning job completed!")
                print(f"File ID: {fine_tuning_response['id']}")

                return fine_tuning_response["id"]
            except openai.error.APIError as e:  
                print(f"Still waiting for servers to process the file")

    def _test_trained_model():
        """
        Tests the fine-tuned model.
        """

        completion = openai.ChatCompletion.create(
            model="ft:gpt-3.5-turbo-0613:personal:juno-test:7zqjfAto",
            messages=[
                {"role": "system", "content": "You are a helpful assistant."},
                {"role": "user", "content": "Hello!"}
            ]
        )
        print(completion.choices[0].message)
        
    def _wait_for_operation_to_complete(self, operation_location, headers):
        while True:
            time.sleep(5)  # Wait for 5 seconds before checking the status again
            response = requests.get(operation_location, headers=headers)
            status = response.json().get("status")
            if status == "succeeded":
                print("Operation completed successfully.")
                break
            elif status == "failed":
                print("Operation failed.")
                break
            
if __name__ == "__main__":
    new_job = OpenAIFineTuningJob()
    new_job.start_finetuning()

