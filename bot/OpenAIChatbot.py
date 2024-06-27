import openai
import datetime
import csv
from birthday import csv_to_dict
from openai import OpenAI

#openai chatbot class, needs api key to work
class OpenAIChatbot:
    def __init__(self, api_key: str):
        openai.api_key = api_key
        self.client = openai.OpenAI(api_key=api_key)

        self.nombres = {}
        self.fechas = csv_to_dict('birthday.csv')
        self.history = []
        self.history_answers = {}
        self.inverted_fechas = {v: k for k, v in self.fechas.items()}


    def initialize_openai_api(self, api_key: str) -> None:
        openai.api_key = api_key

    def get_openai_response(self, user_input: str, username: str) -> str:
        if user_input == '':
            return "deci algo"
        self.fechas = csv_to_dict('birthday.csv')
        
        username = username.lower()
        hour = datetime.datetime.now().time()
        date = datetime.datetime.now().date()
        date = str(datetime.datetime.now().date())
        año, mes, dia = date.split("-")
        fecha = f"{dia}/{mes}"

        if username in self.nombres:
            username = self.nombres[username]
        else:
            username = "loco"

        response = self.client.chat.completions.create(
            model="gpt-3.5-turbo",
            messages=[
                {"role": "system", "content":
                f"""you are a dicord bot """},#add your context in content
                {"role": "user", "content": user_input},
            ],
            temperature=0.1
        )
        self.history.append(user_input)
        self.history_answers[user_input] = response.choices[0].message.content.strip()
        print(user_input)
        return response.choices[0].message.content
