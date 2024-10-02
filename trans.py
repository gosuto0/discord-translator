from discord import app_commands
import discord
import json
import deepl

config_json = json.load(open('./config.json', 'r'))

client = discord.Client(intents=discord.Intents.all())
tree = app_commands.CommandTree(client)
translator = deepl.Translator(config_json["deepl_token"])

@client.event
async def on_ready():
    print('LoggedIN')
    await tree.sync()

@client.event
async def on_reaction_add(reaction, user):
    try:
        countyr_json = json.load(open('./country.json', 'r'))
        if str(reaction) in countyr_json:
            country_data = countyr_json[str(reaction)]
            result = translator.translate_text(reaction.message.content, target_lang=country_data["country"])
            desc = f"""
    BASE: {reaction.message.content}

    {country_data["country"]}: {result.text}
            """
            embed = discord.Embed(title="", description=desc)
            embed.set_author(name=reaction.message.author.global_name,icon_url=reaction.message.author.display_avatar.url)
            await reaction.message.channel.send(embed=embed)
    except Exception as e:
        embed = discord.Embed(title="", description=f"ERROR: {str(e)}")
        embed.set_author(name=reaction.message.author.global_name,icon_url=reaction.message.author.display_avatar.url)
        await reaction.message.channel.send(embed=embed)
        
@tree.command(name="add_language",description="Add target language")
async def add_language(interaction: discord.Interaction, emoji: str, lang_code: str):
    countyr_json = json.load(open('./country.json', 'r'))
    countyr_json[str(emoji)] = {"country": lang_code}
    with open("./country.json", "w", encoding="utf-8") as f:
        json.dump(countyr_json, f, indent=2)
    await interaction.response.send_message(f"[ADD] {str(emoji)} : {lang_code}",ephemeral=True)

client.run(config_json["token"])
