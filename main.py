from discord.ext import commands
from discord import app_commands
import discord
import json

bot = commands.Bot(command_prefix="?", intents=discord.Intents.all())
bot.remove_command("help")

finished_sentences_channel_id = None
sentence_builder_channel_id = None
last_message_ended_with_dot = False
sentence = []
sentence_authors = []
sentence_counter = 0


@bot.event
async def on_ready():
	await load_config()
	print("Online")
	try:
		synced = await bot.tree.sync()
		print(f"Synced {len(synced)} commands")
	except Exception as e:
		print(e)


try:
    with open('sentence_counter.json', 'r') as f: 
        sentence_counter = json.load(f)
except FileNotFoundError:
    pass


async def load_config():
    global finished_sentences_channel_id, sentence_builder_channel_id
    try:
        with open('channels.json', 'r') as f:
            config = json.load(f)
            finished_sentences_channel_id = config.get('finished_sentences_channel_id')
            sentence_builder_channel_id = config.get('sentence_builder_channel_id')
    except FileNotFoundError:
        pass

async def save_config():
    global finished_sentences_channel_id, sentence_builder_channel_id
    config = {'finished_sentences_channel_id': finished_sentences_channel_id, 'sentence_builder_channel_id': sentence_builder_channel_id}
    with open('channels.json', 'w') as f:
        json.dump(config, f)


@bot.tree.command(name="set_finished_channel", description="Set the finished sentences channel.")
@app_commands.checks.has_permissions(manage_messages=True)
async def set_finished_channel(interaction: discord.Interaction, channel: discord.TextChannel):
    global finished_sentences_channel_id
    finished_sentences_channel_id = channel.id
    try:
        await interaction.response.send_message(f"Finished sentences channel set to {channel.mention}", ephemeral=False)
        await save_config()
    except (Exception) as e:
        await interaction.response.send_message("```py\n{}: {}\n```".format(type(e).__name__, str(e)), ephemeral=True)    

@bot.tree.command(name="set_builder_channel", description="Set the sentence builder channel.")
@app_commands.checks.has_permissions(manage_messages=True)
async def set_builder_channel(interaction: discord.Interaction, channel: discord.TextChannel):
    global sentence_builder_channel_id
    sentence_builder_channel_id = channel.id
    try:
        await interaction.response.send_message(f"Sentence builder channel set to {channel.mention}", ephemeral=False)
        await save_config()
    except (Exception) as e:
        await interaction.response.send_message("```py\n{}: {}\n```".format(type(e).__name__, str(e)), ephemeral=True)

@bot.tree.command(name="help", description="Helpful information about the bot.")
async def sendhere(interaction: discord.Interaction):
	embed=discord.Embed(title="Github Repository", url="https://github.com/Topromm/Sentence-Builder")
	embed.set_author(name="Sentence Builder Help")
	embed.add_field(name="Setup", value="Setup is fast and easy. Just use the /set_builder_channel command and select a channel where you'd like to build sentences with other users. After this you can use the /set_finished_channel command and select a channel where you'd like the finished works of art to be posted in.", inline=False)
	embed.add_field(name="Want to discuss issues, ideas, feedback?", value="You can reach me on Github through the \"Github Repository\" hyperlink above. We'll always be ready to help when issues arise, but you can also reach out if you have any new ideas you'd like to tell us about!", inline=True)
	embed.set_footer(text="- Developer Team", icon_url = "https://cdn-icons-png.freepik.com/512/5338/5338322.png")
	await interaction.response.send_message(embed=embed, ephemeral=True)

@bot.event
async def on_message(message):
    global last_message_ended_with_dot, sentence, sentence_authors, sentence_counter

    if message.author.bot:
        return

    if message.channel.id != sentence_builder_channel_id:
        return
    
    if len(message.content.split()) > 1:
        await message.add_reaction('❌')
        return
    
    if sentence_authors and sentence_authors[-1] == message.author and not last_message_ended_with_dot:
        await message.add_reaction('❌')
        return
    
    if sentence_authors and sentence_authors[-1] != message.author and message.content == '.':
        sentence.append(message.content)
        sentence_authors.append(message.author)
        if message.content.endswith('.'):
            sentence_str = ' '.join(sentence)
            if sentence_str.endswith(' .'): 
                sentence_str = sentence_str[:-2] + '.' 
            sentence_channel = bot.get_channel(finished_sentences_channel_id)
            sentence_counter += 1
            sentence_authors_str = ', '.join(user.mention for user in set(sentence_authors))
            await sentence_channel.send(f"> {sentence_str}\nWritten by: {sentence_authors_str} #{sentence_counter}")
            sentence_authors.clear()
            sentence = []
            last_message_ended_with_dot = True
            await message.add_reaction('✅')
        
            with open('sentence_counter.json', 'w') as f:
                json.dump(sentence_counter, f)
            return

        await message.add_reaction('✅')
        return
    
    if message.content.startswith('.'):
        await message.add_reaction('❌')
        return
    
    sentence.append(message.content)
    sentence_authors.append(message.author)
    if message.content.endswith('.'):
        sentence_str = ' '.join(sentence)
        if sentence_str.endswith(' .'): 
            sentence_str = sentence_str[:-2] + '.' 
        sentence_channel = bot.get_channel(finished_sentences_channel_id)
        sentence_counter += 1
        sentence_authors_str = ', '.join(user.mention for user in set(sentence_authors))
        await sentence_channel.send(f"> {sentence_str}\nWritten by: {sentence_authors_str} #{sentence_counter}")
        sentence_authors.clear()
        sentence = []
        last_message_ended_with_dot = True
        await message.add_reaction('✅')
        
        with open('sentence_counter.json', 'w') as f:
            json.dump(sentence_counter, f)
        return

    await message.add_reaction('✅')


bot.run("TOKEN")

