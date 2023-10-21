###### DisPong by @glitchedlime ######

# Last changes: 21. October 2023
# Commands count: 6

# This script version doesn't contain minigames.

# IMPORTANT: A new database must be used while running the minigames bot version script. This system is used here as well. It's "stats.db". You must run "createstatsold.py" to create this database and move it where the main script is (this script). I also used a showcase gif in /help. Feel free to delete it.
# LINUX NOTE: If you are running on Linux, replace 'cls' with 'clear' in consoleclear function!

# Feel free to use this script, but don't steal it (selling, pretending to be creator of this script, etc.)!



# EMOJIS

import discord
from discord import Option
import sqlite3 as sq
from config import token
import random
import os

bot = discord.Bot(help_command = None)

# Show message in console when ready + status showing bot's version

@bot.event
async def on_ready():
    print(f"{bot.user} is ready!")
    await bot.change_presence(activity=discord.Game(name="classic version."))
    
# Console clear (Linux: replace 'cls' with 'clear')

def consoleclear():
    os.system('cls')
    
# Duel command

@bot.slash_command(description = "Send a request to someone.")
async def duel(ctx, opponent: Option(discord.Member, "Select your opponent.", required=True)):
    con = sq.connect('datas.db')
    cur = con.cursor()
    
    if opponent.id == ctx.user.id:
        await ctx.respond("Sorry, but you can't play with yourself. <:crosspong:1134110291311992962>", ephemeral=True)
        con.close()
    else:
        if opponent.bot:
            await ctx.respond("Sorry, but you can't play with a bot. <:crosspong:1134110291311992962>", ephemeral=True)
            con.close()
        else:
            try:
                cur.execute(f"""SELECT isplaying FROM `{ctx.user.id}`""").fetchall()
                await ctx.respond("Sorry, but you are actually playing with someone or have a pending request. <:crosspong:1134110291311992962>", ephemeral=True)
                consoleclear()
                con.close()
            except:
                try:
                    cur.execute(f"""SELECT isplaying FROM `{opponent.id}`""").fetchall()
                    await ctx.respond("Sorry, but mentioned user is actually playing with someone or has a pending request. <:crosspong:1134110291311992962>", ephemeral=True)
                    con.close()
                    consoleclear()
                except:
                    class duelView(discord.ui.View):
                        @discord.ui.button(
                            label="Yes!",
                            style=discord.ButtonStyle.success,
                            emoji="<:tickpong:1134110509872984095>"
                        )

                        async def yes_button_callback(self, button, interaction):
                            con = sq.connect('datas.db')
                            cur = con.cursor()

                            conn2 = sq.connect('stats.db')
                            curs2 = conn2.cursor()

                            try:
                                lastreqid1 = cur.execute(f"""SELECT lastreqid FROM `{ctx.user.id}`""").fetchone()
                                lastreqid2 = sum(lastreqid1)
                                lastreqid = int(lastreqid2)

                                player_21 = cur.execute(f"""SELECT requestedopponent FROM `{ctx.user.id}`""").fetchone()
                                player_22 = sum(player_21)
                                player_2 = int(player_22)

                                if lastreqid != self.message.id:
                                    await interaction.response.send_message("Sorry, but this request is no longer valid. <:crosspong:1134110291311992962>", ephemeral=True)
                                    con.close()
                                    conn2.close()

                                elif interaction.user.id == player_2:
                                    try:
                                        cur.execute(f"""SELECT isplaying FROM `{interaction.user.id}`""").fetchall()
                                        await interaction.response.send_message("Sorry, but you are actually playing with someone or have a pending request. <:crosspong:1134110291311992962>", ephemeral=True)
                                        con.close()
                                        conn2.close()

                                    except:
                                        cur.execute(f"""UPDATE `{ctx.user.id}` SET isplaying=1""")
                                        cur.execute(f"""UPDATE `{ctx.user.id}` SET turn=1""")
                                        cur.execute(f"""UPDATE `{ctx.user.id}` SET opponentid={player_2}""")
                                        cur.execute(f"""UPDATE `{ctx.user.id}` SET requestedopponent=0""")
                                        cur.execute(f"""CREATE TABLE `{player_2}` (isplaying int, opponentid int, turn int, isfirstping int, lastminigameid int)""")                  
                                        cur.execute(f"""INSERT INTO `{player_2}` VALUES (1, {ctx.user.id}, 0, 0, 0)""")
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
                                        self.disable_all_items()
                                        await interaction.message.edit(f'<@{player_2}>\n\nDo you want to play with <@{ctx.user.id}>? If <@{ctx.user.id}> would like to delete request, use </finish:1165193929222787147> or press "Delete request!" button! <:circlepong:1134110288438894654>\n\n**Request accepted! <:tickpong:1134110509872984095>**', view=self)
                                        await interaction.response.send_message(f"Okay! <@{ctx.user.id}> starts! Type </ping:1165193929222787148> to play! Enjoy your playing! <:tickpong:1134110509872984095>")
                                        con.commit()
                                        con.close()
                                        conn2.commit()
                                        conn2.close()

                                elif interaction.user.id == ctx.user.id:
                                    await interaction.response.send_message("Sorry, but only your opponent can accept this request. <:crosspong:1134110291311992962>", ephemeral=True)
                                    con.close()
                                    conn2.close()
                                    consoleclear()

                                else:
                                    await interaction.response.send_message("Sorry, but you are not the asked player. <:crosspong:1134110291311992962>", ephemeral=True)
                                    con.close()
                                    conn2.close()
                                    consoleclear()

                            except:
                                await interaction.response.send_message("Sorry, but this request is no longer valid. <:crosspong:1134110291311992962>", ephemeral=True)
                                con.close()
                                conn2.close()

                        @discord.ui.button(
                            label="No!",
                            style=discord.ButtonStyle.danger,
                            emoji="<:crosspong:1134110291311992962>"
                        )

                        async def no_button_callback(self, button, interaction):
                            con = sq.connect('datas.db')
                            cur = con.cursor()

                            try:
                                lastreqid1 = cur.execute(f"""SELECT lastreqid FROM `{ctx.user.id}`""").fetchone()
                                lastreqid2 = sum(lastreqid1)
                                lastreqid = int(lastreqid2)

                                player_21 = cur.execute(f"""SELECT requestedopponent FROM `{ctx.user.id}`""").fetchone()
                                player_22 = sum(player_21)
                                player_2 = int(player_22)

                                if lastreqid != self.message.id:
                                    await interaction.response.send_message("Sorry, but this request is no longer valid. <:crosspong:1134110291311992962>", ephemeral=True)
                                    con.close()

                                elif interaction.user.id == player_2:
                                    cur.execute(f"""DROP TABLE `{ctx.user.id}`""")
                                    self.disable_all_items()
                                    await interaction.message.edit(f'<@{player_2}>\n\nDo you want to play with <@{ctx.user.id}>? If <@{ctx.user.id}> would like to delete request, use </finish:1165193929222787147> or press "Delete request!" button! <:circlepong:1134110288438894654>\n\n**Request denied! <:tickpong:1134110509872984095>**', view=self)
                                    await interaction.response.send_message("Alright, so we are not playing this time! <:crosspong:1134110291311992962>")
                                    con.commit()
                                    con.close()

                                elif interaction.user.id == ctx.user.id:
                                    await interaction.response.send_message("Sorry, but only your opponent can deny this request. <:crosspong:1134110291311992962>", ephemeral=True)
                                    con.close()
                                        
                                else:
                                    await interaction.response.send_message("Sorry, but you are not the asked player. <:crosspong:1134110291311992962>", ephemeral=True)
                                    con.close()
                                    consoleclear()

                            except:
                                await interaction.response.send_message("Sorry, but this request is no longer valid. <:crosspong:1134110291311992962>", ephemeral=True)
                                con.close()

                        @discord.ui.button(
                            label="Delete request!",
                            style=discord.ButtonStyle.blurple,
                            emoji="<:brokenpong:1134116285014360206>"
                        )

                        async def delete_request_button_callback(self, button, interaction):
                            con = sq.connect('datas.db')
                            cur = con.cursor()

                            try:
                                lastreqid1 = cur.execute(f"""SELECT lastreqid FROM `{ctx.user.id}`""").fetchone()
                                lastreqid2 = sum(lastreqid1)
                                lastreqid = int(lastreqid2)

                                if lastreqid != self.message.id:
                                    await interaction.response.send_message("Sorry, but this request is no longer valid. <:crosspong:1134110291311992962>", ephemeral=True)
                                    con.close()

                                elif interaction.user.id == ctx.user.id:
                                    cur.execute(f"""DROP TABLE `{ctx.user.id}`""")
                                    self.disable_all_items()
                                    await interaction.message.edit(f'<@{opponent.id}>\n\nDo you want to play with <@{ctx.user.id}>? If <@{ctx.user.id}> would like to delete request, use </finish:1165193929222787147> or press "Delete request!" button! <:circlepong:1134110288438894654>\n\n**Request deleted! <:tickpong:1134110509872984095>**', view=self)
                                    con.commit()
                                    con.close()
                                    await interaction.response.defer()
                                        
                                else:
                                    await interaction.response.send_message("Sorry, but only command author can delete this request. <:crosspong:1134110291311992962>", ephemeral=True)
                                    consoleclear()
                                    con.close()

                            except:
                                await interaction.response.send_message("Sorry, but this request is no longer valid. <:crosspong:1134110291311992962>", ephemeral=True)
                                con.close()
                    
                    inter = await ctx.respond(f'<@{opponent.id}>\n\nDo you want to play with <@{ctx.user.id}>? If <@{ctx.user.id}> would like to delete request, use </finish:1165193929222787147> or press "Delete request!" button! <:circlepong:1134110288438894654>', view=duelView())
                    cur.execute(f'''CREATE TABLE `{ctx.user.id}` (isplaying int, requestedopponent int, opponentid int, turn int, isfirstping int, lastreqid int)''')
                    originalmsg = await inter.original_response()
                    cur.execute(f'''INSERT INTO `{ctx.user.id}` VALUES (0, {opponent.id}, 0, 0, 0,{originalmsg.id})''')
                    con.commit()
                    con.close()

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

        if opsids == bot.user.id:
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
            await ctx.respond("Game finished! <:tickpong:1134110509872984095>")

        elif opsids != 0:
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

        else:
            curs.execute(f"""DROP TABLE `{ctx.user.id}`""")
            await ctx.respond("Request deleted! <:tickpong:1134110509872984095>")
            conn.commit()
            conn.close()
        
    except:
        await ctx.respond("Sorry, but you are not playing with anyone. <:crosspong:1134110291311992962>", ephemeral=True)
        conn.close()
        conn2.close()

# Ping command
    
@bot.slash_command(description="Pong!")
async def ping(ctx):
    conne = sq.connect('datas.db')
    curso = conne.cursor()

    connn2 = sq.connect('stats.db')
    curs2 = connn2.cursor()
    
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

        gameover = random.randint(6,20)

        if isplaying2 == 1:
            if opponentid2 != bot.user.id:
                if opponentid2 != ctx.user.id and turn2 == 0:
                    await ctx.respond("Sorry, but it's not your turn. <:crosspong:1134110291311992962>", ephemeral=True)
                    conne.close()
                    connn2.close()
                    consoleclear()
                
                elif isfirstping == 0:
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

                elif isplaying2 == 1 and opponentid2 != ctx.user.id and turn2 == 1 and gameover == 6:
                    await ctx.respond(f"OOF! You've missed the shot and your opponent is the winner! Congratulations, <@{opponentid2}>! **Game over!** 🏆")
                    curso.execute(f"""DROP TABLE `{ctx.user.id}`""")
                    curso.execute(f"""DROP TABLE `{opponentid2}`""")
                    upd1 = curs2.execute(f"""SELECT currentgames FROM main""").fetchone()
                    upd2 = sum(upd1)
                    upd = int(upd2)
                    upd -= 1
                    curs2.execute(f"""UPDATE main SET currentgames={upd}""")
                    conne.commit()
                    conne.close()
                    connn2.commit()
                    connn2.close()
                    consoleclear()
                    
                elif isplaying2 == 1 and opponentid2 != ctx.user.id and turn2 == 1:
                    curso.execute(f"""UPDATE `{ctx.user.id}` SET turn=0""")
                    curso.execute(f"""UPDATE `{opponentid2}` SET turn=1""")
                    upd1 = curs2.execute(f"""SELECT ballspinged FROM main""").fetchone()
                    upd2 = sum(upd1)
                    upd = int(upd2)
                    upd += 1
                    curs2.execute(f"""UPDATE main SET ballspinged={upd}""")
                    conne.commit()
                    conne.close()
                    connn2.commit()
                    connn2.close()
                    await ctx.respond(f"Pong! 🏓")
                    consoleclear()

            else:
                if isfirstping == 0:
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

                elif gameover != 6:
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
                    
                else:
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
            await ctx.respond("Sorry, but you are not playing with anyone. <:crosspong:1134110291311992962>", ephemeral=True)
            conne.close()
            connn2.close()
        
    except Exception as e:
        print(e)
        await ctx.respond("Sorry, but you are not playing with anyone. <:crosspong:1134110291311992962>", ephemeral=True)
        consoleclear()
   
# Singleplayer command
   
@bot.slash_command(description="Play alone with the bot.")
async def singleplayer(ctx):
    con = sq.connect('datas.db')
    cur = con.cursor()
    conn2 = sq.connect("stats.db")
    curs2 = conn2.cursor()
    
    try:
        cur.execute(f"""SELECT isplaying FROM `{ctx.user.id}`""").fetchall()
        await ctx.respond("Sorry, but you are actually playing with someone or have a pending request. <:crosspong:1134110291311992962>", ephemeral=True)
        con.close()
        conn2.close()
        
    except:
        consoleclear()
        cur.execute(f"""CREATE TABLE `{ctx.user.id}` (isplaying int, opponentid int, turn int, isfirstping int)""")
        cur.execute(f"""INSERT INTO `{ctx.user.id}` VALUES (1, {bot.user.id}, 1, 0)""")
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
        
        await ctx.respond("So, you want to play with me? Alright! You start first. Type </ping:1165193929222787148> to start playing! <:tickpong:1134110509872984095>")
        
# Help command

@bot.slash_command(description="Get started playing with DisPong.")
async def help(ctx):
    showcase = discord.File("showcase.gif")
    await ctx.respond("Hello! Thank you for using my bot! I coded this bot in Python with Pycord library. Since this is an open-source bot, the script is available on GitHub. Also, this bot version does not include minigames. Join the support server below if you are interested in GitHub or the minigames version bot.\n\nIf you are using DisPong for the first time, I recommend you watching the gif below.\n\nCurrent commands:\n</help:1165193929222787150> - This message.\n</ping:1165193929222787148> - Play Ping Pong.\n</duel:1165193929222787146> - Start new game with antoher player.\n</finish:1165193929222787147> - Delete your request or finish a game.\n</singleplayer:1165193929222787149> - Play with the bot.\n</stats:1165193929222787151> - Games statistics.\n\nThat's all! I really hope you'll like my bot! If you need some help, want to report a bug, suggest something, or just want to play with others, join our support server: https://discord.gg/dduRC6cdy3", file=showcase)
       
# Statistics command

@bot.slash_command(description="DisPong statistics.")
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
