import openai
import datetime
import csv
from birthday import csv_to_dict
from openai import OpenAI


#local llm chatbot class, you need to create a local port using LM studio to use this class
class LocalAIChatbot:
    def __init__(self, api_key: str):
        self.client = openai.OpenAI(base_url="http://localhost:1234/v1", api_key=api_key)
        #dictionary of user ids and their names for the llm to use
        self.nombres = {"lucianobogado.": "idoboga"}
        #dictionary of user names and their birthdays that can be used in the llm context
        self.fechas = csv_to_dict('birthday.csv')
        self.history = []
        self.history_answers = {}
        self.inverted_fechas = {v: k for k, v in self.fechas.items()}



    def get_openai_response(self, user_input: str, username: str) -> str:
        #add response to empty input
        if user_input == '':
            return "deci algo"
        self.history.append(user_input)
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

        completition = self.client.chat.completions.create(
            model="TheBloke/Mixtral-8x7B-Instruct-v0.1-GGUF",
            messages=[
                {"role": "system", "content": "you are a discord bot"},#add your context in content
                {"role": "user", "content": user_input},
            ],
            temperature=0.8
        )
        self.history.append(user_input)
        self.history_answers[user_input] = completition.choices[0].message.content.strip()
        print(user_input)
        return completition.choices[0].message.content.strip()
