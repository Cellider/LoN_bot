import discord
from discord.ext import commands, tasks
import datetime as dt
import asyncio



# set the internal permissions for the bot
intents = discord.Intents.default()
intents.message_content = True
intents.members = True 
intents.reactions = True 

def denied_embed(ctx):
	print("An attempt was made to use the bot on an unauthorized server")
	print('Time of attempt:', dt.datetime.now(dt.UTC).strftime("%H:%M UTC %a"))
	print(f'Server name: {ctx.message.guild.name}')
	print(f'Server id: {ctx.message.guild.id}')
	print(f'Server member count: {ctx.message.guild.member_count}')
	print(f'Server owner name: {ctx.message.guild.owner}')
	print(f'Server owner id: {ctx.message.guild.owner_id}')
	print(f"Message author: {ctx.message.author.name}, ID: {ctx.message.author.id}")
	message = "This bot is being used in this server without the original developer's consent and knowlodge, feel free to DM Cellider about the usage of the bot on this server, the original developer ||Try again MVP rats||"
	embed = discord.Embed(
		colour = discord.Colour.pink(),
		title = 'Denied',
		description = message
		)
	embed.set_image(url="https://c.tenor.com/s0Mmgevkvl0AAAAd/tenor.gif")
	return embed
    
    
inazuma = 537372854942171156
pika = 1039723936188989551
azureknights = 1412919528630784054
darkknights = 1312988977191583784
carnagehub = 654218111003787264
deathquest = 894709957419757620
ncis = 1300731133495087154

allowed_servers = [inazuma, deathquest, ncis, pika, azureknights, darkknights, carnagehub]
# set the prefix
bot = commands.Bot(command_prefix="..", intents=intents, help_command=None)
# remove default help command

# not sure what to do with this, but it might be needed someday
perm_int = 431913036864
#set channel id, aka mfdt channel to only send there the conquest warning
channel_id = 930944141154738186

page_num = 0
original_message = ''
sent_message = ''
name_list = ''

# tell me some data when it starts, it also starts looping the conquest warning message
@bot.event
async def on_ready():
	print('Now working')
    # get server list
	print(bot.guilds)
	await bot.tree.sync()
        
@bot.hybrid_command(name="entoma", aliases=["cutetoma", 'ENTOMA', "CUTETOMA"], description="Entoma dance (best girl)")
async def entoma(ctx):
    # send entoma dance
	if ctx.message.guild.id in allowed_servers:    
		embed = discord.Embed(
          colour = discord.Colour.pink(),
          title = 'Entoma >>>>> Zesshi'
          )
		embed.set_image(url="https://c.tenor.com/SP7T8fUcCcUAAAAd/tenor.gif")
		await ctx.send(embed=embed)
	else:
		embed = denied_embed(ctx)
		denied_message = f'An attempt was made to use the bot on an unauthorized server\nTime of attempt: {dt.datetime.now(dt.UTC).strftime("%H:%M UTC %a")}\nServer name: {ctx.message.guild.name}\nServer id: {ctx.message.guild.id}\nServer member count: {ctx.message.guild.member_count}\nServer owner name: {ctx.message.guild.owner}\nServer owner id: {ctx.message.guild.owner_id}\nMessage author: {ctx.message.author.name}, ID: {ctx.message.author.id}'
		user = await bot.fetch_user(700831435308924979)
		await user.send(denied_message)
		#print("Server invites:")
		#print(await ctx.message.guild.invites())
		await ctx.send(embed=embed)


@bot.hybrid_command(name="help", aliases=['h', "H", "HELP"], description="Help page")
async def help(ctx):
	if ctx.message.guild.id in allowed_servers:
		message = ""
        # open the start file
		with open("start.txt", "r") as file:
			for line in file:
                    # add each line to message
				message += line
		embed = discord.Embed(
			colour = discord.Colour.pink(),
			description = message,
			title = 'Help guide'
			)
		await ctx.send(embed=embed)
	else:
		embed = denied_embed(ctx)
		denied_message = f'An attempt was made to use the bot on an unauthorized server\nTime of attempt: {dt.datetime.now(dt.UTC).strftime("%H:%M UTC %a")}\nServer name: {ctx.message.guild.name}\nServer id: {ctx.message.guild.id}\nServer member count: {ctx.message.guild.member_count}\nServer owner name: {ctx.message.guild.owner}\nServer owner id: {ctx.message.guild.owner_id}\nMessage author: {ctx.message.author.name}, ID: {ctx.message.author.id}'
		user = await bot.fetch_user(700831435308924979)
		await user.send(denied_message)
		await ctx.send(embed=embed)
    
@bot.hybrid_command(name="hello", escription="Say hello")
async def hello(ctx):
    # if user who typed is dt
	if ctx.message.guild.id in allowed_servers:
		if ctx.author.id == 190228540736798720:
			await ctx.send("Hello Pika")
		else:
			await ctx.send(f"Hello {ctx.author}")
	else:
		embed = denied_embed(ctx)
		await ctx.send(embed=embed)
        

class Buttons(discord.ui.View):
    # BUTTONS FOR THE BUILD GUIDE
	@discord.ui.button(label="", style=discord.ButtonStyle.primary, emoji="<:button_back:1383100829979902124>")
    # def what happens once you click the button
	async def button_press_2(self, button, interaction):
        # PAGE FOR BUILD GUIDE
		global page_num
		if page_num > 0:
			page_num -= 1
		elif page_num == 0:
			page_num = 5
		new_message = original_message

		for name_line in name_list[page_num]:
			new_message += name_line

		embed = discord.Embed(
			colour = discord.Colour.pink(),
			description = new_message,
			title = 'Build Guide'
		)

		await discord.Message.edit(sent_message, view=Buttons(), embed=embed)
    
    # SECOND BUTTON
	@discord.ui.button(label="", style=discord.ButtonStyle.primary, emoji="<:button_forward:1383101079776133260>")
	async def button_press(self, button, interaction):
		global page_num
		if page_num < 6:
			page_num += 1
		elif page_num == 5:
			page_num = 0
		new_message = original_message

		for name_line in name_list[page_num]:
			new_message += name_line
		embed = discord.Embed(
			colour = discord.Colour.pink(),
			description = new_message,
			title = 'Build Guide'
		)

		await discord.Message.edit(sent_message, view=Buttons(), embed=embed)

@bot.hybrid_command(name="build", aliases=['b', "B", "BUILD"], description="You can type the whole name on the first name, example: /build first_name: mage albedo")
async def build(ctx, first_name="", second_name=""):
	if ctx.message.guild.id in allowed_servers:
		global page_num
		page_num = 0
        # put the name that the user typed into a single word
		full_name = first_name + " " + second_name
        # intiate some variables
		add_to_message = False
		image_file = ""
		message = ""
        # if full name is not empty we open the file and look for the character
		if full_name != " ":
			with open("relics_data.txt", "r") as file:
				for line in file:
					if "end guide" in line and add_to_message:
                        # if we reach end guide line, we stop the loop
						add_to_message = False
						break
					if "image_file" in line and add_to_message:
                        # if we find image_file in the line, get the link into a variable
						image_file = line[11:-1]
						continue
					elif add_to_message:
                        # add each line to message
						message += line
                    # if we find the name that the user typed and its with the workd "begin guide"
					if "begin guide" in line and full_name.lower() in line:
						add_to_message = True
                        # always make sure to reset the image file
						image_file = ""

			embed = discord.Embed(
				colour = discord.Colour.pink(),
				description = message,
				title = f'{full_name.title()} guide'
				)
            # if image file is not empty
			if image_file != "":
				image = discord.File(image_file, filename="image.png")
				embed.set_image(url="attachment://image.png")

				await ctx.send(embed=embed, file=image)

            # if we reach end of file, it means that we did not find the character the user typed for
			elif line == "end of file":


				embed.set_footer(text = "If you typed the name correctly, the unit may not be yet on the bot or a it may be a typo on the developer side \nPing Cellider to check it or to add the unit you want\n\nIf you're using a slash command, you can put the whole name on the 'first name' section.\n\nExample:\n/build first_name: mage albedo\n\nType ..b for the full list of available characters")
				embed.set_image(url="https://c.tenor.com/9-1s3l5Ag4cAAAAd/tenor.gif")

				await ctx.send(embed=embed)
			else:
				await ctx.send(embed=embed)
		else:
            # if the user hasnt typed any name, we give the list of available characters
            # Create variables needed in order to separate the names into different lists so we can change pages
            # global these so we can change their values globaly
			global sent_message, original_message, name_list
			add_to_message = False
			message = ""
			add_to_name_list = False
			line_count = 0
			name_list_1 = []
			name_list_2 = []
			name_list_3 = []
			name_list_4 = []
			name_list_5 = []
			name_list_6 = []
			final_name_list = [name_list_1, name_list_2, name_list_3, name_list_4,name_list_5, name_list_6]
			with open("relics_data.txt", "r") as file:
				for line in file:
					if "end list" in line and add_to_message:
						add_to_message = False
						continue
					if add_to_message:
						message += line
					if "begin list" in line:
						add_to_message = True
						continue

					if "end name list" in line:
						add_to_name_list = False
						break

					if add_to_name_list:
						line_count +=1
						if line_count <= 10:
   							name_list_1.append(line)
						elif line_count <= 20:
							name_list_2.append(line)
						elif line_count <= 30:
							name_list_3.append(line)
						elif line_count <= 40:
							name_list_4.append(line)
						elif line_count <= 50:
							name_list_5.append(line)
						elif line_count <= 60:
							name_list_6.append(line)

					if "begin name list" in line:
						add_to_name_list = True
						continue

            # make the default message, this will show up the first 10 names always
			current_list = final_name_list[page_num]
			original_message = message
			name_list = final_name_list
			for name_line in current_list:
				message += name_line

			embed = discord.Embed(
				colour = discord.Colour.pink(),
				description = message,
				title = 'Build Guide'
				)
			sent_message = await ctx.send(embed=embed, view=Buttons())
	else:
		embed = denied_embed(ctx)
		denied_message = f'An attempt was made to use the bot on an unauthorized server\nTime of attempt: {dt.datetime.now(dt.UTC).strftime("%H:%M UTC %a")}\nServer name: {ctx.message.guild.name}\nServer id: {ctx.message.guild.id}\nServer member count: {ctx.message.guild.member_count}\nServer owner name: {ctx.message.guild.owner}\nServer owner id: {ctx.message.guild.owner_id}\nMessage author: {ctx.message.author.name}, ID: {ctx.message.author.id}'
		user = await bot.fetch_user(700831435308924979)
		await user.send(denied_message)
		await ctx.send(embed=embed)  
        
        
        
        
        
        
@bot.hybrid_command(name="realm", aliases=['r', "R", "REALM"], description="Write the realm to see said guide, ex: ..realm ainz")
async def build(ctx, realm_type = " ", stage = " "):
	if ctx.message.guild.id in allowed_servers:
		global page_num
        # intiate some variables
		add_to_message = False
		image_file = ""
		message = ""
		realm_found = False
        # if full name is not empty we open the file and look for the character
		if realm_type != " ":
			with open("realm_data.txt", "r") as file:
				if stage == " ":
					for line in file:
						if "end realm guide" in line and add_to_message:
                        	# if we reach end guide line, we stop the loop
							add_to_message = False
							break
						if "image_file" in line and add_to_message:
                        	# if we find image_file in the line, get the link into a variable
							image_file = line[11:-1]
							continue
						elif add_to_message:
                       	 # add each line to message
							message += line
                   		 # if we find the name that the user typed and its with the workd "begin guide"
						if "begin realm guide" in line and realm_type.lower() in line:
							add_to_message = True
                        	# always make sure to reset the image file
							image_file = ""
				if stage != " ":
					for line in file:
						if realm_type.lower() in line:
							realm_found = True
						if "end stage guide" in line and add_to_message:
							# if we reach end guide line, we stop the loop
							add_to_message = False
							break
						if "image_file" in line and add_to_message:
							# if we find image_file in the line, get the link into a variable
							image_file = line[11:-1]
							continue
						elif add_to_message:
						# add each line to message
							message += line
						# if we find the name that the user typed and its with the workd "begin guide"
						if "begin stage guide" in line and stage in line and realm_found:
							add_to_message = True
							# always make sure to reset the image file
							image_file = ""
                    
			embed = discord.Embed(
				colour = discord.Colour.pink(),
				description = message,
				title = f'{realm_type.title()} Realm Guide'
				)
            # if image file is not empty
			if image_file != "":
				image = discord.File(image_file, filename="image.png")
				embed.set_image(url="attachment://image.png")

				await ctx.send(embed=embed, file=image)

            # if we reach end of file, it means that we did not find the character the user typed for
			elif line == "end of file":
                
				embed.set_footer(text = "Realm type not found, make sure you've typed the realm name correctly, check ' ..realm ' for the available realms")
				embed.set_image(url="https://c.tenor.com/9-1s3l5Ag4cAAAAd/tenor.gif")

				await ctx.send(embed=embed)
			else:
				await ctx.send(embed=embed)
		else:
            # if the user hasnt typed any name, we give the list of available characters
            # Create variables needed in order to separate the names into different lists so we can change pages
            # global these so we can change their values globaly
			add_to_message = False
			message = ""
			add_to_name_list = False
			with open("realm_data.txt", "r") as file:
				for line in file:
					if "end list" in line and add_to_message:
						add_to_message = False
						continue
					if add_to_message:
						message += line
					if "begin list" in line:
						add_to_message = True
						continue

			embed = discord.Embed(
				colour = discord.Colour.pink(),
				description = message,
				title = 'Realm Guide'
				)
			sent_message = await ctx.send(embed=embed)
	else:
		embed = denied_embed(ctx)
		denied_message = f'An attempt was made to use the bot on an unauthorized server\nTime of attempt: {dt.datetime.now(dt.UTC).strftime("%H:%M UTC %a")}\nServer name: {ctx.message.guild.name}\nServer id: {ctx.message.guild.id}\nServer member count: {ctx.message.guild.member_count}\nServer owner name: {ctx.message.guild.owner}\nServer owner id: {ctx.message.guild.owner_id}\nMessage author: {ctx.message.author.name}, ID: {ctx.message.author.id}'
		user = await bot.fetch_user(700831435308924979)
		await user.send(denied_message)
		await ctx.send(embed=embed) 
        
        
@bot.hybrid_command(name="treasury", aliases=['t', "T", "TREASURY"], description="Write the treasury to see said guide, ex: ..treasury dragon")
async def build(ctx, treasury_type = " "):
	if ctx.message.guild.id in allowed_servers:
        # intiate some variables
		add_to_message = False
		image_file = ""
		message = ""
		treasury = False
        # if full name is not empty we open the file and look for the character
		if treasury_type != " ":
			with open("treasury_data.txt", "r") as file:
				for line in file:
					if "end stage guide" in line and add_to_message:
						# if we reach end guide line, we stop the loop
						add_to_message = False
						break
					if "image_file" in line and add_to_message:
						# if we find image_file in the line, get the link into a variable
						image_file = line[11:-1]
						continue
					elif add_to_message:
						# add each line to message
						message += line
						# if we find the name that the user typed and its with the workd "begin guide"
					if "begin treasury guide" in line and treasury_type.lower() in line:
						add_to_message = True
						# always make sure to reset the image file
						image_file = ""
                    
			embed = discord.Embed(
				colour = discord.Colour.pink(),
				description = message,
				title = f'{treasury_type.title()} Treasury Guide'
				)
            # if image file is not empty
			if image_file != "":
				image = discord.File(image_file, filename="image.png")
				embed.set_image(url="attachment://image.png")

				await ctx.send(embed=embed, file=image)

            # if we reach end of file, it means that we did not find the character the user typed for
			elif line == "end of file":
                
				embed.set_footer(text = "Treasury type not found, make sure you've typed the realm name correctly, check ' ..realm ' for the available realms")
				embed.set_image(url="https://c.tenor.com/9-1s3l5Ag4cAAAAd/tenor.gif")

				await ctx.send(embed=embed)
			else:
				await ctx.send(embed=embed)
		else:
            # if the user hasnt typed any name, we give the list of available characters
            # Create variables needed in order to separate the names into different lists so we can change pages
            # global these so we can change their values globaly
			add_to_message = False
			message = ""
			add_to_name_list = False
			with open("treasury_data.txt", "r") as file:
				for line in file:
					if "end list" in line and add_to_message:
						add_to_message = False
						continue
					if add_to_message:
						message += line
					if "begin list" in line:
						add_to_message = True
						continue

			embed = discord.Embed(
				colour = discord.Colour.pink(),
				description = message,
				title = 'Treasury Guide'
				)
			sent_message = await ctx.send(embed=embed)
	else:
		embed = denied_embed(ctx)
		denied_message = f'An attempt was made to use the bot on an unauthorized server\nTime of attempt: {dt.datetime.now(dt.UTC).strftime("%H:%M UTC %a")}\nServer name: {ctx.message.guild.name}\nServer id: {ctx.message.guild.id}\nServer member count: {ctx.message.guild.member_count}\nServer owner name: {ctx.message.guild.owner}\nServer owner id: {ctx.message.guild.owner_id}\nMessage author: {ctx.message.author.name}, ID: {ctx.message.author.id}'
		user = await bot.fetch_user(700831435308924979)
		await user.send(denied_message)
		await ctx.send(embed=embed) 
        

bot.run("MTM0ODY5NDMyNjE1NDM2MjkwMA.Gio17v.QYSGIQ5-lUZvHNasxu7Qa0W1UwjF5xTq0VxMJ0")