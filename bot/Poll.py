import discord

# Poll class, deprecated now that discord has a built-in poll feature
class Poll:
    def __init__(self):
        pass


    async def create_poll(self, message):
        # Extract the question and options from the message
        question, *options = message.content.removeprefix('encuestaocarina').split('.')
        if len(options) <= 1:
            await message.channel.send('Necesitas mas de una opcion para hacer una encuesta')
            return
        if len(options) > 10:
            await message.channel.send('Aguantaa, mas de 10 opciones no voy a poner loco')
            return

        reactions = ['1️⃣', '2️⃣', '3️⃣', '4️⃣', '5️⃣', '6️⃣', '7️⃣', '8️⃣', '9️⃣', '🔟']

        description = []
        for x, option in enumerate(options):
            description += '\n {} {}'.format(reactions[x], option)
        embed = discord.Embed(title=question, description=''.join(description), colour=discord.Colour.dark_purple())
        await message.channel.send("Aca tenes la encuesta amigo")
        react_message = await message.channel.send(embed=embed)
        for reaction in reactions[:len(options)]:
            await react_message.add_reaction(reaction)

        embed.set_footer(text='Elegi bien')
        await react_message.edit(embed=embed)