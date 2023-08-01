###### DisPong by @glitchedlime ######

# Last changes: 1. August 2023
# Commands count: 7
# Bot's version: v.1.2

# Feel free to use this script, but don't steal it (selling, pretending to be creator of this script, etc.)!

# LINUX NOTE: If you are running on Linux, replace 'cls' with 'clear' (in consoleclear function)!

import discord
from discord import Option
from discord.ext import commands
import sqlite3 as sq
from discord.ui import View
from config import token
import random
import os

bot = discord.Bot(help_command = None)

# Show message in console when ready + status showing bot's version

@bot.event
async def on_ready():
    print(f"{bot.user} is ready!")
    await bot.change_presence(activity=discord.Game(name="v1.2"))
    
# Console clear (Linux: replace 'cls' with 'clear')

def consoleclear():
    os.system("cls")
    
# New game command

@bot.slash_command(description = "Start playing Ping Pong with someone.")
async def duel(ctx, opponent: Option(discord.Member, "Select your opponent.", required=True)):
    con = sq.connect('datas.db')
    cur = con.cursor()

    conn2 = sq.connect('stats.db')
    curs2 = conn2.cursor()
    
    player_2 = opponent
    
    if player_2.id == ctx.user.id:
        await ctx.respond("Sorry, but you cannot play with yourself. <:crosspong:1134110291311992962>")
        con.close()
    else:
        if player_2.bot:
            await ctx.respond("Sorry, but you cannot play with a bot. <:crosspong:1134110291311992962>")
            con.close()
        else:
            try:
                cur.execute(f"""SELECT isplaying FROM `{ctx.user.id}`""").fetchall()
                await ctx.respond("Sorry, but you are actually playing with someone. <:crosspong:1134110291311992962>")
                consoleclear()
                con.close()
            except:
                try:
                    cur.execute(f"""SELECT isplaying FROM `{player_2.id}`""").fetchall()
                    await ctx.respond("Sorry, but mentioned user is actually playing with someone. <:crosspong:1134110291311992962>")
                    con.close()
                    consoleclear()
                except:        
                    cur.execute(f'''CREATE TABLE `{ctx.user.id}` (isplaying int, opponentid int, turn int, rps int, rpsbot int, isfirstping int)''')
                                    
                    cur.execute(f'''INSERT INTO `{ctx.user.id}` VALUES (1, {player_2.id}, 1, 0, 6, 0)''')
                    
                    con.commit()
                    
                    btns = []
                    
                    class GreenButton(discord.ui.Button):
                        def __init__(self):
                            super().__init__(label="Yes!", style=discord.ButtonStyle.success, emoji="<:tickpong:1134110509872984095>")
                            btns.append(self)
                            
                        async def callback(self, interaction):
                            con = sq.connect('datas.db')
                            cur = con.cursor()

                            try:
                                # Random selection, bot needs to know if tables exists
                                cur.execute(f"""SELECT turn FROM `{ctx.user.id}`""").fetchall()

                                if interaction.user.id == player_2.id:
                                    cur.execute(f"""CREATE TABLE `{player_2.id}` (isplaying int, opponentid int, turn int, rps int, rpsbot int, isfirstping int)""")
                                                        
                                    cur.execute(f"""INSERT INTO `{player_2.id}` VALUES (1, {ctx.user.id}, 0, 0, 6, 0)""")
                                    upd1 = curs2.execute(f"""SELECT totalgames FROM main""").fetchone()
                                    upd2 = sum(upd1)
                                    upd = int(upd2)
                                    upd += 1
                                    curs2.execute(f"""UPDATE main SET totalgames={upd}""")
                                    upd1 = curs2.execute(f"""SELECT currentgames FROM main""").fetchone()
                                    upd2 = sum(upd1)
                                    upd = int(upd2)
                                    upd += 1
                                    curs2.execute(f"""UPDATE main SET currentgames={upd}""")
                                    await interaction.message.delete()
                                    await interaction.response.send_message(f"Okay! <@{ctx.user.id}> starts! Type </ping:999267081629487196> to play! Enjoy your playing! <:tickpong:1134110509872984095>")
                                    con.commit()
                                    con.close()
                                    conn2.commit()
                                    conn2.close()
                                    
                                else:
                                    await interaction.response.send_message("Sorry, but you are not the asked player. <:crosspong:1134110291311992962>", ephemeral=True)
                                    con.close()
                                    consoleclear()

                            except:
                                await interaction.response.send_message("Sorry, but this request has been disabled. <:crosspong:1134110291311992962>", ephemeral=True)
                                
                                
                    class RedButton(discord.ui.Button):
                        def __init__(self):
                            super().__init__(label = "No!", style=discord.ButtonStyle.danger, emoji="<:crosspong:1134110291311992962>")
                            btns.append(self)
                            
                        async def callback(self, interaction):
                            con = sq.connect('datas.db')
                            cur = con.cursor()

                            try:
                                # Random selection, bot needs to know if this table exists
                                cur.execute(f"""SELECT turn FROM `{ctx.user.id}`""").fetchall()

                                if interaction.user.id == player_2.id:
                                    cur.execute(f"""DROP TABLE `{ctx.user.id}`""")
                                    await interaction.message.delete()
                                    await interaction.response.send_message("Alright, so we are not playing this time! <:crosspong:1134110291311992962>")
                                    con.commit()
                                    con.close()
                                    
                                else:
                                    await interaction.response.send_message("Sorry, but you are not the asked player. <:crosspong:1134110291311992962>", ephemeral=True)
                                    con.close()
                                    consoleclear()

                            except:
                                await interaction.response.send_message("Sorry, but this request has been disabled. <:crosspong:1134110291311992962>", ephemeral=True)
                                
                    class BlueButton(discord.ui.Button):
                        def __init__(self):
                            super().__init__(label = "Delete request!", style=discord.ButtonStyle.primary, emoji="<:brokenpong:1134116285014360206>")
                            btns.append(self)
                            
                        async def callback(self, interaction):
                            con = sq.connect('datas.db')
                            cur = con.cursor()

                            try:
                                # Random selection, bot needs to know if this table exists
                                cur.execute(f"""SELECT turn FROM `{ctx.user.id}`""").fetchall()

                                if interaction.user.id == ctx.user.id:
                                    cur.execute(f"""DROP TABLE `{ctx.user.id}`""")
                                    async def callback1(interaction):
                                        await interaction.response.send_message("Sorry, but this request has been disabled. <:crosspong:1134110291311992962>", ephemeral=True)
                                        consoleclear()
                                        con.close()
                                        
                                    btns[0].callback = callback1
                                    btns[1].callback = callback1
                                    btns[2].callback = callback1
                                    
                                    con.commit()
                                    await interaction.response.send_message("Deleted! <:tickpong:1134110509872984095>")
                                    con.close()
                                    
                                else:
                                    await interaction.response.send_message("Sorry, but you are not the command author. <:crosspong:1134110291311992962>", ephemeral=True)
                                    consoleclear()
                                    con.close()

                            except:
                                await interaction.response.send_message("Sorry, but this request has been disabled. <:crosspong:1134110291311992962>", ephemeral=True)
                    
                    greenbtn = GreenButton()
                    redbtn = RedButton()
                    greybtn = BlueButton()
                    view=View()
                    view.add_item(greenbtn)
                    view.add_item(redbtn)
                    view.add_item(greybtn)
                            
                    await ctx.respond(f"<@{player_2.id}>\n\nDo you want to play with <@{ctx.user.id}>? If <@{ctx.user.id}> would like to delete request, use </finish:999267081629487195> or press **Delete Request** button! <:circlepong:1134110288438894654>", view=view)

# Finish command
                    
@bot.slash_command(description="Finish playing Ping Pong.")
async def finish(ctx):
    conn = sq.connect('datas.db')
    curs = conn.cursor()

    conn2 = sq.connect('stats.db')
    curs2 = conn2.cursor()
    
    try:
        opponentsid = curs.execute(f"""SELECT opponentid FROM `{ctx.user.id}`""").fetchone()
        i = sum(opponentsid)
        opsids = int(i)
        curs.execute(f"""DROP TABLE `{opsids}`""")
        curs.execute(f"""DROP TABLE `{ctx.user.id}`""")
        upd1 = curs2.execute(f"""SELECT currentgames FROM main""").fetchone()
        upd2 = sum(upd1)
        upd = int(upd2)
        upd -= 1
        curs2.execute(f"""UPDATE main SET currentgames={upd}""")
        conn.commit()
        conn.close()
        conn2.commit()
        conn2.close()
        await ctx.respond("Game finished! <:tickpong:1134110509872984095>")
        
    except:
        try:
            isbotid = curs.execute(f"""SELECT opponentid FROM `{ctx.user.id}`""").fetchone()
            i = sum(isbotid)
            opsids = int(i)
            curs.execute(f"""DROP TABLE `{ctx.user.id}`""")
            upd1 = curs2.execute(f"""SELECT botgames FROM main""").fetchone()
            upd2 = sum(upd1)
            upd = int(upd2)
            upd -= 1
            curs2.execute(f"""UPDATE main SET botgames={upd}""")
            conn2.commit()
            conn2.close()
            conn.commit()
            conn.close()
            
            if opsids == bot.user.id:
                await ctx.respond("Game finished! <:tickpong:1134110509872984095>")
                
            else:
                await ctx.respond("Request deleted! <:tickpong:1134110509872984095>")
            
        except:
            await ctx.respond("Sorry, but you are not playing with anyone. <:crosspong:1134110291311992962>")
    
# Ping command (to ping a ball)
    
@bot.slash_command(description="Pong!")
async def ping(ctx):
    conne = sq.connect('datas.db')
    curso = conne.cursor()

    connn2 = sq.connect('stats.db')
    curs2 = connn2.cursor()

    async def rps():
        # 0 - Not in-game
        # 1 - Waiting for turn
        # 2 - Deciding
        # 3 - Rock
        # 4 - Scissors
        # 5 - Paper
        # 6 - Cannot play

        conn = sq.connect('datas.db')
        cur = conn.cursor()

        conn2 = sq.connect('stats.db')
        cur2 = conn2.cursor()

        rpsbot1 = cur.execute(f"""SELECT rpsbot FROM `{ctx.user.id}`""").fetchone()
        rpsbot2 = sum(rpsbot1)
        rpsbot = int(rpsbot2)

        opponentid1 = cur.execute(f"""SELECT opponentid FROM `{ctx.user.id}`""").fetchone()
        opponentid2 = sum(opponentid1)
        opponentid = int(opponentid2)

        btns = []

        try:
            if rpsbot == 6:
                cur.execute(f"""UPDATE `{opponentid}` SET rps=1""")
                cur.execute(f"""UPDATE `{ctx.user.id}` SET rps=2""")
                conn.commit()

            else:
                cur.execute(f"""UPDATE `{ctx.user.id}` SET rps=2""")
                cur.execute(f"""UPDATE `{ctx.user.id}` SET rpsbot=1""")
                conn.commit()

            class RockButton(discord.ui.Button):
                def __init__(self):
                    super().__init__(label="Rock", style=discord.ButtonStyle.primary, emoji="🪨")
                    btns.append(self)
                    
                async def callback(self, interaction):
                    conn = sq.connect('datas.db')
                    cur = conn.cursor()

                    rps1 = cur.execute(f"""SELECT rps FROM `{ctx.user.id}`""").fetchone()
                    rps2 = sum(rps1)
                    rps = int(rps2)

                    if rpsbot == 6:
                        opporps1 = cur.execute(f"""SELECT rps FROM `{opponentid}`""").fetchone()
                        opporps2 = sum(opporps1)
                        opporps = int(opporps2)

                    else:
                        opporps1 = cur.execute(f"""SELECT rpsbot FROM `{ctx.user.id}`""").fetchone()
                        opporps2 = sum(opporps1)
                        opporps = int(opporps2)

                    if interaction.user.id == ctx.user.id and rps == 2:
                        if rpsbot == 6:
                            cur.execute(f"""UPDATE `{ctx.user.id}` SET rps=3""")
                            cur.execute(f"""UPDATE `{opponentid}` SET rps=2""")
                            conn.commit()
                            await interaction.message.edit(f"Okay! Now it's <@{opponentid}>'s turn to choose! 👉")
                            await interaction.response.defer()
                        else:
                            cur.execute(f"""UPDATE `{ctx.user.id}` SET rps=3""")

                            gennum = random.randint(1,3)

                            if gennum == 1:
                                await interaction.message.edit(f"Player: 🪨\nBot: 🪨\n\nDraw! Now it's bot's turn to ping a ball! 🤜🤛")
                                cur.execute(f"""UPDATE `{ctx.user.id}` SET rps=0""")
                                cur.execute(f"""UPDATE `{ctx.user.id}` SET rpsbot=0""")
                                cur.execute(f"""UPDATE `{ctx.user.id}` SET turn=0""")

                                await ctx.respond(":robot:: Pong! 🏓")
                                cur.execute(f"""UPDATE `{ctx.user.id}` SET turn=1""")
                                conn.commit()
                                upd1 = cur2.execute(f"""SELECT ballspinged FROM main""").fetchone()
                                upd2 = sum(upd1)
                                upd = int(upd2)
                                upd += 1
                                cur2.execute(f"""UPDATE main SET ballspinged={upd}""")
                                conn2.commit()
                                conn2.close()

                                await interaction.response.defer()

                            elif gennum == 2:
                                await interaction.message.edit(f"Player: 🪨\nBot: ✂️\n\nPlayer won! Bot missed the shot, so <@{ctx.user.id}> has won this match! **Game over!** 🏆")
                                cur.execute(f"""DROP TABLE `{ctx.user.id}`""")
                                conn.commit()
                                upd1 = cur2.execute(f"""SELECT botgames FROM main""").fetchone()
                                upd2 = sum(upd1)
                                upd = int(upd2)
                                upd -= 1
                                cur2.execute(f"""UPDATE main SET botgames={upd}""")
                                conn2.commit()
                                conn2.close()

                                await interaction.response.defer()

                            else:
                                await interaction.message.edit(f"Player: 🪨\nBot: 📜\n\nBot won! Now it's bot's turn to ping a ball! 🏓")
                                cur.execute(f"""UPDATE `{ctx.user.id}` SET rps=0""")
                                cur.execute(f"""UPDATE `{ctx.user.id}` SET rpsbot=0""")
                                cur.execute(f"""UPDATE `{ctx.user.id}` SET turn=0""")

                                await ctx.respond(":robot:: Pong! 🏓")
                                cur.execute(f"""UPDATE `{ctx.user.id}` SET turn=1""")
                                conn.commit()
                                upd1 = cur2.execute(f"""SELECT ballspinged FROM main""").fetchone()
                                upd2 = sum(upd1)
                                upd = int(upd2)
                                upd += 1
                                cur2.execute(f"""UPDATE main SET ballspinged={upd}""")
                                conn2.commit()
                                conn2.close()

                                await interaction.response.defer()
                                

                    elif interaction.user.id == opponentid and opporps == 2:
                        cur.execute(f"""UPDATE `{opponentid}` SET rps=3""")
                        conn.commit()
                        rps11 = cur.execute(f"""SELECT rps FROM `{ctx.user.id}`""").fetchone()
                        rps12 = sum(rps11)
                        rps1 = int(rps12)

                        if rpsbot == 6:
                            rps21 = cur.execute(f"""SELECT rps FROM `{opponentid}`""").fetchone()
                            rps22 = sum(rps21)
                            rps2 = int(rps22)

                        if rps1 == 3 and rps2 == 3:
                            await interaction.message.edit(f"Player 1: 🪨\nPlayer 2: 🪨\n\nDraw! Now it's <@{opponentid}>'s turn to ping a ball! 🤜🤛")
                            cur.execute(f"""UPDATE `{ctx.user.id}` SET turn=0""")
                            cur.execute(f"""UPDATE `{opponentid}` SET turn=1""")
                            cur.execute(f"""UPDATE `{ctx.user.id}` SET rps=0""")
                            cur.execute(f"""UPDATE `{opponentid}` SET rps=0""")
                            conn.commit()
                            upd1 = cur2.execute(f"""SELECT ballspinged FROM main""").fetchone()
                            upd2 = sum(upd1)
                            upd = int(upd2)
                            upd += 1
                            cur2.execute(f"""UPDATE main SET ballspinged={upd}""")
                            conn2.commit()
                            conn2.close()
                            await interaction.response.defer()

                        elif rps1 == 4 and rps2 == 3:
                            await interaction.message.edit(f"Player 1: 🪨\nPlayer 2: ✂️\n\nPlayer 1 won! <@{opponentid}> missed the shot, so <@{ctx.user.id}> won this match! **Game over!** 🏆")
                            cur.execute(f"""DROP TABLE `{ctx.user.id}`""")
                            cur.execute(f"""DROP TABLE `{opponentid}`""")
                            conn.commit()
                            upd1 = cur2.execute(f"""SELECT currentgames FROM main""").fetchone()
                            upd2 = sum(upd1)
                            upd = int(upd2)
                            upd -= 1
                            cur2.execute(f"""UPDATE main SET currentgames={upd}""")
                            conn2.commit()
                            conn2.close()
                            await interaction.response.defer()

                        elif rps1 == 5 and rps2 == 3:
                            await interaction.message.edit(f"Player 1: 🪨\nPlayer 2: 📜\n\nPlayer 2 won! Now it's <@{opponentid}>'s turn to ping a ball! 🏓")
                            cur.execute(f"""UPDATE `{ctx.user.id}` SET turn=0""")
                            cur.execute(f"""UPDATE `{opponentid}` SET turn=1""")
                            cur.execute(f"""UPDATE `{ctx.user.id}` SET rps=0""")
                            cur.execute(f"""UPDATE `{opponentid}` SET rps=0""")
                            conn.commit()
                            upd1 = cur2.execute(f"""SELECT ballspinged FROM main""").fetchone()
                            upd2 = sum(upd1)
                            upd = int(upd2)
                            upd += 1
                            cur2.execute(f"""UPDATE main SET ballspinged={upd}""")
                            conn2.commit()
                            conn2.close()
                            await interaction.response.defer()

                        if rpsbot == 6:
                            cur.execute(f"""UPDATE `{ctx.user.id}` SET rps=0""")
                            cur.execute(f"""UPDATE `{opponentid}` SET rps=0""")
                            conn.close()

                    else:
                        await interaction.response.send_message("Sorry, but it's not your turn or you're not playing! <:crosspong:1134110291311992962>", ephemeral=True)

            class ScissorsButton(discord.ui.Button):
                def __init__(self):
                    super().__init__(label="Scissors", style=discord.ButtonStyle.primary, emoji="✂️")
                    btns.append(self)
                    
                async def callback(self, interaction):
                    conn = sq.connect('datas.db')
                    cur = conn.cursor()

                    rps1 = cur.execute(f"""SELECT rps FROM `{ctx.user.id}`""").fetchone()
                    rps2 = sum(rps1)
                    rps = int(rps2)

                    if rpsbot == 6:
                        opporps1 = cur.execute(f"""SELECT rps FROM `{opponentid}`""").fetchone()
                        opporps2 = sum(opporps1)
                        opporps = int(opporps2)

                    else:
                        opporps1 = cur.execute(f"""SELECT rpsbot FROM `{ctx.user.id}`""").fetchone()
                        opporps2 = sum(opporps1)
                        opporps = int(opporps2)

                    if interaction.user.id == ctx.user.id and rps == 2:
                        if rpsbot == 6:
                            cur.execute(f"""UPDATE `{ctx.user.id}` SET rps=4""")
                            cur.execute(f"""UPDATE `{opponentid}` SET rps=2""")
                            conn.commit()
                            await interaction.message.edit(f"Okay! Now it's <@{opponentid}>'s turn to choose! 👉")
                            await interaction.response.defer()

                        else:
                            cur.execute(f"""UPDATE `{ctx.user.id}` SET rps=4""")

                            gennum = random.randint(1,3)

                            if gennum == 1:
                                await interaction.message.edit(f"Player: ✂️\nBot: 🪨\n\nBot won! Now it's bot's turn to ping a ball! 🏓")
                                cur.execute(f"""UPDATE `{ctx.user.id}` SET rps=0""")
                                cur.execute(f"""UPDATE `{ctx.user.id}` SET rpsbot=0""")
                                cur.execute(f"""UPDATE `{ctx.user.id}` SET turn=0""")

                                await ctx.respond(":robot:: Pong! 🏓")
                                cur.execute(f"""UPDATE `{ctx.user.id}` SET turn=1""")
                                conn.commit()
                                upd1 = cur2.execute(f"""SELECT ballspinged FROM main""").fetchone()
                                upd2 = sum(upd1)
                                upd = int(upd2)
                                upd += 1
                                cur2.execute(f"""UPDATE main SET ballspinged={upd}""")
                                conn2.commit()
                                conn2.close()

                                await interaction.response.defer()

                            elif gennum == 2:
                                await interaction.message.edit(f"Player: ✂️\nBot: ✂️\n\nDraw! Now it's bot's turn to ping a ball! 🤜🤛")
                                cur.execute(f"""UPDATE `{ctx.user.id}` SET rps=0""")
                                cur.execute(f"""UPDATE `{ctx.user.id}` SET rpsbot=0""")
                                cur.execute(f"""UPDATE `{ctx.user.id}` SET turn=0""")

                                await ctx.respond(":robot:: Pong! 🏓")
                                cur.execute(f"""UPDATE `{ctx.user.id}` SET turn=1""")
                                conn.commit()
                                upd1 = cur2.execute(f"""SELECT ballspinged FROM main""").fetchone()
                                upd2 = sum(upd1)
                                upd = int(upd2)
                                upd += 1
                                cur2.execute(f"""UPDATE main SET ballspinged={upd}""")
                                conn2.commit()
                                conn2.close()

                                await interaction.response.defer()

                            else:
                                await interaction.message.edit(f"Player: ✂️\nBot: 📜\n\nPlayer won! Bot missed the shot, so <@{ctx.user.id}> has won this match! **Game over!** 🏆")
                                cur.execute(f"""DROP TABLE `{ctx.user.id}`""")
                                conn.commit()
                                upd1 = cur2.execute(f"""SELECT botgames FROM main""").fetchone()
                                upd2 = sum(upd1)
                                upd = int(upd2)
                                upd -= 1
                                cur2.execute(f"""UPDATE main SET botgames={upd}""")
                                conn2.commit()
                                conn2.close()

                                await interaction.response.defer()

                    elif interaction.user.id == opponentid and opporps == 2:
                        cur.execute(f"""UPDATE `{opponentid}` SET rps=4""")
                        conn.commit()

                        rps11 = cur.execute(f"""SELECT rps FROM `{ctx.user.id}`""").fetchone()
                        rps12 = sum(rps11)
                        rps1 = int(rps12)

                        rps21 = cur.execute(f"""SELECT rps FROM `{opponentid}`""").fetchone()
                        rps22 = sum(rps21)
                        rps2 = int(rps22)

                        if rps1 == 4 and rps2 == 4:
                            await interaction.message.edit(f"Player 1: ✂️\nPlayer 2: ✂️\n\nDraw! Now it's <@{opponentid}>'s turn to ping a ball! 🤜🤛")
                            cur.execute(f"""UPDATE `{ctx.user.id}` SET turn=0""")
                            cur.execute(f"""UPDATE `{opponentid}` SET turn=1""")
                            cur.execute(f"""UPDATE `{ctx.user.id}` SET rps=0""")
                            cur.execute(f"""UPDATE `{opponentid}` SET rps=0""")
                            conn.commit()
                            upd1 = cur2.execute(f"""SELECT ballspinged FROM main""").fetchone()
                            upd2 = sum(upd1)
                            upd = int(upd2)
                            upd += 1
                            cur2.execute(f"""UPDATE main SET ballspinged={upd}""")
                            conn2.commit()
                            conn2.close()
                            await interaction.response.defer()

                        elif rps1 == 3 and rps2 == 4:
                            await interaction.message.edit(f"Player 1: ✂️ 🪨\nPlayer 2: 🪨\n\nPlayer 2 won! Now it's <@{opponentid}>'s turn to ping a ball! 🏓")
                            cur.execute(f"""UPDATE `{ctx.user.id}` SET turn=0""")
                            cur.execute(f"""UPDATE `{opponentid}` SET turn=1""")
                            cur.execute(f"""UPDATE `{ctx.user.id}` SET rps=0""")
                            cur.execute(f"""UPDATE `{opponentid}` SET rps=0""")
                            conn.commit()
                            upd1 = cur2.execute(f"""SELECT ballspinged FROM main""").fetchone()
                            upd2 = sum(upd1)
                            upd = int(upd2)
                            upd += 1
                            cur2.execute(f"""UPDATE main SET ballspinged={upd}""")
                            conn2.commit()
                            conn2.close()
                            await interaction.response.defer()

                        elif rps1 == 5 and rps2 == 4:
                            await interaction.message.edit(f"Player 1: ✂️\nPlayer 2: 📜\n\nPlayer 1 won! <@{opponentid}> missed the shot, so <@{ctx.user.id}> won this match! **Game over!** 🏆")
                            cur.execute(f"""DROP TABLE `{ctx.user.id}`""")
                            cur.execute(f"""DROP TABLE `{opponentid}`""")
                            conn.commit()
                            upd1 = cur2.execute(f"""SELECT currentgames FROM main""").fetchone()
                            upd2 = sum(upd1)
                            upd = int(upd2)
                            upd -= 1
                            cur2.execute(f"""UPDATE main SET currentgames={upd}""")
                            conn2.commit()
                            conn2.close()
                            await interaction.response.defer()

                        cur.execute(f"""UPDATE `{ctx.user.id}` SET rps=0""")
                        cur.execute(f"""UPDATE `{opponentid}` SET rps=0""")
                        conn.close()
                        
                    else:
                        await interaction.response.send_message("Sorry, but it's not your turn or you're not playing! <:crosspong:1134110291311992962>", ephemeral=True)

            class PaperButton(discord.ui.Button):
                def __init__(self):
                    super().__init__(label="Paper", style=discord.ButtonStyle.primary, emoji="📜")
                    btns.append(self)
                    
                async def callback(self, interaction):
                    conn = sq.connect('datas.db')
                    cur = conn.cursor()

                    rps1 = cur.execute(f"""SELECT rps FROM `{ctx.user.id}`""").fetchone()
                    rps2 = sum(rps1)
                    rps = int(rps2)

                    if rpsbot == 6:
                        opporps1 = cur.execute(f"""SELECT rps FROM `{opponentid}`""").fetchone()
                        opporps2 = sum(opporps1)
                        opporps = int(opporps2)

                    else:
                        opporps1 = cur.execute(f"""SELECT rpsbot FROM `{ctx.user.id}`""").fetchone()
                        opporps2 = sum(opporps1)
                        opporps = int(opporps2)

                    if interaction.user.id == ctx.user.id and rps == 2:
                        if rpsbot == 6:
                            cur.execute(f"""UPDATE `{ctx.user.id}` SET rps=5""")
                            cur.execute(f"""UPDATE `{opponentid}` SET rps=2""")
                            conn.commit()
                            await interaction.message.edit(f"Okay! Now it's <@{opponentid}>'s turn to choose! 👉")
                            await interaction.response.defer()

                        else:
                            cur.execute(f"""UPDATE `{ctx.user.id}` SET rps=5""")

                            gennum = random.randint(1,3)

                            if gennum == 1:
                                await interaction.message.edit(f"Player: 📜\nBot: 🪨\n\nPlayer won! Bot missed the shot, so <@{ctx.user.id}> has won this match! **Game over!** 🏆")
                                cur.execute(f"""DROP TABLE `{ctx.user.id}`""")
                                conn.commit()
                                upd1 = cur2.execute(f"""SELECT botgames FROM main""").fetchone()
                                upd2 = sum(upd1)
                                upd = int(upd2)
                                upd -= 1
                                cur2.execute(f"""UPDATE main SET botgames={upd}""")
                                conn2.commit()
                                conn2.close()

                                await interaction.response.defer()

                            elif gennum == 2:
                                await interaction.message.edit(f"Player: 📜\nBot: ✂️\n\nBot won! Now it's bot's turn to ping a ball! 🏓")
                                cur.execute(f"""UPDATE `{ctx.user.id}` SET rps=0""")
                                cur.execute(f"""UPDATE `{ctx.user.id}` SET rpsbot=0""")
                                cur.execute(f"""UPDATE `{ctx.user.id}` SET turn=0""")

                                await ctx.respond(":robot:: Pong! 🏓")
                                cur.execute(f"""UPDATE `{ctx.user.id}` SET turn=1""")
                                conn.commit()
                                upd1 = cur2.execute(f"""SELECT ballspinged FROM main""").fetchone()
                                upd2 = sum(upd1)
                                upd = int(upd2)
                                upd += 1
                                cur2.execute(f"""UPDATE main SET ballspinged={upd}""")
                                conn2.commit()
                                conn2.close()

                                await interaction.response.defer()

                            else:
                                await interaction.message.edit(f"Player: 📜\nBot: 📜\n\nDraw! Now it's bot's turn to ping a ball! 🤜🤛")
                                cur.execute(f"""UPDATE `{ctx.user.id}` SET rps=0""")
                                cur.execute(f"""UPDATE `{ctx.user.id}` SET rpsbot=0""")
                                cur.execute(f"""UPDATE `{ctx.user.id}` SET turn=0""")

                                await ctx.respond(":robot:: Pong! 🏓")
                                cur.execute(f"""UPDATE `{ctx.user.id}` SET turn=1""")
                                upd1 = cur2.execute(f"""SELECT ballspinged FROM main""").fetchone()
                                upd2 = sum(upd1)
                                upd = int(upd2)
                                upd += 1
                                cur2.execute(f"""UPDATE main SET ballspinged={upd}""")
                                conn2.commit()
                                conn2.close()
                                conn.commit()

                                await interaction.response.defer()

                    elif interaction.user.id == opponentid and opporps == 2:
                        cur.execute(f"""UPDATE `{opponentid}` SET rps=5""")
                        conn.commit()

                        rps11 = cur.execute(f"""SELECT rps FROM `{ctx.user.id}`""").fetchone()
                        rps12 = sum(rps11)
                        rps1 = int(rps12)

                        rps21 = cur.execute(f"""SELECT rps FROM `{opponentid}`""").fetchone()
                        rps22 = sum(rps21)
                        rps2 = int(rps22)
                        
                        if rps1 == 5 and rps2 == 5:
                            await interaction.message.edit(f"Player 1: 📜\nPlayer 2: 📜\n\nDraw! Now it's <@{opponentid}>'s turn to ping a ball! 🤜🤛")
                            cur.execute(f"""UPDATE `{ctx.user.id}` SET turn=0""")
                            cur.execute(f"""UPDATE `{opponentid}` SET turn=1""")
                            cur.execute(f"""UPDATE `{ctx.user.id}` SET rps=0""")
                            cur.execute(f"""UPDATE `{opponentid}` SET rps=0""")
                            conn.commit()
                            upd1 = cur2.execute(f"""SELECT ballspinged FROM main""").fetchone()
                            upd2 = sum(upd1)
                            upd = int(upd2)
                            upd += 1
                            cur2.execute(f"""UPDATE main SET ballspinged={upd}""")
                            conn2.commit()
                            conn2.close()
                            await interaction.response.defer()

                        elif rps1 == 3 and rps2 == 5:
                            await interaction.message.edit(f"Player 1:📜\nPlayer 2: 🪨\n\nPlayer 2 won! <@{opponentid}> missed the shot, so <@{ctx.user.id}> won this match! **Game over!** 🏆")
                            upd1 = cur2.execute(f"""SELECT currentgames FROM main""").fetchone()
                            upd2 = sum(upd1)
                            upd = int(upd2)
                            upd -= 1
                            cur2.execute(f"""UPDATE main SET currentgames={upd}""")
                            cur.execute(f"""DROP TABLE `{ctx.user.id}`""")
                            cur.execute(f"""DROP TABLE `{opponentid}`""")
                            conn.commit()
                            conn2.commit()
                            conn2.close()
                            await interaction.response.defer()

                        elif rps1 == 4 and rps2 == 5:
                            await interaction.message.edit(f"Player 1:📜\nPlayer 2: ✂️\n\nPlayer 1 won! Now it's <@{opponentid}>'s turn to ping a ball! 🏓")
                            cur.execute(f"""UPDATE `{ctx.user.id}` SET turn=0""")
                            cur.execute(f"""UPDATE `{opponentid}` SET turn=1""")
                            cur.execute(f"""UPDATE `{ctx.user.id}` SET rps=0""")
                            cur.execute(f"""UPDATE `{opponentid}` SET rps=0""")
                            upd1 = cur2.execute(f"""SELECT ballspinged FROM main""").fetchone()
                            upd2 = sum(upd1)
                            upd = int(upd2)
                            upd += 1
                            cur2.execute(f"""UPDATE main SET ballspinged={upd}""")
                            conn2.commit()
                            conn2.close()
                            conn.commit()
                            await interaction.response.defer()

                        cur.execute(f"""UPDATE `{ctx.user.id}` SET rps=0""")
                        cur.execute(f"""UPDATE `{opponentid}` SET rps=0""")
                        conn.commit()
                        conn.close()
                        
                    else:
                        await interaction.response.send_message("Sorry, but it's not your turn or you're not playing! <:crosspong:1134110291311992962>", ephemeral=True)

        except:
            # I'll use this for printing exceptions
            pass

        rockbtn = RockButton()
        scissorsbtn = ScissorsButton()
        paperbtn = PaperButton()
        view=View()
        view.add_item(rockbtn)
        view.add_item(scissorsbtn)
        view.add_item(paperbtn)
        
        await ctx.respond(f"__**RPS TIME! 🪨📜✂️**__\n\nIf <@{ctx.user.id}> wins, the match ends and this user wins this match. Other situations ends with <@{opponentid}>'s turn.\n\n<@{ctx.user.id}>, choose *Rock*, *Scissors* or *Paper*!", view=view)
    
    try:
        isply = curso.execute(f"""SELECT isplaying FROM `{ctx.user.id}`""").fetchone()
        izply = sum(isply)
        isplaying2 = int(izply)
        
        opntid = curso.execute(f"""SELECT opponentid FROM `{ctx.user.id}`""").fetchone()
        obntid = sum(opntid)
        opponentid2 = int(obntid)

        isfirstping1 = curso.execute(f"""SELECT isfirstping FROM `{ctx.user.id}`""").fetchone()
        isfirstping2 = sum(isfirstping1)
        isfirstping = int(isfirstping2)

        torn = curso.execute(f"""SELECT turn FROM `{ctx.user.id}`""").fetchone()
        cern = sum(torn)
        turn2 = int(cern)

        rps1 = curso.execute(f"""SELECT rps FROM `{ctx.user.id}`""").fetchone()
        rps2 = sum(rps1)
        ctxrps = int(rps2)
        
        gameover = random.randint(1,15)
        rpsgen = random.randint(5,7)
        
        if opponentid2 != bot.user.id:
            if isplaying2 == 1 and opponentid2 != ctx.user.id and turn2 == 0 and ctxrps == 0:
                await ctx.respond("Sorry, but it's not your turn. <:crosspong:1134110291311992962>", ephemeral=True)
                consoleclear()

            elif ctxrps != 0:
                await ctx.respond("Sorry, but you're playing RPS right now. <:crosspong:1134110291311992962>", ephemeral=True)
            
            elif isfirstping == 0 and ctxrps == 0:
                curso.execute(f"""UPDATE `{ctx.user.id}` SET isfirstping=1""")
                curso.execute(f"""UPDATE `{ctx.user.id}` SET turn=0""")
                curso.execute(f"""UPDATE `{opponentid2}` SET turn=1""")
                upd1 = curs2.execute(f"""SELECT ballspinged FROM main""").fetchone()
                upd2 = sum(upd1)
                upd = int(upd2)
                upd += 1
                curs2.execute(f"""UPDATE main SET ballspinged={upd}""")
                await ctx.respond(f"Pong! 🏓")
                conne.commit()
                conne.close()
                connn2.commit()
                connn2.close()
                
            elif isplaying2 == 1 and opponentid2 != ctx.user.id and turn2 == 1 and gameover != 6 and rpsgen == 6 and isfirstping == 1 and ctxrps == 0:
                await rps()
                
            elif isplaying2 == 1 and opponentid2 != ctx.user.id and turn2 == 1 and gameover == 6 and ctxrps == 0:
                await ctx.respond(f"OOF! You've missed the shot and your opponent is the winner! Congratulations, <@{opponentid2}>! **Game over!** 🏆")
                curso.execute(f"""DROP TABLE `{ctx.user.id}`""")
                curso.execute(f"""DROP TABLE `{opponentid2}`""")
                upd1 = curs2.execute(f"""SELECT currentgames FROM main""").fetchone()
                upd2 = sum(upd1)
                upd = int(upd2)
                upd -= 1
                curs2.execute(f"""UPDATE main SET currentgames={upd}""")
                conne.commit()
                connn2.commit()
                connn2.close()
                consoleclear()
                
            elif isplaying2 == 1 and opponentid2 != ctx.user.id and turn2 == 1 and gameover != 6 and rpsgen != 6 and ctxrps == 0:
                if rpsgen != 6:
                    curso.execute(f"""UPDATE `{ctx.user.id}` SET turn=0""")
                    curso.execute(f"""UPDATE `{opponentid2}` SET turn=1""")
                    upd1 = curs2.execute(f"""SELECT ballspinged FROM main""").fetchone()
                    upd2 = sum(upd1)
                    upd = int(upd2)
                    upd += 1
                    curs2.execute(f"""UPDATE main SET ballspinged={upd}""")
                    conne.commit()
                    connn2.commit()
                    connn2.close()
                    await ctx.respond(f"Pong! 🏓")
                    consoleclear()
                else:
                    await rps()

        else:
            if isplaying2 == 1:
                gameover2 = random.randint(1,15)
                rpsgen = random.randint(5,7)

                ctxrps1 = curso.execute(f"""SELECT rps FROM `{ctx.user.id}`""").fetchone()
                ctxrps2 = sum(ctxrps1)
                ctxrps = int(ctxrps2)
                
                isfirstping1 = curso.execute(f"""SELECT isfirstping FROM `{ctx.user.id}`""").fetchone()
                isfirstping2 = sum(isfirstping1)
                isfirstping = int(isfirstping2)
                
                if isfirstping == 0 and ctxrps == 0:
                    curso.execute(f"""UPDATE `{ctx.user.id}` SET isfirstping=1""")
                    await ctx.respond(":person_raising_hand:: Pong! 🏓")
                    await ctx.respond(":robot:: Pong! 🏓")
                    upd1 = curs2.execute(f"""SELECT ballspinged FROM main""").fetchone()
                    upd2 = sum(upd1)
                    upd = int(upd2)
                    upd += 2
                    curs2.execute(f"""UPDATE main SET ballspinged={upd}""")
                    connn2.commit()
                    connn2.close()
                    conne.commit()
                    conne.close()

                elif ctxrps != 0:
                    await ctx.respond("Sorry, but you're playing RPS right now. <:crosspong:1134110291311992962>", ephemeral=True)
                    conne.close()
                    connn2.close()

                elif gameover2 != 6 and rpsgen != 6:
                    await ctx.respond(":person_raising_hand:: Pong! 🏓")
                    await ctx.respond(":robot:: Pong! 🏓")
                    upd1 = curs2.execute(f"""SELECT ballspinged FROM main""").fetchone()
                    upd2 = sum(upd1)
                    upd = int(upd2)
                    upd += 2
                    curs2.execute(f"""UPDATE main SET ballspinged={upd}""")
                    connn2.commit()
                    connn2.close()
                    conne.close()
                    consoleclear()

                elif gameover2 != 6 and rpsgen == 6:
                    await rps()
                    conne.close()
                    connn2.close()
                    
                elif gameover2 == 6 and rpsgen == 6:
                    gennum = random.randint(1,2)

                    if gennum == 1:
                        await ctx.respond(":person_raising_hand:: OOF! You've missed the shot, so :robot: won! Better luck next time! **Game over!** 🏆")
                        curso.execute(f"""DROP TABLE `{ctx.user.id}`""")
                        upd1 = curs2.execute(f"""SELECT botgames FROM main""").fetchone()
                        upd2 = sum(upd1)
                        upd = int(upd2)
                        upd -= 1
                        curs2.execute(f"""UPDATE main SET botgames={upd}""")
                        connn2.commit()
                        connn2.close()
                        conne.commit()
                        conne.close()
                        consoleclear()

                    else:
                        await ctx.respond(":person_raising_hand:: Pong! 🏓")
                        await ctx.respond(f":robot:: OOF! I've missed the shot and you won! Congratultions, <@{ctx.user.id}>! **Game over!** 🏆")
                        curso.execute(f"""DROP TABLE `{ctx.user.id}`""")
                        upd1 = curs2.execute(f"""SELECT botgames FROM main""").fetchone()
                        upd2 = sum(upd1)
                        upd = int(upd2)
                        upd -= 1
                        curs2.execute(f"""UPDATE main SET botgames={upd}""")
                        upd1 = curs2.execute(f"""SELECT ballspinged FROM main""").fetchone()
                        upd2 = sum(upd1)
                        upd = int(upd2)
                        upd += 1
                        curs2.execute(f"""UPDATE main SET ballspinged={upd}""")
                        connn2.commit()
                        connn2.close()
                        conne.commit()
                        conne.close()
                        consoleclear()
                    
            else:
                await ctx.respond(":person_raising_hand:: OOF! You've missed the shot, so :robot: won! Better luck next time! **Game over!** 🏆")
                curso.execute(f"""DROP TABLE `{ctx.user.id}`""")
                upd1 = curs2.execute(f"""SELECT botgames FROM main""").fetchone()
                upd2 = sum(upd1)
                upd = int(upd2)
                upd -= 1
                curs2.execute(f"""UPDATE main SET botgames={upd}""")
                connn2.commit()
                connn2.close()
                conne.commit()
                conne.close()
                consoleclear()
        
    except Exception as e:
        await ctx.respond("Sorry, but you are not playing with anyone. <:crosspong:1134110291311992962>")
        consoleclear()
   
# Singleplayer command
   
@bot.slash_command(description="Play alone with bot!")
async def singleplayer(ctx):
    con = sq.connect('datas.db')
    cur = con.cursor()
    conn2 = sq.connect("stats.db")
    curs2 = conn2.cursor()
    
    try:
        cur.execute(f"""SELECT isplaying FROM `{ctx.user.id}`""").fetchall()
        await ctx.respond("Sorry, but you are actually playing with someone. <:crosspong:1134110291311992962>")
        con.close()
        conn2.close()
        
    except:
        consoleclear()
        cur.execute(f"""CREATE TABLE `{ctx.user.id}` (isplaying int, opponentid int, turn int, rps int, rpsbot int, isfirstping int)""")
        cur.execute(f"""INSERT INTO `{ctx.user.id}` VALUES (1, {bot.user.id}, 1, 0, 0, 0)""")
        con.commit()
        con.close()
        upd1 = curs2.execute("""SELECT totalgames FROM main""").fetchone()
        upd2 = sum(upd1)
        upd = int(upd2)
        upd += 1
        curs2.execute(f"""UPDATE main SET totalgames={upd}""")
        conn2.commit()
        upd1 = curs2.execute("""SELECT botgames FROM main""").fetchone()
        upd2 = sum(upd1)
        upd = int(upd2)
        upd += 1
        curs2.execute(f"""UPDATE main SET botgames={upd}""")
        conn2.commit()
        conn2.close()
        consoleclear()
        
        await ctx.respond("So, you want to play with me? Alright! You start first. Type </ping:999267081629487196> to start playing! <:tickpong:1134110509872984095>")
        
# Help command        

@bot.slash_command(description="Get started playing with DisPong!")
async def help(ctx):
    await ctx.respond("Hey! I'm **DisPong**! I was created by Gl1tch3dL1m3...he coded me in Python with Pycord library! Anyways, I hope you will have fun with me! Come on! Invite someone to play by typing </duel:1085970985552978033>!\n\nHow to play? Just type </ping:999267081629487196>...command author starts first..then command author's opponent and so on! My commands are:\n</help:999334780732719244> - This message\n</ping:999267081629487196> - Play Ping Pong!\n</duel:1085970985552978033> - Start new game with antoher player! (this was **/newgame** before, but there will be (maybe :D) 4 players match and this is going to be **/newgame** command!)\n</finish:999267081629487195> - Delete your request or finish a game!\n</singleplayer:1085970985552978034> - Play with DisPong!\n</changelog:1085970985552978035> - DisPong updates log!\n</stats:1134139510070980648> - Games statistics!\n\n*You may encounter bugs with __v1.2__ update. If this happens, please report it to the support server (preferably with a screenshot). Thanks!*\n\nOk, that's all! If you need some help, want to report a bug, suggest something, or just want to play with others, join our support server: https://discord.gg/dduRC6cdy3")
    
# Changelog command

@bot.slash_command(description="DisPong updates log.")
async def changelog(ctx):
    await ctx.respond("__v1.1__: Added Singleplayer and better looking responses.\n__v1.2__: Added RPS minigame, games statistics and custom emojis (more emojis are going to be added soon). Fixed some bugs in </duel:1085970985552978033> command.\n\n*More comming soon!*")
    
# Statistics command

@bot.slash_command(description="Statistics!")
async def stats(ctx):
    # Global statistics

    conn = sq.connect("stats.db")
    cur = conn.cursor()
    
    totalgames1 = cur.execute(f"""SELECT totalgames FROM main""").fetchone()
    totalgames2 = sum(totalgames1)
    totalgames = int(totalgames2)
    
    currentgames1 = cur.execute(f"""SELECT currentgames FROM main""").fetchone()
    currentgames2 = sum(currentgames1)
    currentgames = int(currentgames2)
    
    ballspinged1 = cur.execute(f"""SELECT ballspinged FROM main""").fetchone()
    ballspinged2 = sum(ballspinged1)
    ballspinged = int(ballspinged2)

    botgames1 = cur.execute(f"""SELECT botgames FROM main""").fetchone()
    botgames2 = sum(botgames1)
    botgames = int(botgames2)

    await ctx.respond(f"__Statistics:__\nTotal games played: {totalgames}\nCurrent games playing: {currentgames}\nCurrent singleplayer games: {botgames}\nTotal balls pinged: {ballspinged}")

    conn.close()
    consoleclear()
    
bot.run(token)
