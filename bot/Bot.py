from typing import Final
import os
from dotenv import load_dotenv
from discord import Intents, Client, Message
from ScriptedResponseGenerator import ScriptedResponseGenerator
from OpenAIChatbot import OpenAIChatbot
from ReplicateGenHD import ReplicateGenHD
from ReplicateGenAnime import ReplicateGenAnime
from ReplicateGenPortrait import ReplicateGenPortrait
import asyncio
from Poll import Poll
import discord
from discord.ext import commands, tasks
import datetime
from datetime import datetime, time, timedelta
from birthday import birthday
from news import News
from Alarm import Alarm
from LocalAIChatbot import LocalAIChatbot
os.chdir(os.path.dirname(os.path.abspath(__file__)))

#discord bot class
class Bot:
    def __init__(self):
        # Load TOKEN and API KEY
        load_dotenv()
        self.TOKEN: Final[str] = os.getenv("DISCORD_TOKEN")
        self.KEY: Final[str] = os.getenv("OPENAI_KEY")
        self.LOCAL_KEY = "lm-studio"
        
        
        
        # Initialize classes
        self.openai_bot = OpenAIChatbot(self.KEY)
        self.localai_bot = LocalAIChatbot(self.LOCAL_KEY)
        self.response_generator = ScriptedResponseGenerator()
        self.replicate_generatorHD = ReplicateGenHD()
        self.replicate_generatorAnime = ReplicateGenAnime()
        self.replicate_generatorPortrait = ReplicateGenPortrait()
        self.poll = Poll()
        self.cumple = birthday()
        self.noticias = News()
        self.alarma = Alarm()
        
        
        # Setup bot
        intents: Intents = Intents.default()
        intents.message_content = True
        self.client: Client = Client(intents=intents)
        # Define bot message methods
        self.client.event(self.on_ready)
        self.client.event(self.on_message)
    
    #method to check if the message needs to be sent to the local ai chatbot
    def needs_localai_response(self, user_message: str) -> bool:
        user_message = user_message.lower()
        return user_message.startswith("localocarina")
    #method to check if the message needs to be sent to the openai chatbot
    def needs_openai_response(self, user_message: str) -> bool:
        user_message = user_message.lower()
        return user_message.startswith("ocarina")
    #method to check if the message needs to be sent to the replicate API
    def needs_replicate_response(self, user_message: str) -> bool:
        user_message = user_message.lower()
        return user_message.startswith("jpgocarina")
    
    #method to check if the message needs to be sent to the replicate anime API
    def needs_replicate_response_anime(self, user_message: str) -> bool:
        user_message = user_message.lower()
        return user_message.startswith("animeocarina")
    
    #method to check if the message needs to be sent to the replicate portrait API
    def needs_replicate_response_portrait(self, user_message: str) -> bool:
        user_message = user_message.lower()
        return user_message.startswith("portraitocarina")
    
    #method to check if the message needs to be sent to the poll class
    def needs_poll(self, user_message: str) -> bool:
        user_message = user_message.lower()
        return user_message.startswith("encuestaocarina")
    
    #method to check if the message needs to be sent to the birthday class
    def needs_birthday(self, user_message: str) -> bool:
        user_message = user_message.lower()
        return user_message.startswith("cumpleañosocarina")
    def needs_birthday_list(self, user_message: str) -> bool:
        user_message = user_message.lower()
        return user_message.startswith("listaocarina")
    
    #method to send the message to the news class
    def needs_news(self, user_message: str) -> bool:
        user_message = user_message.lower()
        return user_message.startswith("noticiasocarina")
    
    def needs_alarma(self, user_message: str) -> bool:
        user_message = user_message.lower()
        return user_message.startswith("alarmaocarina")
     
    async def send_message(self, message: Message, username: str) -> None:
        username: str = str(message.author)
        userId: str = str(message.author.id)
        user_message: str = message.content
        channel: str = str(message.channel)
        if not user_message:
            print("Empty message, boolean intent possibly not set")
            return
        try:
            if self.needs_localai_response(user_message):
                response = f"""{self.localai_bot.get_openai_response(user_message[13:], username)}"""
            elif self.needs_openai_response(user_message):
                response = f"""{self.openai_bot.get_openai_response(user_message[8:], username)}"""
            elif self.needs_replicate_response(user_message):
                print("HD response")
                response = f"""aca tenes tu imagen pibe {self.replicate_generatorHD.get_replicate_response(user_message, 1, 7.5, 100)[0]}"""
            elif self.needs_replicate_response_anime(user_message):
                print("Anime response")
                response = f"""aca tenes tu imagen de anime pibe {self.replicate_generatorAnime.get_replicate_response(user_message, 1, 7, 20)[0]}"""
            elif self.needs_replicate_response_portrait(user_message):
                print("Portrait response")
                response = f"""aca tenes tu imagen de retrato pibe {self.replicate_generatorPortrait.get_replicate_response(user_message)[0]}"""
            elif self.needs_poll(user_message):
                response = await self.poll.create_poll(message)
            elif self.needs_birthday(user_message):
                self.cumple.agregar_birthday(user_message)
                if self.cumple.validate_input(user_message.split()[1]):
                    response = f"Cumpleaños agregado: {user_message.split()[1]}"     
                else:  
                    response = f"Formato invalido, el formato es nombre,dd/mm/yy, tu mensaje fue {user_message.split()[1]}"   
            elif self.needs_birthday_list(user_message):
                response = await self.cumple.lista_birthday(message)
            elif self.needs_news(user_message):
                response = f"Encontre esta noticia sobre {user_message.split()[1:][0]}: {self.noticias.get_news(user_message.split()[1])[0:1998]}"
            elif self.needs_alarma(user_message):
                self.alarma.agregar_alarma(user_message.split()[1], userId)
                response = f"Alarma agregada a las {user_message.split()[1]} para {username}"
            else:
                response = self.response_generator.get_scripted_response(user_message, username)
            return response
        except Exception as e:
            print(e)
            return ""     
        
    async def on_ready(self) -> None:
        print(f'{self.client.user} has connected to Discord!')
        if time(0, 0) <= datetime.now().time() <= time(12, 30):
            #input channel id to send alerts
            await self.cumple.alerta_birthday(self.client.get_channel(1))
        #alarm iterator each minute, the iterator never stops
        while True:
            await asyncio.sleep(60)
            self.alarma = Alarm()
            print("Checking alarms")
            #input channel id to send alerts
            await self.alarma.mostrar_alarmas(datetime.now().time().strftime("%H:%M"), self.client.get_channel(1))
        
    async def on_message(self, message: Message) -> None:
        if message.author == self.client.user:
            return
        username: str = str(message.author)
        user_message: str = message.content
        channel: str = str(message.channel)
        print(f'[{channel}] {username}: {user_message}')
        response = await self.send_message(message, username)
        if response:
            async with message.channel.typing():
                await asyncio.sleep(3)
            if user_message[0] == "?":
                await message.author.send(response)
            else:
                await message.channel.send(response)
        
     
     
        
    def run(self) -> None:
        self.client.run(token=self.TOKEN)
        
        
if __name__ == "__main__":
    bot = Bot()
    bot.run()