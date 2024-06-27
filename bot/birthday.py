import discord
import datetime
import csv
import random


def csv_to_dict(filename):
        with open(filename, 'r') as file:
            reader = csv.reader(file)
            next(reader)  #skip encabezado
            return {rows[0]:rows[1] for rows in reader}

#clas that handles birthday list and alerts
class birthday:
    def __init__(self):
        self.fechas = csv_to_dict('birthday.csv')
        #add random gifs
        self.gifs = ["https://tenor.com/view/ganondorf-ganon-terminalmontage-transparent-dance-gif-23527523",
                     "https://tenor.com/view/ocarina-of-time-link-zelda-the-legend-of-zelda-nintendo-gif-16974185",
                     "https://tenor.com/view/the-legend-of-zelda-ocarina-of-time-zelda-nintendo-bongo-bongo-gif-19577273"]


    def agregar_birthday(self, string):
        mensaje = string.split()[1]
        if not self.validate_input(mensaje):
            return
        
        nombre, birthday = mensaje.split(",")
        
        self.fechas[nombre] = birthday
        
        with open('birthday.csv', 'w', newline='') as file:
            writer = csv.writer(file)
            writer.writerow(["Name", "Birthday"])
            for key, value in self.fechas.items():
                writer.writerow([key.capitalize(), value])
    
    
    def validate_date(self, date):
        try:
            datetime.datetime.strptime(date, "%d/%m/%Y")
            return True
        except ValueError:
            return False
    
    
    def validate_input(self, string):
        parts = string.split(",")
        if len(parts) != 2:
            return False
        
        birthday = parts[1]
        if not self.validate_date(birthday):
            return False
        
        return True
    
    
    async def alerta_birthday(self, channel):
        date = str(datetime.datetime.now().date())
        año, mes, dia = date.split("-")
        fecha = f"{dia}/{mes}"
        birthday = f"hoy es {fecha} y no hay cumpleaños"
        for key in self.fechas:
            if self.fechas[key][:-5] == fecha:
                #modify message as you please
                birthday = f"Hoy es {fecha} y es el cumpleaños de {key}!!! @everyone diganle Feliz cumpleaños a {key}!!!{random.choice(self.gifs)}"
                await channel.send(birthday)


    async def lista_birthday(self, message):
        embed = discord.Embed(title="Lista de cumpleaños", color=discord.Color.dark_purple())

        for key in self.fechas:
            embed.add_field(name=key, value=self.fechas[key], inline=False)
        await message.channel.send("Aca tenes la lista de cumpleaños")
        await message.channel.send(embed=embed)
