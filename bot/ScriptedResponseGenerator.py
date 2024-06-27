import re
import random

#scripted responses class
class ScriptedResponseGenerator:
    def __init__(self):
        #add your scripted responses here
        self.respuestas = {"lol": "bulk"}
        self.respuestasN = {"rocket": "otra vez jugando a los cochecitos"}
        self.respuestas_nombre = {"lucianobogado.": "idoboga"}
        self.respuestasSiempre = {"como estas ocarina": "https://media.discordapp.net/attachments/1116832518050676826/1123071308197015572/makeitmeme_PWmHN.gif?ex=66022d29&is=65efb829&hm=016d35d1446d81346702d217b50de7d2e0b2649eecd2314a8847a4920bad5e42&"}


    def get_scripted_response(self, user_input: str, username: str) -> str:
        lowered_username = username.lower()              
        lowered_str: str = user_input.lower()
        for key in self.respuestas:#uses 1st dict
            if re.search(key, lowered_str) and random.random() < 0.10:
                return self.respuestas[key]
        for key in self.respuestasN:#uses 2nd dict
            for name in self.respuestas_nombre:#uses 3rd dict, adds a name to the response
                if re.search(name, lowered_username) and re.search(key, lowered_str) and random.random() < 0.10:
                    return f"{self.respuestasN[key]} {self.respuestas_nombre[name]}"
        for key in self.respuestasSiempre:#uses 4th dict
            if re.search(key, lowered_str):
                return self.respuestasSiempre[key]