import datetime
from birthday import csv_to_dict
import discord
import csv

class Alarm:
    def __init__(self):
        self.alarms = csv_to_dict('alarms.csv')
    
    
    def validate_input(self, string):
        hora = string
        try:
            datetime.datetime.strptime(hora, "%H:%M")
            return True
        except ValueError:
            return False
    
    def agregar_alarma(self, mensaje, usuario):
        print (self.alarms)
        if not self.validate_input(mensaje):
            print(f"Formato invalido, input: {mensaje}")
            return
        hora = mensaje
        self.alarms[usuario] = hora
        with open('alarms.csv', 'w', newline='') as file:
            writer = csv.writer(file)
            writer.writerow(["Name", "Alarm"])
            for key, value in self.alarms.items():
                writer.writerow([key, value])
        
        
    async def mostrar_alarmas(self, hora, channel):
        if hora in self.alarms.values():
            for key, value in self.alarms.items():
                if value == hora:
                    user = await channel.guild.fetch_member(int(key))
                    alarma = f"Alarma para {user.mention}"
                    await channel.send(alarma)