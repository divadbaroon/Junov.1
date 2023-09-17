import openai
import time
from configuration.secrets.key_vault import KeyVaultManager

import openai

training_data = "training/gpt_training_data/training_data.jsonl"

openai.api_key = KeyVaultManager().retrieve_secret("OPENAI-API-KEY")

def upload_training_data():

    # Upload training data
    file_response = openai.File.create(
        file=open(training_data, "rb"),
        purpose='fine-tune'
    )

    return file_response["id"]

def create_fine_tuning_job(file_id):
    
    while True:
        time.sleep(10) 
        try:
            # Create a fine-tuning job
            fine_tuning_response = openai.FineTuningJob.create(
                training_file=file_id,
                model="gpt-3.5-turbo",
                suffix="juno-test"
            )

            return fine_tuning_response["id"]
        except openai.error.APIError as e:  
            print(e)

def test_trained_model():

    completion = openai.ChatCompletion.create(
        model="ft:gpt-3.5-turbo-0613:personal:juno-test:7zqjfAto",
        messages=[
            {"role": "system", "content": "You are a helpful assistant."},
            {"role": "user", "content": "Hello!"}
        ]
    )
    print(completion.choices[0].message)
    
import time
# ... (other imports)

def main():
    try:
        #file_id = upload_training_data()
        #print(f"File ID: {file_id}")
        
        file_id = 'file-0RYp5lpVPbiTO3pBzcNGp1Eq'
        
        job_id = create_fine_tuning_job(file_id)
        print(f"Job ID: {job_id}")

        # Uncomment to list 10 fine-tuning jobs
        #print(openai.FineTuningJob.list(limit=10))

        # Uncomment to retrieve the state of a fine-tune
        #print(openai.FineTuningJob.retrieve(job_id))

        #test_trained_model()
        
    except openai.error.InvalidRequestError as e:
        print(f"An OpenAI InvalidRequestError occurred: {e}")
    except Exception as e:
        print(f"An unexpected error occurred: {e}")
        
if __name__ == "__main__":
    main()

