import google.generativeai as palm
import os

from dotenv import load_dotenv

def get_api():
    load_dotenv()
    
    palm.configure(api_key=os.getenv("TEXT_SUMMARY_KEY"))

    models = [
        m for m in palm.list_models() if "generateText" in m.supported_generation_methods
    ]

    return models[0]

class ExtractSummarization():
    def __init__(self, p) -> None:
        self.model = get_api()
        self.p = p

    def summary(self, text) -> list:
        s = len(text.split("."))

        prompt = "Choose the " + str(int(self.p * s)) + " most informative sentences from the following text and keep the words unchanged: "
        prompt = prompt + text
        
        completion = palm.generate_text(
            model=self.model,
            prompt=prompt,
            temperature=0.3,
            # The maximum length of the response
            max_output_tokens=2000,
        )

        result = completion.result.split("\n")

        result = [r[r.find(". ") + 2: ] for r in result]
        return result

class AbstractSummarization():
    def __init__(self) -> None:
        self.model = get_api()

    def summary(self, text:list)->str:

        prompt = "Rewrite the following sentences to form a paragraph: " + ' '.join(text)
        
        completion = palm.generate_text(
            model=self.model,
            prompt=prompt,
            temperature=0.3,
            # The maximum length of the response
            max_output_tokens=2000,
        )

        return completion.result
    
