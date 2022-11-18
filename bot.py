import discord
from discord import Option
from discord.ext import commands
import sqlite3 as sq
from discord.ui import View
from config import token
import random

bot = discord.Bot(help_command = None)

guild_id = [993011300147920896]

@bot.slash_command(description = "Start playing Ping Pong with someone.")
async def newgame(ctx, player_2: Option(discord.Member, "Select your opponent.", required=True)):
    con = sq.connect('datas.db')
    cur = con.cursor()
    
    player_2 = player_2
    if player_2.id == ctx.user.id:
        await ctx.respond("Sorry, but you cannot play with yourself.")
    else:
        if player_2.bot:
            await ctx.respond("Sorry, but you cannot play with bot.")
        else:
            try:
                cur.execute(f"""SELECT isplaying FROM `{ctx.user.id}`""").fetchall()
                await ctx.respond("Sorry, but you are actually playing with someone.")
            except:
                try:
                    cur.execute(f"""SELECT isplaying FROM `{player_2.id}`""").fetchall()
                    await ctx.respond("Sorry, but mentioned user is actually playing with someone.")
                except:        
                    cur.execute(f'''CREATE TABLE `{ctx.user.id}`
                                    (isplaying int, opponentid int, turn int)''')
                                    
                    cur.execute(f'''INSERT INTO `{ctx.user.id}` VALUES (1, {player_2.id}, 1)''')
                    
                    con.commit()
                    
                    btns = []
                    
                    class GreenButton(discord.ui.Button):
                        def __init__(self):
                            super().__init__(label="Yes!", style=discord.ButtonStyle.success, emoji="✅")
                            btns.append(self)
                            
                        async def callback(self, interaction):
                            if interaction.user.id == player_2.id:
                                cur.execute(f"""CREATE TABLE `{player_2.id}`
                                                    (isplaying int, opponentid int, turn int)""")
                                                    
                                cur.execute(f"""INSERT INTO `{player_2.id}` VALUES (1, {ctx.user.id}, 0)""")
                                await interaction.message.delete()
                                await interaction.response.send_message(f"Okay! <@{ctx.user.id}> starts! Type **/ping** to play! Enjoy your playing! :)")
                                con.commit()
                                
                            else:
                                await interaction.response.send_message("Sorry, but you are not the asked player.", ephemeral=True)
                                
                                
                    class RedButton(discord.ui.Button):
                        def __init__(self):
                            super().__init__(label = "No!", style=discord.ButtonStyle.danger, emoji="❎")
                            btns.append(self)
                            
                        async def callback(self, interaction):
                            if interaction.user.id == player_2.id:
                                cur.execute(f"""DROP TABLE `{ctx.user.id}`""")
                                await interaction.message.delete()
                                await interaction.response.send_message("Okay!")
                                con.commit()
                                
                            else:
                                await interaction.response.send_message("Sorry, but you are not the asked player.", ephemeral=True)
                                
                    class GreyButton(discord.ui.Button):
                        def __init__(self):
                            super().__init__(label = "Delete request", style=discord.ButtonStyle.primary, emoji="🚫")
                            btns.append(self)
                            
                        async def callback(self, interaction):
                            if interaction.user.id == ctx.user.id:
                                cur.execute(f"""DROP TABLE `{ctx.user.id}`""")
                                async def callback1(interaction):
                                    await interaction.response.send_message("Sorry, but this request has been disabled.", ephemeral=True)
                                    
                                async def callback2(interaction):
                                    await interaction.response.send_message("Sorry, but this request has been disabled.", ephemeral=True)
                                    
                                async def callback3(interaction):
                                    await interaction.response.send_message("Sorry, but this request has been disabled.", ephemeral=True)
                                    
                                btns[0].callback = callback1
                                btns[1].callback = callback2
                                btns[2].callback = callback3
                                
                                con.commit()
                                await interaction.response.send_message("Deleted!")
                                
                            else:
                                await interaction.response.send_message("Sorry, but you are not the command author.", ephemeral=True)
                    
                    greenbtn = GreenButton()
                    redbtn = RedButton()
                    greybtn = GreyButton()
                    view=View()
                    view.add_item(greenbtn)
                    view.add_item(redbtn)
                    view.add_item(greybtn)
                            
                    await ctx.respond(f"<@{player_2.id}>\n\nDo you want to play with <@{ctx.user.id}>? If <@{ctx.user.id}> would like to delete request, use **/finish** or press **Delete Request** button", view=view)
                    
@bot.slash_command(description="Finish playing Ping Pong.")
async def finish(ctx):
    conn = sq.connect('datas.db')
    curs = conn.cursor()
    
    try:
        opponentsid = curs.execute(f"""SELECT opponentid FROM `{ctx.user.id}`""").fetchone()
        i = sum(opponentsid)
        opsids = int(i)
        curs.execute(f"""DROP TABLE `{opsids}`""")
        curs.execute(f"""DROP TABLE `{ctx.user.id}`""")
        await ctx.respond("Game finished!")
    except:
        try:
            curs.execute(f"""DROP TABLE `{ctx.user.id}`""")
            await ctx.respond("Request deleted!")
        except:
            await ctx.respond("Sorry, but you are not playing with anyone.")
    
@bot.slash_command(description="Pong!")
async def ping(ctx):
    conne = sq.connect('datas.db')
    curso = conne.cursor()
    
    try:
        isply = curso.execute(f"""SELECT isplaying FROM `{ctx.user.id}`""").fetchone()
        izply = sum(isply)
        isplaying2 = int(izply)
        
        opntid = curso.execute(f"""SELECT opponentid FROM `{ctx.user.id}`""").fetchone()
        obntid = sum(opntid)
        opponentid2 = int(obntid)
        
        torn = curso.execute(f"""SELECT turn FROM `{ctx.user.id}`""").fetchone()
        cern = sum(torn)
        turn2 = int(cern)
        
        torn = curso.execute(f"""SELECT turn FROM `math{ctx.user.id}`""").fetchone()
        cern = sum(torn)
        turn2 = int(cern)
        
        gameover = 0
                
        if isplaying2 == 1 and opponentid2 != ctx.user.id and turn2 == 0:
            await ctx.respond("Sorry, but it's not your turn.")
            
        elif isplaying2 == 1 and opponentid2 != ctx.user.id and turn2 == 1 and gameover == 6:
            await ctx.respond(f"OOF! You've missed the shot and your opponent is the winner! Congratulations, <@{opponentid2}>!")
            curso.execute(f"""DROP TABLE `{ctx.user.id}`""")
            curso.execute(f"""DROP TABLE `{opponentid2}`""")
            
        elif isplaying2 == 1 and opponentid2 != ctx.user.id and turn2 == 1 and gameover != 6 and mathping != 2:
            curso.execute(f"""UPDATE `{ctx.user.id}` SET turn=0""")
            curso.execute(f"""UPDATE `{opponentid2}` SET turn=1""")
            conne.commit()
            await ctx.respond("Pong!")
        
    except Exception as e:
        print(e)
        await ctx.respond("Sorry, but you are not playing with anyone.")
        
@bot.slash_command(description="Get started with DisPong!")
async def help(ctx):
    await ctx.respond("Hey! I'm **DisPong**! I was created by Gl1tch3dL1m3...he coded me in Python with Pycord library! Anyways, I hope you will have fun with me! Don't be shy and invite someone to play by typing **/newgame**!\n\nHow to play? Just type **/ping**...command author starts first..then command author's opponent and so on! My commands are:\n**/help** - This message\n**/ping** - Play Ping Pong!\n**/newgame** - Start new game!\n**/finish** - Delete your request or finish a game!\n\nOk, that's all! If you need some help or just want to play with others, join our support server: **https://discord.gg/dduRC6cdy3**")
    
bot.run(token)
