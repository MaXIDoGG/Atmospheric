import discord
import html
import requests
import random
from googletrans import Translator

from discord.ext import commands
from config import settings

intents = discord.Intents.default()
intents.presences = True
intents.members = True
intents.message_content = True

bot = commands.Bot(command_prefix=settings['prefix'], intents=intents)


translator = Translator(service_urls=['translate.googleapis.com'])


def formatting(s):
    s = html.unescape(s)
    s = translator.translate(s, dest='ru').text
    return s


class Button(discord.ui.View):
    @discord.ui.button(label='1', style=discord.ButtonStyle.primary)
    async def button_callback1(self, interaction, button):
        button.disabled = True
        await interaction.response.edit_message(view=self)

    @discord.ui.button(label='2', style=discord.ButtonStyle.primary)
    async def button_callback2(self, interaction, button):
        button.disabled = True
        await interaction.response.edit_message(view=self)

    @discord.ui.button(label='3', style=discord.ButtonStyle.primary)
    async def button_callback3(self, interaction, button):
        button.disabled = True
        await interaction.response.edit_message(view=self)

    @discord.ui.button(label='4', style=discord.ButtonStyle.primary)
    async def button_callback4(self, interaction, button):
        button.disabled = True
        await interaction.response.edit_message(view=self)


@bot.command()
async def quiz(ctx):
    author = ctx.message.author

    response = requests.get('https://opentdb.com/api.php?amount=1')

    question = formatting(response.json()['results'][0]['question'])
    correct_answer = formatting(
        response.json()['results'][0]['correct_answer'])
    incorrect_answers = response.json()['results'][0]['incorrect_answers']
    for i in range(len(incorrect_answers)):
        incorrect_answers[i] = formatting(incorrect_answers[i])

    answers = incorrect_answers + [correct_answer]
    print(answers)
    random.shuffle(answers)
    answers = "1."+" ".join(answers)
    print(correct_answer)
    # buttons = [discord.Button()]
    await ctx.send(f'{author.mention}, {question}\nОтветы: {answers}', view=Button())


bot.run(settings['token'])
