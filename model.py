from azure.identity import AzureCliCredential, get_bearer_token_provider
from openai import AzureOpenAI
 
class GPT:
    def __init__(self, model='gpt-4o') -> None:
        self.model = model
        credential = AzureCliCredential()

        self.aoiclient = AzureOpenAI(
            api_version = "2023-03-15-preview",
            azure_endpoint = 'https://aischool01.openai.azure.com',
            api_key = 'Placeholder',
            max_retries = 5,
        )
        # TODO: restore the following line before deployment
        #self.test_connection()


    def test_connection(self):
        print("Testing the connection to the Azure OpenAI service...")
        response = self.aoiclient.chat.completions.create(
                        model = self.model,
                        messages = [
                                {"role": "system", "content": "You are a helpful assistant."},
                                {"role": "user", "content": "Is the connection working?"}                    
                        ],
                        temperature = 0.0,
                        top_p = 1.0,
                        n = 1,
                        frequency_penalty = 0,
                        presence_penalty = 0,
                        stop = None,
                )
        print(response.choices[0].message.content)


    def infer(self, user_prompt, system_prompt=None):
        if system_prompt is None:
            system_prompt = 'You are a helpful assistant.'
        response = self.aoiclient.chat.completions.create(
                model = self.model,
                messages = [
                        {"role": "system", "content": system_prompt},
                        {"role": "user", "content": user_prompt}                    
                ],
                temperature = 0.0,
                top_p = 1.0,
                n = 1,
                frequency_penalty = 0,
                presence_penalty = 0,
                stop = None,
        )
        return response.choices[0].message.content
