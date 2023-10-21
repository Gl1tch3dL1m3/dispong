###### DisPong by @glitchedlime ######

# Last changes: 21. October 2023
# Commands count: 7
# Bot's version: v1.3

# IMPORTANT: A new database must be used while running this script since update v1.2. It's "stats.db". You must run "createstats.py" to create this database and move it where the main script is (this script). I also used a showcase gif in /help. Feel free to delete it.
# LINUX NOTE: If you are running on Linux, replace 'cls' with 'clear' in consoleclear function!

# Feel free to use this script, but don't steal it (selling, pretending to be creator of this script, etc.)!

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
    await bot.change_presence(activity=discord.Game(name="v1.3"))
    
# Console clear (Linux: replace 'cls' with 'clear')

def consoleclear():
    os.system('cls')
    
# Duel command (v1.0)

@bot.slash_command(description = "Send a request to someone.")
async def duel(ctx, opponent: Option(discord.Member, "Select your opponent.", required=True)):
    con = sq.connect('datas.db')
    cur = con.cursor()

    # I used player_2 variable before opponent variable and I didn't want to change it
    player_2 = opponent
    
    if player_2.id == ctx.user.id:
        await ctx.respond("Sorry, but you can't play with yourself. <:crosspong:1134110291311992962>", ephemeral=True)
        con.close()
    else:
        if player_2.bot:
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
                    cur.execute(f"""SELECT isplaying FROM `{player_2.id}`""").fetchall()
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
                                        cur.execute(f"""CREATE TABLE `{player_2}` (isplaying int, opponentid int, turn int, rps int, rpsbot int, isfirstping int, tttturn int, tttgame int, tttbot int, lastminigameid int)""")                  
                                        cur.execute(f"""INSERT INTO `{player_2}` VALUES (1, {ctx.user.id}, 0, 0, 6, 0, 0, 111111111, 3, 0)""")
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
                                        await interaction.message.edit(f'<@{player_2}>\n\nDo you want to play with <@{ctx.user.id}>? If <@{ctx.user.id}> would like to delete request, use </finish:999267081629487195> or press "Delete request!" button! <:circlepong:1134110288438894654>\n\n**Request accepted! <:tickpong:1134110509872984095>**', view=self)
                                        await interaction.response.send_message(f"Okay! <@{ctx.user.id}> starts! Type </ping:999267081629487196> to play! Enjoy your playing! <:tickpong:1134110509872984095>")
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
                                    await interaction.message.edit(f'<@{player_2}>\n\nDo you want to play with <@{ctx.user.id}>? If <@{ctx.user.id}> would like to delete request, use </finish:999267081629487195> or press "Delete request!" button! <:circlepong:1134110288438894654>\n\n**Request denied! <:tickpong:1134110509872984095>**', view=self)
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
                                    await interaction.message.edit(f'<@{player_2.id}>\n\nDo you want to play with <@{ctx.user.id}>? If <@{ctx.user.id}> would like to delete request, use </finish:999267081629487195> or press "Delete request!" button! <:circlepong:1134110288438894654>\n\n**Request deleted! <:tickpong:1134110509872984095>**', view=self)
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
                    
                    inter = await ctx.respond(f'<@{player_2.id}>\n\nDo you want to play with <@{ctx.user.id}>? If <@{ctx.user.id}> would like to delete request, use </finish:999267081629487195> or press "Delete request!" button! <:circlepong:1134110288438894654>', view=duelView())
                    cur.execute(f'''CREATE TABLE `{ctx.user.id}` (isplaying int, requestedopponent int, opponentid int, turn int, rps int, rpsbot int, isfirstping int, tttturn int, tttgame int, tttbot int, lastminigameid int, lastreqid int)''')
                    originalmsg = await inter.original_response()
                    cur.execute(f'''INSERT INTO `{ctx.user.id}` VALUES (0, {player_2.id}, 0, 0, 0, 6, 0, 0, 111111111, 3, 0, {originalmsg.id})''')
                    con.commit()
                    con.close()

# Finish command (v1.0)
                    
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

# Ping command (v1.0)
    
@bot.slash_command(description="Pong!")
async def ping(ctx):
    conne = sq.connect('datas.db')
    curso = conne.cursor()

    connn2 = sq.connect('stats.db')
    curs2 = connn2.cursor()

    # RPS minigame (v1.2)

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

        try:
            if rpsbot == 6:
                cur.execute(f"""UPDATE `{opponentid}` SET rps=1""")
                cur.execute(f"""UPDATE `{ctx.user.id}` SET rps=2""")
                conn.commit()

            else:
                cur.execute(f"""UPDATE `{ctx.user.id}` SET rps=2""")
                cur.execute(f"""UPDATE `{ctx.user.id}` SET rpsbot=1""")
                conn.commit()

            class rpsView(discord.ui.View):
                @discord.ui.button(
                    label="Rock",
                    style=discord.ButtonStyle.primary,
                    emoji="🪨"
                )

                async def rock_button_callback(self, button, interaction):
                    conn = sq.connect('datas.db')
                    cur = conn.cursor()

                    conn2 = sq.connect('stats.db')
                    cur2 = conn2.cursor()

                    try:
                        minigameid1 = cur.execute(f"""SELECT lastminigameid FROM `{interaction.user.id}`""").fetchone()
                        minigameid2 = sum(minigameid1)
                        minigameid = int(minigameid2)

                        if minigameid == self.message.id:
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
                                        self.disable_all_items()
                                        await interaction.message.edit(f"Player: 🪨\nBot: 🪨\n\nDraw! Now it's bot's turn to ping a ball! 🤜🤛", view=self)
                                        cur.execute(f"""UPDATE `{ctx.user.id}` SET rps=0""")
                                        cur.execute(f"""UPDATE `{ctx.user.id}` SET rpsbot=0""")
                                        cur.execute(f"""UPDATE `{ctx.user.id}` SET turn=0""")
                                        await ctx.respond(":robot:: Pong! 🏓")
                                        cur.execute(f"""UPDATE `{ctx.user.id}` SET turn=1""")
                                        conn.commit()
                                        conn.close()
                                        upd1 = cur2.execute(f"""SELECT ballspinged FROM main""").fetchone()
                                        upd2 = sum(upd1)
                                        upd = int(upd2)
                                        upd += 1
                                        cur2.execute(f"""UPDATE main SET ballspinged={upd}""")
                                        conn2.commit()
                                        conn2.close()
                                        await interaction.response.defer()

                                    elif gennum == 2:
                                        self.disable_all_items()
                                        await interaction.message.edit(f"Player: 🪨\nBot: ✂️\n\nPlayer won! Bot missed the shot, so <@{ctx.user.id}> has won this match! **Game over!** 🏆", view=self)
                                        cur.execute(f"""DROP TABLE `{ctx.user.id}`""")
                                        conn.commit()
                                        conn.close()
                                        upd1 = cur2.execute(f"""SELECT botgames FROM main""").fetchone()
                                        upd2 = sum(upd1)
                                        upd = int(upd2)
                                        upd -= 1
                                        cur2.execute(f"""UPDATE main SET botgames={upd}""")
                                        conn2.commit()
                                        conn2.close()
                                        await interaction.response.defer()

                                    else:
                                        self.disable_all_items()
                                        await interaction.message.edit(f"Player: 🪨\nBot: 📜\n\nBot won! Now it's bot's turn to ping a ball! 🏓", view=self)
                                        cur.execute(f"""UPDATE `{ctx.user.id}` SET rps=0""")
                                        cur.execute(f"""UPDATE `{ctx.user.id}` SET rpsbot=0""")
                                        cur.execute(f"""UPDATE `{ctx.user.id}` SET turn=0""")
                                        await ctx.respond(":robot:: Pong! 🏓")
                                        cur.execute(f"""UPDATE `{ctx.user.id}` SET turn=1""")
                                        conn.commit()
                                        conn.close()
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

                                rps21 = cur.execute(f"""SELECT rps FROM `{opponentid}`""").fetchone()
                                rps22 = sum(rps21)
                                rps2 = int(rps22)

                                if rps2 == 3 and rps1 == 3:
                                    self.disable_all_items()
                                    await interaction.message.edit(f"Player 1: 🪨\nPlayer 2: 🪨\n\nDraw! Now it's <@{opponentid}>'s turn to ping a ball! 🤜🤛", view=self)
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

                                elif rps2 == 3 and rps1 == 4:
                                    self.disable_all_items()
                                    await interaction.message.edit(f"Player 1: ✂️\nPlayer 2: 🪨\n\nPlayer 2 won! Now it's <@{opponentid}>'s turn to ping a ball! 🏓", view=self)
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

                                elif rps2 == 3 and rps1 == 5:
                                    self.disable_all_items()
                                    await interaction.message.edit(f"Player 1: 📜\nPlayer 2: 🪨\n\nPlayer 1 won! <@{opponentid}> missed the shot, so <@{ctx.user.id}> won this match! **Game over!** 🏆", view=self)
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

                                conn.close()

                            else:
                                await interaction.response.send_message("Sorry, but it's not your turn. <:crosspong:1134110291311992962>", ephemeral=True)
                        else:
                            await interaction.response.send_message("Sorry, but this action is not valid. Please check if you are playing this game or your opponent didn't leave the match. <:crosspong:1134110291311992962>", ephemeral=True)
                    except:
                        await interaction.response.send_message("Sorry, but this action is not valid. Please check if you are playing this game or your opponent didn't leave the match. <:crosspong:1134110291311992962>", ephemeral=True)

                @discord.ui.button(
                    label="Scissors",
                    style=discord.ButtonStyle.primary,
                    emoji="✂️"
                )

                async def scissors_button_callback(self, button, interaction):
                    conn = sq.connect('datas.db')
                    cur = conn.cursor()

                    conn2 = sq.connect('stats.db')
                    cur2 = conn2.cursor()

                    try:
                        minigameid1 = cur.execute(f"""SELECT lastminigameid FROM `{interaction.user.id}`""").fetchone()
                        minigameid2 = sum(minigameid1)
                        minigameid = int(minigameid2)

                        if minigameid == self.message.id:
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
                                        self.disable_all_items()
                                        await interaction.message.edit(f"Player: ✂️\nBot: 🪨\n\nBot won! Now it's bot's turn to ping a ball! 🏓", view=self)
                                        cur.execute(f"""UPDATE `{ctx.user.id}` SET rps=0""")
                                        cur.execute(f"""UPDATE `{ctx.user.id}` SET rpsbot=0""")
                                        cur.execute(f"""UPDATE `{ctx.user.id}` SET turn=0""")
                                        await ctx.respond(":robot:: Pong! 🏓")
                                        cur.execute(f"""UPDATE `{ctx.user.id}` SET turn=1""")
                                        conn.commit()
                                        conn.close()
                                        upd1 = cur2.execute(f"""SELECT ballspinged FROM main""").fetchone()
                                        upd2 = sum(upd1)
                                        upd = int(upd2)
                                        upd += 1
                                        cur2.execute(f"""UPDATE main SET ballspinged={upd}""")
                                        conn2.commit()
                                        conn2.close()
                                        await interaction.response.defer()

                                    elif gennum == 2:
                                        self.disable_all_items()
                                        await interaction.message.edit(f"Player: ✂️\nBot: ✂️\n\nDraw! Now it's bot's turn to ping a ball! 🤜🤛", view=self)
                                        cur.execute(f"""UPDATE `{ctx.user.id}` SET rps=0""")
                                        cur.execute(f"""UPDATE `{ctx.user.id}` SET rpsbot=0""")
                                        cur.execute(f"""UPDATE `{ctx.user.id}` SET turn=0""")
                                        await ctx.respond(":robot:: Pong! 🏓")
                                        cur.execute(f"""UPDATE `{ctx.user.id}` SET turn=1""")
                                        conn.commit()
                                        conn.close()
                                        upd1 = cur2.execute(f"""SELECT ballspinged FROM main""").fetchone()
                                        upd2 = sum(upd1)
                                        upd = int(upd2)
                                        upd += 1
                                        cur2.execute(f"""UPDATE main SET ballspinged={upd}""")
                                        conn2.commit()
                                        conn2.close()
                                        await interaction.response.defer()

                                    else:
                                        self.disable_all_items()
                                        await interaction.message.edit(f"Player: ✂️\nBot: 📜\n\nPlayer won! Bot missed the shot, so <@{ctx.user.id}> has won this match! **Game over!** 🏆", view=self)
                                        cur.execute(f"""DROP TABLE `{ctx.user.id}`""")
                                        conn.commit()
                                        conn.close()
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

                                if rps2 == 4 and rps1 == 4:
                                    self.disable_all_items()
                                    await interaction.message.edit(f"Player 1: ✂️\nPlayer 2: ✂️\n\nDraw! Now it's <@{opponentid}>'s turn to ping a ball! 🤜🤛", view=self)
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

                                elif rps2 == 4 and rps1 == 3:
                                    self.disable_all_items()
                                    await interaction.message.edit(f"Player 1: 🪨\nPlayer 2: ✂️\n\nPlayer 1 won! <@{opponentid}> missed the shot, so <@{ctx.user.id}> won this match! **Game over!** 🏆", view=self)
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

                                elif rps2 == 4 and rps1 == 5:
                                    self.disable_all_items()
                                    await interaction.message.edit(f"Player 1: 📜\nPlayer 2: ✂️\n\nPlayer 2 won! Now it's <@{opponentid}>'s turn to ping a ball! 🏓", view=self)
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

                                conn.close()
                                
                            else:
                                await interaction.response.send_message("Sorry, but it's not your turn. <:crosspong:1134110291311992962>", ephemeral=True)
                        else:
                            await interaction.response.send_message("Sorry, but this action is not valid. Please check if you are playing this game or your opponent didn't leave the match. <:crosspong:1134110291311992962>", ephemeral=True)
                    except:
                        await interaction.response.send_message("Sorry, but this action is not valid. Please check if you are playing this game or your opponent didn't leave the match. <:crosspong:1134110291311992962>", ephemeral=True)

                @discord.ui.button(
                    label="Paper",
                    style=discord.ButtonStyle.primary,
                    emoji="📜"
                )

                async def paper_button_callback(self, button, interaction):
                    conn = sq.connect('datas.db')
                    cur = conn.cursor()

                    conn2 = sq.connect('stats.db')
                    cur2 = conn2.cursor()

                    try:
                        minigameid1 = cur.execute(f"""SELECT lastminigameid FROM `{interaction.user.id}`""").fetchone()
                        minigameid2 = sum(minigameid1)
                        minigameid = int(minigameid2)

                        if minigameid == self.message.id:
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
                                        self.disable_all_items()
                                        await interaction.message.edit(f"Player: 📜\nBot: 🪨\n\nPlayer won! Bot missed the shot, so <@{ctx.user.id}> has won this match! **Game over!** 🏆", view=self)
                                        cur.execute(f"""DROP TABLE `{ctx.user.id}`""")
                                        conn.commit()
                                        conn.close()
                                        upd1 = cur2.execute(f"""SELECT botgames FROM main""").fetchone()
                                        upd2 = sum(upd1)
                                        upd = int(upd2)
                                        upd -= 1
                                        cur2.execute(f"""UPDATE main SET botgames={upd}""")
                                        conn2.commit()
                                        conn2.close()
                                        await interaction.response.defer()

                                    elif gennum == 2:
                                        self.disable_all_items()
                                        await interaction.message.edit(f"Player: 📜\nBot: ✂️\n\nBot won! Now it's bot's turn to ping a ball! 🏓", view=self)
                                        cur.execute(f"""UPDATE `{ctx.user.id}` SET rps=0""")
                                        cur.execute(f"""UPDATE `{ctx.user.id}` SET rpsbot=0""")
                                        cur.execute(f"""UPDATE `{ctx.user.id}` SET turn=0""")
                                        await ctx.respond(":robot:: Pong! 🏓")
                                        cur.execute(f"""UPDATE `{ctx.user.id}` SET turn=1""")
                                        conn.commit()
                                        conn.close()
                                        upd1 = cur2.execute(f"""SELECT ballspinged FROM main""").fetchone()
                                        upd2 = sum(upd1)
                                        upd = int(upd2)
                                        upd += 1
                                        cur2.execute(f"""UPDATE main SET ballspinged={upd}""")
                                        conn2.commit()
                                        conn2.close()
                                        await interaction.response.defer()

                                    else:
                                        self.disable_all_items()
                                        await interaction.message.edit(f"Player: 📜\nBot: 📜\n\nDraw! Now it's bot's turn to ping a ball! 🤜🤛", view=self)
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
                                        conn.commit()
                                        conn.close()
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
                                
                                if rps2 == 5 and rps1 == 5:
                                    self.disable_all_items()
                                    await interaction.message.edit(f"Player 1: 📜\nPlayer 2: 📜\n\nDraw! Now it's <@{opponentid}>'s turn to ping a ball! 🤜🤛", view=self)
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

                                elif rps2 == 5 and rps1 == 4:
                                    self.disable_all_items()
                                    await interaction.message.edit(f"Player 1: ✂️\nPlayer 2: 📜\n\nPlayer 1 won! <@{opponentid}> missed the shot, so <@{ctx.user.id}> won this match! **Game over!** 🏆", view=self)
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

                                elif rps2 == 5 and rps1 == 3:
                                    self.disable_all_items()
                                    await interaction.message.edit(f"Player 1: 🪨\nPlayer 2: 📜\n\nPlayer 2 won! Now it's <@{opponentid}>'s turn to ping a ball! 🏓", view=self)
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

                                conn.close()
                                
                            else:
                                await interaction.response.send_message("Sorry, but it's not your turn. <:crosspong:1134110291311992962>", ephemeral=True)
                        else:
                            await interaction.response.send_message("Sorry, but this action is not valid. Please check if you are playing this game or your opponent didn't leave the match. <:crosspong:1134110291311992962>", ephemeral=True)
                    except:
                        await interaction.response.send_message("Sorry, but this action is not valid. Please check if you are playing this game or your opponent didn't leave the match. <:crosspong:1134110291311992962>", ephemeral=True)
        except:
            # I'll use this to print errors.
            pass

        inter = await ctx.respond(f"__**RPS TIME!**__ 🪨📜✂️\n\nIf <@{ctx.user.id}> wins, the minigame ends and this user wins this match. Other situations ends with <@{opponentid}>'s turn.\n\n<@{ctx.user.id}>, choose *Rock*, *Scissors* or *Paper*! <:circlepong:1134110288438894654>", view=rpsView())
        originalmsg = await inter.original_response()
        cur.execute(f"""UPDATE `{ctx.user.id}` SET lastminigameid={originalmsg.id}""")
        
        rpsbot1 = cur.execute(f"""SELECT rpsbot FROM `{ctx.user.id}`""").fetchone()
        rpsbot2 = sum(rpsbot1)
        rpsbot = int(rpsbot2)

        if rpsbot == 6:
            cur.execute(f"""UPDATE `{opponentid}` SET lastminigameid={originalmsg.id}""")

        conn.commit()
        conn.close()

    # Tic-Tac-Toe minigame (v1.3)
    
    async def ttt():
        # 0 - Not in-game
        # 1 - Waiting for turn
        # 2 - Deciding
        # 3 - Cannot play

        conn = sq.connect('datas.db')
        cur = conn.cursor()

        tttbot1 = cur.execute(f"""SELECT tttbot FROM `{ctx.user.id}`""").fetchone()
        tttbot2 = sum(tttbot1)
        tttbot = int(tttbot2)

        opponentid1 = cur.execute(f"""SELECT opponentid FROM `{ctx.user.id}`""").fetchone()
        opponentid2 = sum(opponentid1)
        opponentid = int(opponentid2)

        try:
            if tttbot == 3:
                cur.execute(f"""UPDATE `{opponentid}` SET tttturn=1""")
                cur.execute(f"""UPDATE `{ctx.user.id}` SET tttturn=2""")
                conn.commit()

            else:
                cur.execute(f"""UPDATE `{ctx.user.id}` SET tttturn=2""")
                cur.execute(f"""UPDATE `{ctx.user.id}` SET tttbot=1""")
                conn.commit()
            
            options = [
                discord.SelectOption(label="1"),
                discord.SelectOption(label="2"),
                discord.SelectOption(label="3"),
                discord.SelectOption(label="4"),
                discord.SelectOption(label="5"),
                discord.SelectOption(label="6"),
                discord.SelectOption(label="7"),
                discord.SelectOption(label="8"),
                discord.SelectOption(label="9")
            ]

            one1="<:one1:1164986232841982003>"
            two2="<:two2:1164986146539970632>"
            three3="<:three3:1164986176487305356>"
            four4="<:four4:1164986285715365909>"
            five5="<:five5:1164986312667967608>"
            six6="<:six6:1164986175312896081>"
            seven7="<:seven7:1164986188873072660>"
            eight8="<:eight8:1164986320922361856>"
            nine9="<:nine9:1164986246884499569>"

            class menuView(discord.ui.View):
                @discord.ui.select(
                        placeholder="Choose a position to place your symbol...",
                        options=options
                )
                
                async def select_callback(self, select, interaction):
                    # 1 - Nothing
                    # 2 - X
                    # 3 - O

                    conn = sq.connect('datas.db')
                    cur = conn.cursor()

                    conn2 = sq.connect('stats.db')
                    cur2 = conn.cursor()

                    try:
                        turn1 = cur.execute(f"""SELECT tttturn FROM `{interaction.user.id}`""").fetchone()
                        turn2 = sum(turn1)
                        interactiontttturn = int(turn2)

                        tttbot1 = cur.execute(f"""SELECT tttbot FROM `{ctx.user.id}`""").fetchone()
                        tttbot2 = sum(tttbot1)
                        tttbot = int(tttbot2)

                        opponentid1 = cur.execute(f"""SELECT opponentid FROM `{ctx.user.id}`""").fetchone()
                        opponentid2 = sum(opponentid1)
                        opponentid = int(opponentid2)

                        minigameid1 = cur.execute(f"""SELECT lastminigameid FROM `{interaction.user.id}`""").fetchone()
                        minigameid2 = sum(minigameid1)
                        minigameid = int(minigameid2)

                        if interactiontttturn == 2:
                            if interaction.user.id == ctx.user.id or interaction.user.id == opponentid:
                                if minigameid == self.message.id:
                                    needdefer = True
                                    anywin = True
                                    if select.values[0] == "1":
                                            tttgame1 = cur.execute(f"""SELECT tttgame FROM `{ctx.user.id}`""").fetchone()
                                            tttgame = int(''.join(map(str, tttgame1)))
                                            tttgame = [int(x) for x in str(tttgame)]

                                            if tttgame[0] == 1:
                                                if tttbot == 3:
                                                    if interaction.user.id == ctx.user.id:
                                                        tttgame[0] = 2
                                                        tttgameint = f"{tttgame[0]}{tttgame[1]}{tttgame[2]}{tttgame[3]}{tttgame[4]}{tttgame[5]}{tttgame[6]}{tttgame[7]}{tttgame[8]}"
                                                        tttgameint = int(tttgameint)
                                                        cur.execute(f"""UPDATE `{ctx.user.id}` SET tttgame={tttgameint}""")
                                                        cur.execute(f"""UPDATE `{opponentid}` SET tttgame={tttgameint}""")
                                                        cur.execute(f"""UPDATE `{ctx.user.id}` SET tttturn=1""")
                                                        cur.execute(f"""UPDATE `{opponentid}` SET tttturn=2""")
                                                        conn.commit()

                                                    elif interaction.user.id == opponentid:
                                                        tttgame[0] = 3
                                                        tttgameint = f"{tttgame[0]}{tttgame[1]}{tttgame[2]}{tttgame[3]}{tttgame[4]}{tttgame[5]}{tttgame[6]}{tttgame[7]}{tttgame[8]}"
                                                        tttgameint = int(tttgameint)
                                                        cur.execute(f"""UPDATE `{ctx.user.id}` SET tttgame={tttgameint}""")
                                                        cur.execute(f"""UPDATE `{opponentid}` SET tttgame={tttgameint}""")
                                                        cur.execute(f"""UPDATE `{ctx.user.id}` SET tttturn=2""")
                                                        cur.execute(f"""UPDATE `{opponentid}` SET tttturn=1""")
                                                        conn.commit()

                                                else:
                                                    if interaction.user.id == ctx.user.id:
                                                        tttgame[0] = 2
                                                        tttgameint = f"{tttgame[0]}{tttgame[1]}{tttgame[2]}{tttgame[3]}{tttgame[4]}{tttgame[5]}{tttgame[6]}{tttgame[7]}{tttgame[8]}"
                                                        tttgameint = int(tttgameint)
                                                        cur.execute(f"""UPDATE `{ctx.user.id}` SET tttgame={tttgameint}""")
                                                        cur.execute(f"""UPDATE `{ctx.user.id}` SET tttturn=1""")
                                                        cur.execute(f"""UPDATE `{ctx.user.id}` SET tttbot=2""")
                                                        conn.commit()

                                                    else:
                                                        await interaction.response.send_message("Sorry, but this action is not valid. Please check if you are playing this game or your opponent didn't leave the match. <:crosspong:1134110291311992962>", ephemeral=True)
                                                        needdefer = False

                                            else:
                                                await interaction.response.send_message("This field is occupied! Please choose antoher one. <:crosspong:1134110291311992962>", ephemeral=True)
                                                needdefer = False

                                    if select.values[0] == "2":
                                            tttgame1 = cur.execute(f"""SELECT tttgame FROM `{ctx.user.id}`""").fetchone()
                                            tttgame = int(''.join(map(str, tttgame1)))
                                            tttgame = [int(x) for x in str(tttgame)]

                                            if tttgame[1] == 1:
                                                if tttbot == 3:
                                                    if interaction.user.id == ctx.user.id:
                                                        tttgame[1] = 2
                                                        tttgameint = f"{tttgame[0]}{tttgame[1]}{tttgame[2]}{tttgame[3]}{tttgame[4]}{tttgame[5]}{tttgame[6]}{tttgame[7]}{tttgame[8]}"
                                                        tttgameint = int(tttgameint)
                                                        cur.execute(f"""UPDATE `{ctx.user.id}` SET tttgame={tttgameint}""")
                                                        cur.execute(f"""UPDATE `{opponentid}` SET tttgame={tttgameint}""")
                                                        cur.execute(f"""UPDATE `{ctx.user.id}` SET tttturn=1""")
                                                        cur.execute(f"""UPDATE `{opponentid}` SET tttturn=2""")
                                                        conn.commit()

                                                    elif interaction.user.id == opponentid:
                                                        tttgame[1] = 3
                                                        tttgameint = f"{tttgame[0]}{tttgame[1]}{tttgame[2]}{tttgame[3]}{tttgame[4]}{tttgame[5]}{tttgame[6]}{tttgame[7]}{tttgame[8]}"
                                                        tttgameint = int(tttgameint)
                                                        cur.execute(f"""UPDATE `{ctx.user.id}` SET tttgame={tttgameint}""")
                                                        cur.execute(f"""UPDATE `{opponentid}` SET tttgame={tttgameint}""")
                                                        cur.execute(f"""UPDATE `{ctx.user.id}` SET tttturn=2""")
                                                        cur.execute(f"""UPDATE `{opponentid}` SET tttturn=1""")
                                                        conn.commit()
                                                else:
                                                    if interaction.user.id == ctx.user.id:
                                                        tttgame[1] = 2
                                                        tttgameint = f"{tttgame[0]}{tttgame[1]}{tttgame[2]}{tttgame[3]}{tttgame[4]}{tttgame[5]}{tttgame[6]}{tttgame[7]}{tttgame[8]}"
                                                        tttgameint = int(tttgameint)
                                                        cur.execute(f"""UPDATE `{ctx.user.id}` SET tttgame={tttgameint}""")
                                                        cur.execute(f"""UPDATE `{ctx.user.id}` SET tttturn=1""")
                                                        cur.execute(f"""UPDATE `{ctx.user.id}` SET tttbot=2""")
                                                        conn.commit()

                                                    else:
                                                        await interaction.response.send_message("Sorry, but this action is not valid. Please check if you are playing this game or your opponent didn't leave the match. <:crosspong:1134110291311992962>", ephemeral=True)
                                                        needdefer = False

                                            else:
                                                await interaction.response.send_message("This field is occupied! Please choose antoher one. <:crosspong:1134110291311992962>", ephemeral=True)
                                                needdefer = False

                                    if select.values[0] == "3":
                                            tttgame1 = cur.execute(f"""SELECT tttgame FROM `{ctx.user.id}`""").fetchone()
                                            tttgame = int(''.join(map(str, tttgame1)))
                                            tttgame = [int(x) for x in str(tttgame)]

                                            if tttgame[2] == 1:
                                                if tttbot == 3:
                                                    if interaction.user.id == ctx.user.id:
                                                        tttgame[2] = 2
                                                        tttgameint = f"{tttgame[0]}{tttgame[1]}{tttgame[2]}{tttgame[3]}{tttgame[4]}{tttgame[5]}{tttgame[6]}{tttgame[7]}{tttgame[8]}"
                                                        tttgameint = int(tttgameint)
                                                        cur.execute(f"""UPDATE `{ctx.user.id}` SET tttgame={tttgameint}""")
                                                        cur.execute(f"""UPDATE `{opponentid}` SET tttgame={tttgameint}""")
                                                        cur.execute(f"""UPDATE `{ctx.user.id}` SET tttturn=1""")
                                                        cur.execute(f"""UPDATE `{opponentid}` SET tttturn=2""")
                                                        conn.commit()

                                                    elif interaction.user.id == opponentid:
                                                        tttgame[2] = 3
                                                        tttgameint = f"{tttgame[0]}{tttgame[1]}{tttgame[2]}{tttgame[3]}{tttgame[4]}{tttgame[5]}{tttgame[6]}{tttgame[7]}{tttgame[8]}"
                                                        tttgameint = int(tttgameint)
                                                        cur.execute(f"""UPDATE `{ctx.user.id}` SET tttgame={tttgameint}""")
                                                        cur.execute(f"""UPDATE `{opponentid}` SET tttgame={tttgameint}""")
                                                        cur.execute(f"""UPDATE `{ctx.user.id}` SET tttturn=2""")
                                                        cur.execute(f"""UPDATE `{opponentid}` SET tttturn=1""")
                                                        conn.commit()
                                                else:
                                                    if interaction.user.id == ctx.user.id:
                                                        tttgame[2] = 2
                                                        tttgameint = f"{tttgame[0]}{tttgame[1]}{tttgame[2]}{tttgame[3]}{tttgame[4]}{tttgame[5]}{tttgame[6]}{tttgame[7]}{tttgame[8]}"
                                                        tttgameint = int(tttgameint)
                                                        cur.execute(f"""UPDATE `{ctx.user.id}` SET tttgame={tttgameint}""")
                                                        cur.execute(f"""UPDATE `{ctx.user.id}` SET tttturn=1""")
                                                        cur.execute(f"""UPDATE `{ctx.user.id}` SET tttbot=2""")
                                                        conn.commit()

                                                    else:
                                                        await interaction.response.send_message("Sorry, but this action is not valid. Please check if you are playing this game or your opponent didn't leave the match. <:crosspong:1134110291311992962>", ephemeral=True)
                                                        needdefer = False

                                            else:
                                                await interaction.response.send_message("This field is occupied! Please choose antoher one. <:crosspong:1134110291311992962>", ephemeral=True)
                                                needdefer = False
                                                
                                    if select.values[0] == "4":
                                            tttgame1 = cur.execute(f"""SELECT tttgame FROM `{ctx.user.id}`""").fetchone()
                                            tttgame = int(''.join(map(str, tttgame1)))
                                            tttgame = [int(x) for x in str(tttgame)]

                                            if tttgame[3] == 1:
                                                if tttbot == 3:
                                                    if interaction.user.id == ctx.user.id:
                                                        tttgame[3] = 2
                                                        tttgameint = f"{tttgame[0]}{tttgame[1]}{tttgame[2]}{tttgame[3]}{tttgame[4]}{tttgame[5]}{tttgame[6]}{tttgame[7]}{tttgame[8]}"
                                                        tttgameint = int(tttgameint)
                                                        cur.execute(f"""UPDATE `{ctx.user.id}` SET tttgame={tttgameint}""")
                                                        cur.execute(f"""UPDATE `{opponentid}` SET tttgame={tttgameint}""")
                                                        cur.execute(f"""UPDATE `{ctx.user.id}` SET tttturn=1""")
                                                        cur.execute(f"""UPDATE `{opponentid}` SET tttturn=2""")
                                                        conn.commit()

                                                    elif interaction.user.id == opponentid:
                                                        tttgame[3] = 3
                                                        tttgameint = f"{tttgame[0]}{tttgame[1]}{tttgame[2]}{tttgame[3]}{tttgame[4]}{tttgame[5]}{tttgame[6]}{tttgame[7]}{tttgame[8]}"
                                                        tttgameint = int(tttgameint)
                                                        cur.execute(f"""UPDATE `{ctx.user.id}` SET tttgame={tttgameint}""")
                                                        cur.execute(f"""UPDATE `{opponentid}` SET tttgame={tttgameint}""")
                                                        cur.execute(f"""UPDATE `{ctx.user.id}` SET tttturn=2""")
                                                        cur.execute(f"""UPDATE `{opponentid}` SET tttturn=1""")
                                                        conn.commit()

                                                else:
                                                    if interaction.user.id == ctx.user.id:
                                                        tttgame[3] = 2
                                                        tttgameint = f"{tttgame[0]}{tttgame[1]}{tttgame[2]}{tttgame[3]}{tttgame[4]}{tttgame[5]}{tttgame[6]}{tttgame[7]}{tttgame[8]}"
                                                        tttgameint = int(tttgameint)
                                                        cur.execute(f"""UPDATE `{ctx.user.id}` SET tttgame={tttgameint}""")
                                                        cur.execute(f"""UPDATE `{ctx.user.id}` SET tttturn=1""")
                                                        cur.execute(f"""UPDATE `{ctx.user.id}` SET tttbot=2""")
                                                        conn.commit()

                                                    else:
                                                        await interaction.response.send_message("Sorry, but this action is not valid. Please check if you are playing this game or your opponent didn't leave the match. <:crosspong:1134110291311992962>", ephemeral=True)
                                                        needdefer = False

                                            else:
                                                await interaction.response.send_message("This field is occupied! Please choose antoher one. <:crosspong:1134110291311992962>", ephemeral=True)
                                                needdefer = False
                                                
                                    if select.values[0] == "5":
                                            tttgame1 = cur.execute(f"""SELECT tttgame FROM `{ctx.user.id}`""").fetchone()
                                            tttgame = int(''.join(map(str, tttgame1)))
                                            tttgame = [int(x) for x in str(tttgame)]

                                            if tttgame[4] == 1:
                                                if tttbot == 3:
                                                    if interaction.user.id == ctx.user.id:
                                                        tttgame[4] = 2
                                                        tttgameint = f"{tttgame[0]}{tttgame[1]}{tttgame[2]}{tttgame[3]}{tttgame[4]}{tttgame[5]}{tttgame[6]}{tttgame[7]}{tttgame[8]}"
                                                        tttgameint = int(tttgameint)
                                                        cur.execute(f"""UPDATE `{ctx.user.id}` SET tttgame={tttgameint}""")
                                                        cur.execute(f"""UPDATE `{opponentid}` SET tttgame={tttgameint}""")
                                                        cur.execute(f"""UPDATE `{ctx.user.id}` SET tttturn=1""")
                                                        cur.execute(f"""UPDATE `{opponentid}` SET tttturn=2""")
                                                        conn.commit()

                                                    elif interaction.user.id == opponentid:
                                                        tttgame[4] = 3
                                                        tttgameint = f"{tttgame[0]}{tttgame[1]}{tttgame[2]}{tttgame[3]}{tttgame[4]}{tttgame[5]}{tttgame[6]}{tttgame[7]}{tttgame[8]}"
                                                        tttgameint = int(tttgameint)
                                                        cur.execute(f"""UPDATE `{ctx.user.id}` SET tttgame={tttgameint}""")
                                                        cur.execute(f"""UPDATE `{opponentid}` SET tttgame={tttgameint}""")
                                                        cur.execute(f"""UPDATE `{ctx.user.id}` SET tttturn=2""")
                                                        cur.execute(f"""UPDATE `{opponentid}` SET tttturn=1""")
                                                        conn.commit()

                                                else:
                                                    if interaction.user.id == ctx.user.id:
                                                        tttgame[4] = 2
                                                        tttgameint = f"{tttgame[0]}{tttgame[1]}{tttgame[2]}{tttgame[3]}{tttgame[4]}{tttgame[5]}{tttgame[6]}{tttgame[7]}{tttgame[8]}"
                                                        tttgameint = int(tttgameint)
                                                        cur.execute(f"""UPDATE `{ctx.user.id}` SET tttgame={tttgameint}""")
                                                        cur.execute(f"""UPDATE `{ctx.user.id}` SET tttturn=1""")
                                                        cur.execute(f"""UPDATE `{ctx.user.id}` SET tttbot=2""")
                                                        conn.commit()

                                                    else:
                                                        await interaction.response.send_message("Sorry, but this action is not valid. Please check if you are playing this game or your opponent didn't leave the match. <:crosspong:1134110291311992962>", ephemeral=True)
                                                        needdefer = False

                                            else:
                                                await interaction.response.send_message("This field is occupied! Please choose antoher one. <:crosspong:1134110291311992962>", ephemeral=True)
                                                needdefer = False

                                    if select.values[0] == "6":
                                            tttgame1 = cur.execute(f"""SELECT tttgame FROM `{ctx.user.id}`""").fetchone()
                                            tttgame = int(''.join(map(str, tttgame1)))
                                            tttgame = [int(x) for x in str(tttgame)]

                                            if tttgame[5] == 1:
                                                if tttbot == 3:
                                                    if interaction.user.id == ctx.user.id:
                                                        tttgame[5] = 2
                                                        tttgameint = f"{tttgame[0]}{tttgame[1]}{tttgame[2]}{tttgame[3]}{tttgame[4]}{tttgame[5]}{tttgame[6]}{tttgame[7]}{tttgame[8]}"
                                                        tttgameint = int(tttgameint)
                                                        cur.execute(f"""UPDATE `{ctx.user.id}` SET tttgame={tttgameint}""")
                                                        cur.execute(f"""UPDATE `{opponentid}` SET tttgame={tttgameint}""")
                                                        cur.execute(f"""UPDATE `{ctx.user.id}` SET tttturn=1""")
                                                        cur.execute(f"""UPDATE `{opponentid}` SET tttturn=2""")
                                                        conn.commit()

                                                    elif interaction.user.id == opponentid:
                                                        tttgame[5] = 3
                                                        tttgameint = f"{tttgame[0]}{tttgame[1]}{tttgame[2]}{tttgame[3]}{tttgame[4]}{tttgame[5]}{tttgame[6]}{tttgame[7]}{tttgame[8]}"
                                                        tttgameint = int(tttgameint)
                                                        cur.execute(f"""UPDATE `{ctx.user.id}` SET tttgame={tttgameint}""")
                                                        cur.execute(f"""UPDATE `{opponentid}` SET tttgame={tttgameint}""")
                                                        cur.execute(f"""UPDATE `{ctx.user.id}` SET tttturn=2""")
                                                        cur.execute(f"""UPDATE `{opponentid}` SET tttturn=1""")
                                                        conn.commit()

                                                else:
                                                    if interaction.user.id == ctx.user.id:
                                                        tttgame[5] = 2
                                                        tttgameint = f"{tttgame[0]}{tttgame[1]}{tttgame[2]}{tttgame[3]}{tttgame[4]}{tttgame[5]}{tttgame[6]}{tttgame[7]}{tttgame[8]}"
                                                        tttgameint = int(tttgameint)
                                                        cur.execute(f"""UPDATE `{ctx.user.id}` SET tttgame={tttgameint}""")
                                                        cur.execute(f"""UPDATE `{ctx.user.id}` SET tttturn=1""")
                                                        cur.execute(f"""UPDATE `{ctx.user.id}` SET tttbot=2""")
                                                        conn.commit()

                                                    else:
                                                        await interaction.response.send_message("Sorry, but this action is not valid. Please check if you are playing this game or your opponent didn't leave the match. <:crosspong:1134110291311992962>", ephemeral=True)
                                                        needdefer = False

                                            else:
                                                await interaction.response.send_message("This field is occupied! Please choose antoher one. <:crosspong:1134110291311992962>", ephemeral=True)
                                                needdefer = False

                                    if select.values[0] == "7":
                                            tttgame1 = cur.execute(f"""SELECT tttgame FROM `{ctx.user.id}`""").fetchone()
                                            tttgame = int(''.join(map(str, tttgame1)))
                                            tttgame = [int(x) for x in str(tttgame)]

                                            if tttgame[6] == 1:
                                                if tttbot == 3:
                                                    if interaction.user.id == ctx.user.id:
                                                        tttgame[6] = 2
                                                        tttgameint = f"{tttgame[0]}{tttgame[1]}{tttgame[2]}{tttgame[3]}{tttgame[4]}{tttgame[5]}{tttgame[6]}{tttgame[7]}{tttgame[8]}"
                                                        tttgameint = int(tttgameint)
                                                        cur.execute(f"""UPDATE `{ctx.user.id}` SET tttgame={tttgameint}""")
                                                        cur.execute(f"""UPDATE `{opponentid}` SET tttgame={tttgameint}""")
                                                        cur.execute(f"""UPDATE `{ctx.user.id}` SET tttturn=1""")
                                                        cur.execute(f"""UPDATE `{opponentid}` SET tttturn=2""")
                                                        conn.commit()

                                                    elif interaction.user.id == opponentid:
                                                        tttgame[6] = 3
                                                        tttgameint = f"{tttgame[0]}{tttgame[1]}{tttgame[2]}{tttgame[3]}{tttgame[4]}{tttgame[5]}{tttgame[6]}{tttgame[7]}{tttgame[8]}"
                                                        tttgameint = int(tttgameint)
                                                        cur.execute(f"""UPDATE `{ctx.user.id}` SET tttgame={tttgameint}""")
                                                        cur.execute(f"""UPDATE `{opponentid}` SET tttgame={tttgameint}""")
                                                        cur.execute(f"""UPDATE `{ctx.user.id}` SET tttturn=2""")
                                                        cur.execute(f"""UPDATE `{opponentid}` SET tttturn=1""")
                                                        conn.commit()

                                                else:
                                                    if interaction.user.id == ctx.user.id:
                                                        tttgame[6] = 2
                                                        tttgameint = f"{tttgame[0]}{tttgame[1]}{tttgame[2]}{tttgame[3]}{tttgame[4]}{tttgame[5]}{tttgame[6]}{tttgame[7]}{tttgame[8]}"
                                                        tttgameint = int(tttgameint)
                                                        cur.execute(f"""UPDATE `{ctx.user.id}` SET tttgame={tttgameint}""")
                                                        cur.execute(f"""UPDATE `{ctx.user.id}` SET tttturn=1""")
                                                        cur.execute(f"""UPDATE `{ctx.user.id}` SET tttbot=2""")
                                                        conn.commit()

                                                    else:
                                                        await interaction.response.send_message("Sorry, but this action is not valid. Please check if you are playing this game or your opponent didn't leave the match. <:crosspong:1134110291311992962>", ephemeral=True)
                                                        needdefer = False

                                            else:
                                                await interaction.response.send_message("This field is occupied! Please choose antoher one. <:crosspong:1134110291311992962>", ephemeral=True)
                                                needdefer = False

                                    if select.values[0] == "8":
                                            tttgame1 = cur.execute(f"""SELECT tttgame FROM `{ctx.user.id}`""").fetchone()
                                            tttgame = int(''.join(map(str, tttgame1)))
                                            tttgame = [int(x) for x in str(tttgame)]

                                            if tttgame[7] == 1:
                                                if tttbot == 3:
                                                    if interaction.user.id == ctx.user.id:
                                                        tttgame[7] = 2
                                                        tttgameint = f"{tttgame[0]}{tttgame[1]}{tttgame[2]}{tttgame[3]}{tttgame[4]}{tttgame[5]}{tttgame[6]}{tttgame[7]}{tttgame[8]}"
                                                        tttgameint = int(tttgameint)
                                                        cur.execute(f"""UPDATE `{ctx.user.id}` SET tttgame={tttgameint}""")
                                                        cur.execute(f"""UPDATE `{opponentid}` SET tttgame={tttgameint}""")
                                                        cur.execute(f"""UPDATE `{ctx.user.id}` SET tttturn=1""")
                                                        cur.execute(f"""UPDATE `{opponentid}` SET tttturn=2""")
                                                        conn.commit()

                                                    elif interaction.user.id == opponentid:
                                                        tttgame[7] = 3
                                                        tttgameint = f"{tttgame[0]}{tttgame[1]}{tttgame[2]}{tttgame[3]}{tttgame[4]}{tttgame[5]}{tttgame[6]}{tttgame[7]}{tttgame[8]}"
                                                        tttgameint = int(tttgameint)
                                                        cur.execute(f"""UPDATE `{ctx.user.id}` SET tttgame={tttgameint}""")
                                                        cur.execute(f"""UPDATE `{opponentid}` SET tttgame={tttgameint}""")
                                                        cur.execute(f"""UPDATE `{ctx.user.id}` SET tttturn=2""")
                                                        cur.execute(f"""UPDATE `{opponentid}` SET tttturn=1""")
                                                        conn.commit()

                                                else:
                                                    if interaction.user.id == ctx.user.id:
                                                        tttgame[7] = 2
                                                        tttgameint = f"{tttgame[0]}{tttgame[1]}{tttgame[2]}{tttgame[3]}{tttgame[4]}{tttgame[5]}{tttgame[6]}{tttgame[7]}{tttgame[8]}"
                                                        tttgameint = int(tttgameint)
                                                        cur.execute(f"""UPDATE `{ctx.user.id}` SET tttgame={tttgameint}""")
                                                        cur.execute(f"""UPDATE `{ctx.user.id}` SET tttturn=1""")
                                                        cur.execute(f"""UPDATE `{ctx.user.id}` SET tttbot=2""")
                                                        conn.commit()

                                                    else:
                                                        await interaction.response.send_message("Sorry, but this action is not valid. Please check if you are playing this game or your opponent didn't leave the match. <:crosspong:1134110291311992962>", ephemeral=True)
                                                        needdefer = False

                                            else:
                                                await interaction.response.send_message("This field is occupied! Please choose antoher one. <:crosspong:1134110291311992962>", ephemeral=True)
                                                needdefer = False

                                    if select.values[0] == "9":
                                            tttgame1 = cur.execute(f"""SELECT tttgame FROM `{ctx.user.id}`""").fetchone()
                                            tttgame = int(''.join(map(str, tttgame1)))
                                            tttgame = [int(x) for x in str(tttgame)]

                                            if tttgame[8] == 1:
                                                if tttbot == 3:
                                                    if interaction.user.id == ctx.user.id:
                                                        tttgame[8] = 2
                                                        tttgameint = f"{tttgame[0]}{tttgame[1]}{tttgame[2]}{tttgame[3]}{tttgame[4]}{tttgame[5]}{tttgame[6]}{tttgame[7]}{tttgame[8]}"
                                                        tttgameint = int(tttgameint)
                                                        cur.execute(f"""UPDATE `{ctx.user.id}` SET tttgame={tttgameint}""")
                                                        cur.execute(f"""UPDATE `{opponentid}` SET tttgame={tttgameint}""")
                                                        cur.execute(f"""UPDATE `{ctx.user.id}` SET tttturn=1""")
                                                        cur.execute(f"""UPDATE `{opponentid}` SET tttturn=2""")
                                                        conn.commit()

                                                    elif interaction.user.id == opponentid:
                                                        tttgame[8] = 3
                                                        tttgameint = f"{tttgame[0]}{tttgame[1]}{tttgame[2]}{tttgame[3]}{tttgame[4]}{tttgame[5]}{tttgame[6]}{tttgame[7]}{tttgame[8]}"
                                                        tttgameint = int(tttgameint)
                                                        cur.execute(f"""UPDATE `{ctx.user.id}` SET tttgame={tttgameint}""")
                                                        cur.execute(f"""UPDATE `{opponentid}` SET tttgame={tttgameint}""")
                                                        cur.execute(f"""UPDATE `{ctx.user.id}` SET tttturn=2""")
                                                        cur.execute(f"""UPDATE `{opponentid}` SET tttturn=1""")
                                                        conn.commit()

                                                else:
                                                    if interaction.user.id == ctx.user.id:
                                                        tttgame[8] = 2
                                                        tttgameint = f"{tttgame[0]}{tttgame[1]}{tttgame[2]}{tttgame[3]}{tttgame[4]}{tttgame[5]}{tttgame[6]}{tttgame[7]}{tttgame[8]}"
                                                        tttgameint = int(tttgameint)
                                                        cur.execute(f"""UPDATE `{ctx.user.id}` SET tttgame={tttgameint}""")
                                                        cur.execute(f"""UPDATE `{ctx.user.id}` SET tttturn=1""")
                                                        cur.execute(f"""UPDATE `{ctx.user.id}` SET tttbot=2""")
                                                        conn.commit()

                                                    else:
                                                        await interaction.response.send_message("Sorry, but this action is not valid. Please check if you are playing this game or your opponent didn't leave the match. <:crosspong:1134110291311992962>", ephemeral=True)
                                                        needdefer = False

                                            else:
                                                await interaction.response.send_message("This field is occupied! Please choose antoher one. <:crosspong:1134110291311992962>", ephemeral=True)
                                                needdefer = False

                                    # "<:one1:1164986232841982003>"
                                    # "<:two2:1164986146539970632>"
                                    # "<:three3:1164986176487305356>"
                                    # "<:four4:1164986285715365909>"
                                    # "<:five5:1164986312667967608>"
                                    # "<:six6:1164986175312896081>"
                                    # "<:seven7:1164986188873072660>"
                                    # "<:eight8:1164986320922361856>"
                                    # "<:nine9:1164986246884499569>"
                                    # "<:bluex:1164986327167672361>"
                                    # "<:redo:1164986221118902362>"
                                    #
                                    # CTX.USER.ID = X
                                    # OPPONENTID = O
                                    #
                                    # 2 - X
                                    # 3 - 0

                                    # 0 1 2
                                    # 3 4 5
                                    # 6 7 8

                                    if tttgame[0] == 1:
                                        one1 = "<:one1:1164986232841982003>"

                                    elif tttgame[0] == 2:
                                        one1 = "<:bluex:1164986327167672361>"
                                    
                                    else:
                                        one1 = "<:redo:1164986221118902362>"

                                    if tttgame[1] == 1:
                                        two2 = "<:two2:1164986146539970632>"

                                    elif tttgame[1] == 2:
                                        two2 = "<:bluex:1164986327167672361>"
                                    
                                    else:
                                        two2 = "<:redo:1164986221118902362>"

                                    if tttgame[2] == 1:
                                        three3 = "<:three3:1164986176487305356>"

                                    elif tttgame[2] == 2:
                                        three3 = "<:bluex:1164986327167672361>"
                                    
                                    else:
                                        three3 = "<:redo:1164986221118902362>"

                                    if tttgame[3] == 1:
                                        four4 = "<:four4:1164986285715365909>"

                                    elif tttgame[3] == 2:
                                        four4 = "<:bluex:1164986327167672361>"
                                    
                                    else:
                                        four4 = "<:redo:1164986221118902362>"

                                    if tttgame[4] == 1:
                                        five5 = "<:five5:1164986312667967608>"

                                    elif tttgame[4] == 2:
                                        five5 = "<:bluex:1164986327167672361>"
                                    
                                    else:
                                        five5 = "<:redo:1164986221118902362>"

                                    if tttgame[5] == 1:
                                        six6 = "<:six6:1164986175312896081>"

                                    elif tttgame[5] == 2:
                                        six6 = "<:bluex:1164986327167672361>"
                                    
                                    else:
                                        six6 = "<:redo:1164986221118902362>"

                                    if tttgame[6] == 1:
                                        seven7 = "<:seven7:1164986188873072660>"

                                    elif tttgame[6] == 2:
                                        seven7 = "<:bluex:1164986327167672361>"
                                    
                                    else:
                                        seven7 = "<:redo:1164986221118902362>"

                                    if tttgame[7] == 1:
                                        eight8 = "<:eight8:1164986320922361856>"

                                    elif tttgame[7] == 2:
                                        eight8 = "<:bluex:1164986327167672361>"
                                    
                                    else:
                                        eight8 = "<:redo:1164986221118902362>"

                                    if tttgame[8] == 1:
                                        nine9 = "<:nine9:1164986246884499569>"

                                    elif tttgame[8] == 2:
                                        nine9 = "<:bluex:1164986327167672361>"
                                    
                                    else:
                                        nine9 = "<:redo:1164986221118902362>"

                                    msgtext = f"{one1}<:whitelinevertical:1164986150113513624>{two2}<:whitelinevertical:1164986150113513624>{three3}\n<:whitelinehorizontal:1164986148205109308><:whiteplus:1164986151849959495><:whitelinehorizontal:1164986148205109308><:whiteplus:1164986151849959495><:whitelinehorizontal:1164986148205109308>\n{four4}<:whitelinevertical:1164986150113513624>{five5}<:whitelinevertical:1164986150113513624>{six6}\n<:whitelinehorizontal:1164986148205109308><:whiteplus:1164986151849959495><:whitelinehorizontal:1164986148205109308><:whiteplus:1164986151849959495><:whitelinehorizontal:1164986148205109308>\n{seven7}<:whitelinevertical:1164986150113513624>{eight8}<:whitelinevertical:1164986150113513624>{nine9}"

                                    if tttbot != 3:
                                        if tttgame[0] == 2 and tttgame[3] == 2 and tttgame [6] == 2:
                                            self.disable_all_items()
                                            await interaction.message.edit(f"<@{ctx.user.id}> won! This user won this match as well! Congratulations! 🏆<:bluex:1164986327167672361>\n\n{msgtext}", view=self)
                                            cur.execute(f"""DROP TABLE `{ctx.user.id}`""")
                                            conn.commit()
                                            anywin = False
                                            await interaction.response.defer()

                                        elif tttgame[1] == 2 and tttgame[4] == 2 and tttgame [7] == 2:
                                            self.disable_all_items()
                                            await interaction.message.edit(f"<@{ctx.user.id}> won! This user won this match as well! Congratulations! 🏆<:bluex:1164986327167672361>\n\n{msgtext}", view=self)
                                            cur.execute(f"""DROP TABLE `{ctx.user.id}`""")
                                            conn.commit()
                                            anywin = False
                                            await interaction.response.defer()
                                            
                                        elif tttgame[2] == 2 and tttgame[5] == 2 and tttgame [8] == 2:
                                            self.disable_all_items()
                                            await interaction.message.edit(f"<@{ctx.user.id}> won! This user won this match as well! Congratulations! 🏆<:bluex:1164986327167672361>\n\n{msgtext}", view=self)
                                            cur.execute(f"""DROP TABLE `{ctx.user.id}`""")
                                            conn.commit()
                                            anywin = False
                                            await interaction.response.defer()
                                            
                                        elif tttgame[0] == 2 and tttgame[1] == 2 and tttgame [2] == 2:
                                            self.disable_all_items()
                                            await interaction.message.edit(f"<@{ctx.user.id}> won! This user won this match as well! Congratulations! 🏆<:bluex:1164986327167672361>\n\n{msgtext}", view=self)
                                            cur.execute(f"""DROP TABLE `{ctx.user.id}`""")
                                            conn.commit()
                                            anywin = False
                                            await interaction.response.defer()

                                        elif tttgame[3] == 2 and tttgame[4] == 2 and tttgame [5] == 2:
                                            self.disable_all_items()
                                            await interaction.message.edit(f"<@{ctx.user.id}> won! This user won this match as well! Congratulations! 🏆<:bluex:1164986327167672361>\n\n{msgtext}", view=self)
                                            cur.execute(f"""DROP TABLE `{ctx.user.id}`""")
                                            conn.commit()
                                            anywin = False
                                            await interaction.response.defer()

                                        elif tttgame[6] == 2 and tttgame[7] == 2 and tttgame [8] == 2:
                                            self.disable_all_items()
                                            await interaction.message.edit(f"<@{ctx.user.id}> won! This user won this match as well! Congratulations! 🏆<:bluex:1164986327167672361>\n\n{msgtext}", view=self)
                                            cur.execute(f"""DROP TABLE `{ctx.user.id}`""")
                                            conn.commit()
                                            anywin = False
                                            await interaction.response.defer()

                                        elif tttgame[0] == 2 and tttgame[4] == 2 and tttgame [8] == 2:
                                            self.disable_all_items()
                                            await interaction.message.edit(f"<@{ctx.user.id}> won! This user won this match as well! Congratulations! 🏆<:bluex:1164986327167672361>\n\n{msgtext}", view=self)
                                            cur.execute(f"""DROP TABLE `{ctx.user.id}`""")
                                            conn.commit()
                                            anywin = False
                                            await interaction.response.defer()

                                        elif tttgame[2] == 2 and tttgame[4] == 2 and tttgame [6] == 2:
                                            self.disable_all_items()
                                            await interaction.message.edit(f"<@{ctx.user.id}> won! This user won this match as well! Congratulations! 🏆<:bluex:1164986327167672361>\n\n{msgtext}", view=self)
                                            cur.execute(f"""DROP TABLE `{ctx.user.id}`""")
                                            conn.commit()
                                            anywin = False
                                            await interaction.response.defer()

                                    else:
                                        if tttgame[0] == 2 and tttgame[3] == 2 and tttgame [6] == 2:
                                            self.disable_all_items()
                                            await interaction.message.edit(f"<@{ctx.user.id}> won! This user won this match as well! Congratulations! 🏆<:bluex:1164986327167672361>\n\n{msgtext}", view=self)
                                            cur.execute(f"""DROP TABLE `{ctx.user.id}`""")
                                            cur.execute(f"""DROP TABLE `{opponentid}`""")
                                            conn.commit()
                                            anywin = False
                                            await interaction.response.defer()

                                        elif tttgame[1] == 2 and tttgame[4] == 2 and tttgame [7] == 2:
                                            self.disable_all_items()
                                            await interaction.message.edit(f"<@{ctx.user.id}> won! This user won this match as well! Congratulations! 🏆<:bluex:1164986327167672361>\n\n{msgtext}", view=self)
                                            cur.execute(f"""DROP TABLE `{ctx.user.id}`""")
                                            cur.execute(f"""DROP TABLE `{opponentid}`""")
                                            conn.commit()
                                            anywin = False
                                            await interaction.response.defer()
                                            
                                        elif tttgame[2] == 2 and tttgame[5] == 2 and tttgame [8] == 2:
                                            self.disable_all_items()
                                            await interaction.message.edit(f"<@{ctx.user.id}> won! This user won this match as well! Congratulations! 🏆<:bluex:1164986327167672361>\n\n{msgtext}", view=self)
                                            cur.execute(f"""DROP TABLE `{ctx.user.id}`""")
                                            cur.execute(f"""DROP TABLE `{opponentid}`""")
                                            conn.commit()
                                            anywin = False
                                            await interaction.response.defer()
                                            
                                        elif tttgame[0] == 2 and tttgame[1] == 2 and tttgame [2] == 2:
                                            self.disable_all_items()
                                            await interaction.message.edit(f"<@{ctx.user.id}> won! This user won this match as well! Congratulations! 🏆<:bluex:1164986327167672361>\n\n{msgtext}", view=self)
                                            cur.execute(f"""DROP TABLE `{ctx.user.id}`""")
                                            cur.execute(f"""DROP TABLE `{opponentid}`""")
                                            conn.commit()
                                            anywin = False
                                            await interaction.response.defer()

                                        elif tttgame[3] == 2 and tttgame[4] == 2 and tttgame [5] == 2:
                                            self.disable_all_items()
                                            await interaction.message.edit(f"<@{ctx.user.id}> won! This user won this match as well! Congratulations! 🏆<:bluex:1164986327167672361>\n\n{msgtext}", view=self)
                                            cur.execute(f"""DROP TABLE `{ctx.user.id}`""")
                                            cur.execute(f"""DROP TABLE `{opponentid}`""")
                                            conn.commit()
                                            anywin = False
                                            await interaction.response.defer()

                                        elif tttgame[6] == 2 and tttgame[7] == 2 and tttgame [8] == 2:
                                            self.disable_all_items()
                                            await interaction.message.edit(f"<@{ctx.user.id}> won! This user won this match as well! Congratulations! 🏆<:bluex:1164986327167672361>\n\n{msgtext}", view=self)
                                            cur.execute(f"""DROP TABLE `{ctx.user.id}`""")
                                            cur.execute(f"""DROP TABLE `{opponentid}`""")
                                            conn.commit()
                                            anywin = False
                                            await interaction.response.defer()

                                        elif tttgame[0] == 2 and tttgame[4] == 2 and tttgame [8] == 2:
                                            self.disable_all_items()
                                            await interaction.message.edit(f"<@{ctx.user.id}> won! This user won this match as well! Congratulations! 🏆<:bluex:1164986327167672361>\n\n{msgtext}", view=self)
                                            cur.execute(f"""DROP TABLE `{ctx.user.id}`""")
                                            cur.execute(f"""DROP TABLE `{opponentid}`""")
                                            conn.commit()
                                            anywin = False
                                            await interaction.response.defer()

                                        elif tttgame[2] == 2 and tttgame[4] == 2 and tttgame [6] == 2:
                                            self.disable_all_items()
                                            await interaction.message.edit(f"<@{ctx.user.id}> won! This user won this match as well! Congratulations! 🏆<:bluex:1164986327167672361>\n\n{msgtext}", view=self)
                                            cur.execute(f"""DROP TABLE `{ctx.user.id}`""")
                                            cur.execute(f"""DROP TABLE `{opponentid}`""")
                                            conn.commit()
                                            anywin = False
                                            await interaction.response.defer()

                                    # BOT MOVES

                                    if anywin:
                                        tttbot1 = cur.execute(f"""SELECT tttbot FROM `{ctx.user.id}`""").fetchone()
                                        tttbot2 = sum(tttbot1)
                                        tttbot = int(tttbot2)

                                        if tttbot == 2:
                                            # Look for any possible wins...

                                            # 0
                                            # 3
                                            # 6

                                            if tttgame[0] == 3 and tttgame[6] == 3 and tttgame[3] == 1:
                                                tttgame[3] = 3
                                                tttgameint = f"{tttgame[0]}{tttgame[1]}{tttgame[2]}{tttgame[3]}{tttgame[4]}{tttgame[5]}{tttgame[6]}{tttgame[7]}{tttgame[8]}"
                                                tttgameint = int(tttgameint)
                                                cur.execute(f"""UPDATE `{ctx.user.id}` SET tttgame={tttgameint}""")
                                                cur.execute(f"""UPDATE `{ctx.user.id}` SET tttturn=2""")
                                                cur.execute(f"""UPDATE `{ctx.user.id}` SET tttbot=1""")
                                                conn.commit()
                                            elif tttgame[0] == 3 and tttgame[3] == 3 and tttgame[6] == 1:
                                                tttgame[6] = 3
                                                tttgameint = f"{tttgame[0]}{tttgame[1]}{tttgame[2]}{tttgame[3]}{tttgame[4]}{tttgame[5]}{tttgame[6]}{tttgame[7]}{tttgame[8]}"
                                                tttgameint = int(tttgameint)
                                                cur.execute(f"""UPDATE `{ctx.user.id}` SET tttgame={tttgameint}""")
                                                cur.execute(f"""UPDATE `{ctx.user.id}` SET tttturn=2""")
                                                cur.execute(f"""UPDATE `{ctx.user.id}` SET tttbot=1""")
                                                conn.commit()
                                            elif tttgame[6] == 3 and tttgame[3] == 3 and tttgame[0] == 1:
                                                tttgame[0] = 3
                                                tttgameint = f"{tttgame[0]}{tttgame[1]}{tttgame[2]}{tttgame[3]}{tttgame[4]}{tttgame[5]}{tttgame[6]}{tttgame[7]}{tttgame[8]}"
                                                tttgameint = int(tttgameint)
                                                cur.execute(f"""UPDATE `{ctx.user.id}` SET tttgame={tttgameint}""")
                                                cur.execute(f"""UPDATE `{ctx.user.id}` SET tttturn=2""")
                                                cur.execute(f"""UPDATE `{ctx.user.id}` SET tttbot=1""")
                                                conn.commit()

                                            # 1
                                            # 4
                                            # 7

                                            elif tttgame[1] == 3 and tttgame[4] == 3 and tttgame[7] == 1:
                                                tttgame[7] = 3
                                                tttgameint = f"{tttgame[0]}{tttgame[1]}{tttgame[2]}{tttgame[3]}{tttgame[4]}{tttgame[5]}{tttgame[6]}{tttgame[7]}{tttgame[8]}"
                                                tttgameint = int(tttgameint)
                                                cur.execute(f"""UPDATE `{ctx.user.id}` SET tttgame={tttgameint}""")
                                                cur.execute(f"""UPDATE `{ctx.user.id}` SET tttturn=2""")
                                                cur.execute(f"""UPDATE `{ctx.user.id}` SET tttbot=1""")
                                                conn.commit()
                                            elif tttgame[1] == 3 and tttgame[7] == 3 and tttgame[4] == 1:
                                                tttgame[4] = 3
                                                tttgameint = f"{tttgame[0]}{tttgame[1]}{tttgame[2]}{tttgame[3]}{tttgame[4]}{tttgame[5]}{tttgame[6]}{tttgame[7]}{tttgame[8]}"
                                                tttgameint = int(tttgameint)
                                                cur.execute(f"""UPDATE `{ctx.user.id}` SET tttgame={tttgameint}""")
                                                cur.execute(f"""UPDATE `{ctx.user.id}` SET tttturn=2""")
                                                cur.execute(f"""UPDATE `{ctx.user.id}` SET tttbot=1""")
                                                conn.commit()
                                            elif tttgame[4] == 3 and tttgame[7] == 3 and tttgame[1] == 1:
                                                tttgame[1] = 3
                                                tttgameint = f"{tttgame[0]}{tttgame[1]}{tttgame[2]}{tttgame[3]}{tttgame[4]}{tttgame[5]}{tttgame[6]}{tttgame[7]}{tttgame[8]}"
                                                tttgameint = int(tttgameint)
                                                cur.execute(f"""UPDATE `{ctx.user.id}` SET tttgame={tttgameint}""")
                                                cur.execute(f"""UPDATE `{ctx.user.id}` SET tttturn=2""")
                                                cur.execute(f"""UPDATE `{ctx.user.id}` SET tttbot=1""")
                                                conn.commit()

                                            # 2
                                            # 5
                                            # 8

                                            elif tttgame[2] == 3 and tttgame[5] == 3 and tttgame[8] == 1:
                                                tttgame[8] = 3
                                                tttgameint = f"{tttgame[0]}{tttgame[1]}{tttgame[2]}{tttgame[3]}{tttgame[4]}{tttgame[5]}{tttgame[6]}{tttgame[7]}{tttgame[8]}"
                                                tttgameint = int(tttgameint)
                                                cur.execute(f"""UPDATE `{ctx.user.id}` SET tttgame={tttgameint}""")
                                                cur.execute(f"""UPDATE `{ctx.user.id}` SET tttturn=2""")
                                                cur.execute(f"""UPDATE `{ctx.user.id}` SET tttbot=1""")
                                                conn.commit()
                                            elif tttgame[2] == 3 and tttgame[8] == 3 and tttgame[5] == 1:
                                                tttgame[5] = 3
                                                tttgameint = f"{tttgame[0]}{tttgame[1]}{tttgame[2]}{tttgame[3]}{tttgame[4]}{tttgame[5]}{tttgame[6]}{tttgame[7]}{tttgame[8]}"
                                                tttgameint = int(tttgameint)
                                                cur.execute(f"""UPDATE `{ctx.user.id}` SET tttgame={tttgameint}""")
                                                cur.execute(f"""UPDATE `{ctx.user.id}` SET tttturn=2""")
                                                cur.execute(f"""UPDATE `{ctx.user.id}` SET tttbot=1""")
                                                conn.commit()
                                            elif tttgame[8] == 3 and tttgame[5] == 3 and tttgame[2] == 1:
                                                tttgame[2] = 3
                                                tttgameint = f"{tttgame[0]}{tttgame[1]}{tttgame[2]}{tttgame[3]}{tttgame[4]}{tttgame[5]}{tttgame[6]}{tttgame[7]}{tttgame[8]}"
                                                tttgameint = int(tttgameint)
                                                cur.execute(f"""UPDATE `{ctx.user.id}` SET tttgame={tttgameint}""")
                                                cur.execute(f"""UPDATE `{ctx.user.id}` SET tttturn=2""")
                                                cur.execute(f"""UPDATE `{ctx.user.id}` SET tttbot=1""")
                                                conn.commit()

                                            # 0 1 2

                                            elif tttgame[0] == 3 and tttgame[1] == 3 and tttgame[2] == 1:
                                                tttgame[2] = 3
                                                tttgameint = f"{tttgame[0]}{tttgame[1]}{tttgame[2]}{tttgame[3]}{tttgame[4]}{tttgame[5]}{tttgame[6]}{tttgame[7]}{tttgame[8]}"
                                                tttgameint = int(tttgameint)
                                                cur.execute(f"""UPDATE `{ctx.user.id}` SET tttgame={tttgameint}""")
                                                cur.execute(f"""UPDATE `{ctx.user.id}` SET tttturn=2""")
                                                cur.execute(f"""UPDATE `{ctx.user.id}` SET tttbot=1""")
                                                conn.commit()
                                            elif tttgame[0] == 3 and tttgame[2] == 3 and tttgame[1] == 1:
                                                tttgame[1] = 3
                                                tttgameint = f"{tttgame[0]}{tttgame[1]}{tttgame[2]}{tttgame[3]}{tttgame[4]}{tttgame[5]}{tttgame[6]}{tttgame[7]}{tttgame[8]}"
                                                tttgameint = int(tttgameint)
                                                cur.execute(f"""UPDATE `{ctx.user.id}` SET tttgame={tttgameint}""")
                                                cur.execute(f"""UPDATE `{ctx.user.id}` SET tttturn=2""")
                                                cur.execute(f"""UPDATE `{ctx.user.id}` SET tttbot=1""")
                                                conn.commit()
                                            elif tttgame[2] == 3 and tttgame[1] == 3 and tttgame[0] == 1:
                                                tttgame[0] = 3
                                                tttgameint = f"{tttgame[0]}{tttgame[1]}{tttgame[2]}{tttgame[3]}{tttgame[4]}{tttgame[5]}{tttgame[6]}{tttgame[7]}{tttgame[8]}"
                                                tttgameint = int(tttgameint)
                                                cur.execute(f"""UPDATE `{ctx.user.id}` SET tttgame={tttgameint}""")
                                                cur.execute(f"""UPDATE `{ctx.user.id}` SET tttturn=2""")
                                                cur.execute(f"""UPDATE `{ctx.user.id}` SET tttbot=1""")
                                                conn.commit()

                                            # 3 4 5

                                            elif tttgame[3] == 3 and tttgame[4] == 3 and tttgame[5] == 1:
                                                tttgame[5] = 3
                                                tttgameint = f"{tttgame[0]}{tttgame[1]}{tttgame[2]}{tttgame[3]}{tttgame[4]}{tttgame[5]}{tttgame[6]}{tttgame[7]}{tttgame[8]}"
                                                tttgameint = int(tttgameint)
                                                cur.execute(f"""UPDATE `{ctx.user.id}` SET tttgame={tttgameint}""")
                                                cur.execute(f"""UPDATE `{ctx.user.id}` SET tttturn=2""")
                                                cur.execute(f"""UPDATE `{ctx.user.id}` SET tttbot=1""")
                                                conn.commit()
                                            elif tttgame[3] == 3 and tttgame[5] == 3 and tttgame[4] == 1:
                                                tttgame[4] = 3
                                                tttgameint = f"{tttgame[0]}{tttgame[1]}{tttgame[2]}{tttgame[3]}{tttgame[4]}{tttgame[5]}{tttgame[6]}{tttgame[7]}{tttgame[8]}"
                                                tttgameint = int(tttgameint)
                                                cur.execute(f"""UPDATE `{ctx.user.id}` SET tttgame={tttgameint}""")
                                                cur.execute(f"""UPDATE `{ctx.user.id}` SET tttturn=2""")
                                                cur.execute(f"""UPDATE `{ctx.user.id}` SET tttbot=1""")
                                                conn.commit()
                                            elif tttgame[4] == 3 and tttgame[5] == 3 and tttgame[3] == 1:
                                                tttgame[3] = 3
                                                tttgameint = f"{tttgame[0]}{tttgame[1]}{tttgame[2]}{tttgame[3]}{tttgame[4]}{tttgame[5]}{tttgame[6]}{tttgame[7]}{tttgame[8]}"
                                                tttgameint = int(tttgameint)
                                                cur.execute(f"""UPDATE `{ctx.user.id}` SET tttgame={tttgameint}""")
                                                cur.execute(f"""UPDATE `{ctx.user.id}` SET tttturn=2""")
                                                cur.execute(f"""UPDATE `{ctx.user.id}` SET tttbot=1""")
                                                conn.commit()

                                            # 6 7 8

                                            elif tttgame[6] == 3 and tttgame[7] == 3 and tttgame[8] == 1:
                                                tttgame[8] = 3
                                                tttgameint = f"{tttgame[0]}{tttgame[1]}{tttgame[2]}{tttgame[3]}{tttgame[4]}{tttgame[5]}{tttgame[6]}{tttgame[7]}{tttgame[8]}"
                                                tttgameint = int(tttgameint)
                                                cur.execute(f"""UPDATE `{ctx.user.id}` SET tttgame={tttgameint}""")
                                                cur.execute(f"""UPDATE `{ctx.user.id}` SET tttturn=2""")
                                                cur.execute(f"""UPDATE `{ctx.user.id}` SET tttbot=1""")
                                                conn.commit()
                                            elif tttgame[6] == 3 and tttgame[8] == 3 and tttgame[7] == 1:
                                                tttgame[7] = 3
                                                tttgameint = f"{tttgame[0]}{tttgame[1]}{tttgame[2]}{tttgame[3]}{tttgame[4]}{tttgame[5]}{tttgame[6]}{tttgame[7]}{tttgame[8]}"
                                                tttgameint = int(tttgameint)
                                                cur.execute(f"""UPDATE `{ctx.user.id}` SET tttgame={tttgameint}""")
                                                cur.execute(f"""UPDATE `{ctx.user.id}` SET tttturn=2""")
                                                cur.execute(f"""UPDATE `{ctx.user.id}` SET tttbot=1""")
                                                conn.commit()
                                            elif tttgame[7] == 3 and tttgame[8] == 3 and tttgame[6] == 1:
                                                tttgame[6] = 3
                                                tttgameint = f"{tttgame[0]}{tttgame[1]}{tttgame[2]}{tttgame[3]}{tttgame[4]}{tttgame[5]}{tttgame[6]}{tttgame[7]}{tttgame[8]}"
                                                tttgameint = int(tttgameint)
                                                cur.execute(f"""UPDATE `{ctx.user.id}` SET tttgame={tttgameint}""")
                                                cur.execute(f"""UPDATE `{ctx.user.id}` SET tttturn=2""")
                                                cur.execute(f"""UPDATE `{ctx.user.id}` SET tttbot=1""")
                                                conn.commit()

                                            # 0
                                            #   4
                                            #     8

                                            elif tttgame[0] == 3 and tttgame[4] == 3 and tttgame[8] == 1:
                                                tttgame[8] = 3
                                                tttgameint = f"{tttgame[0]}{tttgame[1]}{tttgame[2]}{tttgame[3]}{tttgame[4]}{tttgame[5]}{tttgame[6]}{tttgame[7]}{tttgame[8]}"
                                                tttgameint = int(tttgameint)
                                                cur.execute(f"""UPDATE `{ctx.user.id}` SET tttgame={tttgameint}""")
                                                cur.execute(f"""UPDATE `{ctx.user.id}` SET tttturn=2""")
                                                cur.execute(f"""UPDATE `{ctx.user.id}` SET tttbot=1""")
                                                conn.commit()
                                            elif tttgame[0] == 3 and tttgame[8] == 3 and tttgame[4] == 1:
                                                tttgame[4] = 3
                                                tttgameint = f"{tttgame[0]}{tttgame[1]}{tttgame[2]}{tttgame[3]}{tttgame[4]}{tttgame[5]}{tttgame[6]}{tttgame[7]}{tttgame[8]}"
                                                tttgameint = int(tttgameint)
                                                cur.execute(f"""UPDATE `{ctx.user.id}` SET tttgame={tttgameint}""")
                                                cur.execute(f"""UPDATE `{ctx.user.id}` SET tttturn=2""")
                                                cur.execute(f"""UPDATE `{ctx.user.id}` SET tttbot=1""")
                                                conn.commit()
                                            elif tttgame[4] == 3 and tttgame[8] == 3 and tttgame[0] == 1:
                                                tttgame[0] = 3
                                                tttgameint = f"{tttgame[0]}{tttgame[1]}{tttgame[2]}{tttgame[3]}{tttgame[4]}{tttgame[5]}{tttgame[6]}{tttgame[7]}{tttgame[8]}"
                                                tttgameint = int(tttgameint)
                                                cur.execute(f"""UPDATE `{ctx.user.id}` SET tttgame={tttgameint}""")
                                                cur.execute(f"""UPDATE `{ctx.user.id}` SET tttturn=2""")
                                                cur.execute(f"""UPDATE `{ctx.user.id}` SET tttbot=1""")
                                                conn.commit()

                                            #     2
                                            #   4
                                            # 6

                                            elif tttgame[2] == 3 and tttgame[4] == 3 and tttgame[6] == 1:
                                                tttgame[6] = 3
                                                tttgameint = f"{tttgame[0]}{tttgame[1]}{tttgame[2]}{tttgame[3]}{tttgame[4]}{tttgame[5]}{tttgame[6]}{tttgame[7]}{tttgame[8]}"
                                                tttgameint = int(tttgameint)
                                                cur.execute(f"""UPDATE `{ctx.user.id}` SET tttgame={tttgameint}""")
                                                cur.execute(f"""UPDATE `{ctx.user.id}` SET tttturn=2""")
                                                cur.execute(f"""UPDATE `{ctx.user.id}` SET tttbot=1""")
                                                conn.commit()
                                            elif tttgame[2] == 3 and tttgame[6] == 3 and tttgame[4] == 1:
                                                tttgame[4] = 3
                                                tttgameint = f"{tttgame[0]}{tttgame[1]}{tttgame[2]}{tttgame[3]}{tttgame[4]}{tttgame[5]}{tttgame[6]}{tttgame[7]}{tttgame[8]}"
                                                tttgameint = int(tttgameint)
                                                cur.execute(f"""UPDATE `{ctx.user.id}` SET tttgame={tttgameint}""")
                                                cur.execute(f"""UPDATE `{ctx.user.id}` SET tttturn=2""")
                                                cur.execute(f"""UPDATE `{ctx.user.id}` SET tttbot=1""")
                                                conn.commit()
                                            elif tttgame[4] == 3 and tttgame[6] == 3 and tttgame[2] == 1:
                                                tttgame[2] = 3
                                                tttgameint = f"{tttgame[0]}{tttgame[1]}{tttgame[2]}{tttgame[3]}{tttgame[4]}{tttgame[5]}{tttgame[6]}{tttgame[7]}{tttgame[8]}"
                                                tttgameint = int(tttgameint)
                                                cur.execute(f"""UPDATE `{ctx.user.id}` SET tttgame={tttgameint}""")
                                                cur.execute(f"""UPDATE `{ctx.user.id}` SET tttturn=2""")
                                                cur.execute(f"""UPDATE `{ctx.user.id}` SET tttbot=1""")
                                                conn.commit()

                                            # Defend system

                                            # 0
                                            # 3
                                            # 6

                                            elif tttgame[0] == 2 and tttgame[6] == 2 and tttgame[3] == 1:
                                                tttgame[3] = 3
                                                tttgameint = f"{tttgame[0]}{tttgame[1]}{tttgame[2]}{tttgame[3]}{tttgame[4]}{tttgame[5]}{tttgame[6]}{tttgame[7]}{tttgame[8]}"
                                                tttgameint = int(tttgameint)
                                                cur.execute(f"""UPDATE `{ctx.user.id}` SET tttgame={tttgameint}""")
                                                cur.execute(f"""UPDATE `{ctx.user.id}` SET tttturn=2""")
                                                cur.execute(f"""UPDATE `{ctx.user.id}` SET tttbot=1""")
                                                conn.commit()
                                            elif tttgame[0] == 2 and tttgame[3] == 2 and tttgame[6] == 1:
                                                tttgame[6] = 3
                                                tttgameint = f"{tttgame[0]}{tttgame[1]}{tttgame[2]}{tttgame[3]}{tttgame[4]}{tttgame[5]}{tttgame[6]}{tttgame[7]}{tttgame[8]}"
                                                tttgameint = int(tttgameint)
                                                cur.execute(f"""UPDATE `{ctx.user.id}` SET tttgame={tttgameint}""")
                                                cur.execute(f"""UPDATE `{ctx.user.id}` SET tttturn=2""")
                                                cur.execute(f"""UPDATE `{ctx.user.id}` SET tttbot=1""")
                                                conn.commit()
                                            elif tttgame[6] == 2 and tttgame[3] == 2 and tttgame[0] == 1:
                                                tttgame[0] = 3
                                                tttgameint = f"{tttgame[0]}{tttgame[1]}{tttgame[2]}{tttgame[3]}{tttgame[4]}{tttgame[5]}{tttgame[6]}{tttgame[7]}{tttgame[8]}"
                                                tttgameint = int(tttgameint)
                                                cur.execute(f"""UPDATE `{ctx.user.id}` SET tttgame={tttgameint}""")
                                                cur.execute(f"""UPDATE `{ctx.user.id}` SET tttturn=2""")
                                                cur.execute(f"""UPDATE `{ctx.user.id}` SET tttbot=1""")
                                                conn.commit()

                                            # 1
                                            # 4
                                            # 7

                                            elif tttgame[1] == 2 and tttgame[4] == 2 and tttgame[7] == 1:
                                                tttgame[7] = 3
                                                tttgameint = f"{tttgame[0]}{tttgame[1]}{tttgame[2]}{tttgame[3]}{tttgame[4]}{tttgame[5]}{tttgame[6]}{tttgame[7]}{tttgame[8]}"
                                                tttgameint = int(tttgameint)
                                                cur.execute(f"""UPDATE `{ctx.user.id}` SET tttgame={tttgameint}""")
                                                cur.execute(f"""UPDATE `{ctx.user.id}` SET tttturn=2""")
                                                cur.execute(f"""UPDATE `{ctx.user.id}` SET tttbot=1""")
                                                conn.commit()
                                            elif tttgame[1] == 2 and tttgame[7] == 2 and tttgame[4] == 1:
                                                tttgame[4] = 3
                                                tttgameint = f"{tttgame[0]}{tttgame[1]}{tttgame[2]}{tttgame[3]}{tttgame[4]}{tttgame[5]}{tttgame[6]}{tttgame[7]}{tttgame[8]}"
                                                tttgameint = int(tttgameint)
                                                cur.execute(f"""UPDATE `{ctx.user.id}` SET tttgame={tttgameint}""")
                                                cur.execute(f"""UPDATE `{ctx.user.id}` SET tttturn=2""")
                                                cur.execute(f"""UPDATE `{ctx.user.id}` SET tttbot=1""")
                                                conn.commit()
                                            elif tttgame[4] == 2 and tttgame[7] == 2 and tttgame[1] == 1:
                                                tttgame[1] = 3
                                                tttgameint = f"{tttgame[0]}{tttgame[1]}{tttgame[2]}{tttgame[3]}{tttgame[4]}{tttgame[5]}{tttgame[6]}{tttgame[7]}{tttgame[8]}"
                                                tttgameint = int(tttgameint)
                                                cur.execute(f"""UPDATE `{ctx.user.id}` SET tttgame={tttgameint}""")
                                                cur.execute(f"""UPDATE `{ctx.user.id}` SET tttturn=2""")
                                                cur.execute(f"""UPDATE `{ctx.user.id}` SET tttbot=1""")
                                                conn.commit()

                                            # 2
                                            # 5
                                            # 8

                                            elif tttgame[2] == 2 and tttgame[5] == 2 and tttgame[8] == 1:
                                                tttgame[8] = 3
                                                tttgameint = f"{tttgame[0]}{tttgame[1]}{tttgame[2]}{tttgame[3]}{tttgame[4]}{tttgame[5]}{tttgame[6]}{tttgame[7]}{tttgame[8]}"
                                                tttgameint = int(tttgameint)
                                                cur.execute(f"""UPDATE `{ctx.user.id}` SET tttgame={tttgameint}""")
                                                cur.execute(f"""UPDATE `{ctx.user.id}` SET tttturn=2""")
                                                cur.execute(f"""UPDATE `{ctx.user.id}` SET tttbot=1""")
                                                conn.commit()
                                            elif tttgame[2] == 2 and tttgame[8] == 2 and tttgame[5] == 1:
                                                tttgame[5] = 3
                                                tttgameint = f"{tttgame[0]}{tttgame[1]}{tttgame[2]}{tttgame[3]}{tttgame[4]}{tttgame[5]}{tttgame[6]}{tttgame[7]}{tttgame[8]}"
                                                tttgameint = int(tttgameint)
                                                cur.execute(f"""UPDATE `{ctx.user.id}` SET tttgame={tttgameint}""")
                                                cur.execute(f"""UPDATE `{ctx.user.id}` SET tttturn=2""")
                                                cur.execute(f"""UPDATE `{ctx.user.id}` SET tttbot=1""")
                                                conn.commit()
                                            elif tttgame[8] == 2 and tttgame[5] == 2 and tttgame[2] == 1:
                                                tttgame[2] = 3
                                                tttgameint = f"{tttgame[0]}{tttgame[1]}{tttgame[2]}{tttgame[3]}{tttgame[4]}{tttgame[5]}{tttgame[6]}{tttgame[7]}{tttgame[8]}"
                                                tttgameint = int(tttgameint)
                                                cur.execute(f"""UPDATE `{ctx.user.id}` SET tttgame={tttgameint}""")
                                                cur.execute(f"""UPDATE `{ctx.user.id}` SET tttturn=2""")
                                                cur.execute(f"""UPDATE `{ctx.user.id}` SET tttbot=1""")
                                                conn.commit()

                                            # 0 1 2

                                            elif tttgame[0] == 2 and tttgame[1] == 2 and tttgame[2] == 1:
                                                tttgame[2] = 3
                                                tttgameint = f"{tttgame[0]}{tttgame[1]}{tttgame[2]}{tttgame[3]}{tttgame[4]}{tttgame[5]}{tttgame[6]}{tttgame[7]}{tttgame[8]}"
                                                tttgameint = int(tttgameint)
                                                cur.execute(f"""UPDATE `{ctx.user.id}` SET tttgame={tttgameint}""")
                                                cur.execute(f"""UPDATE `{ctx.user.id}` SET tttturn=2""")
                                                cur.execute(f"""UPDATE `{ctx.user.id}` SET tttbot=1""")
                                                conn.commit()
                                            elif tttgame[0] == 2 and tttgame[2] == 2 and tttgame[1] == 1:
                                                tttgame[1] = 3
                                                tttgameint = f"{tttgame[0]}{tttgame[1]}{tttgame[2]}{tttgame[3]}{tttgame[4]}{tttgame[5]}{tttgame[6]}{tttgame[7]}{tttgame[8]}"
                                                tttgameint = int(tttgameint)
                                                cur.execute(f"""UPDATE `{ctx.user.id}` SET tttgame={tttgameint}""")
                                                cur.execute(f"""UPDATE `{ctx.user.id}` SET tttturn=2""")
                                                cur.execute(f"""UPDATE `{ctx.user.id}` SET tttbot=1""")
                                                conn.commit()
                                            elif tttgame[2] == 2 and tttgame[1] == 2 and tttgame[0] == 1:
                                                tttgame[0] = 3
                                                tttgameint = f"{tttgame[0]}{tttgame[1]}{tttgame[2]}{tttgame[3]}{tttgame[4]}{tttgame[5]}{tttgame[6]}{tttgame[7]}{tttgame[8]}"
                                                tttgameint = int(tttgameint)
                                                cur.execute(f"""UPDATE `{ctx.user.id}` SET tttgame={tttgameint}""")
                                                cur.execute(f"""UPDATE `{ctx.user.id}` SET tttturn=2""")
                                                cur.execute(f"""UPDATE `{ctx.user.id}` SET tttbot=1""")
                                                conn.commit()

                                            # 3 4 5

                                            elif tttgame[3] == 2 and tttgame[4] == 2 and tttgame[5] == 1:
                                                tttgame[5] = 3
                                                tttgameint = f"{tttgame[0]}{tttgame[1]}{tttgame[2]}{tttgame[3]}{tttgame[4]}{tttgame[5]}{tttgame[6]}{tttgame[7]}{tttgame[8]}"
                                                tttgameint = int(tttgameint)
                                                cur.execute(f"""UPDATE `{ctx.user.id}` SET tttgame={tttgameint}""")
                                                cur.execute(f"""UPDATE `{ctx.user.id}` SET tttturn=2""")
                                                cur.execute(f"""UPDATE `{ctx.user.id}` SET tttbot=1""")
                                                conn.commit()
                                            elif tttgame[3] == 2 and tttgame[5] == 2 and tttgame[4] == 1:
                                                tttgame[4] = 3
                                                tttgameint = f"{tttgame[0]}{tttgame[1]}{tttgame[2]}{tttgame[3]}{tttgame[4]}{tttgame[5]}{tttgame[6]}{tttgame[7]}{tttgame[8]}"
                                                tttgameint = int(tttgameint)
                                                cur.execute(f"""UPDATE `{ctx.user.id}` SET tttgame={tttgameint}""")
                                                cur.execute(f"""UPDATE `{ctx.user.id}` SET tttturn=2""")
                                                cur.execute(f"""UPDATE `{ctx.user.id}` SET tttbot=1""")
                                                conn.commit()
                                            elif tttgame[4] == 2 and tttgame[5] == 2 and tttgame[3] == 1:
                                                tttgame[3] = 3
                                                tttgameint = f"{tttgame[0]}{tttgame[1]}{tttgame[2]}{tttgame[3]}{tttgame[4]}{tttgame[5]}{tttgame[6]}{tttgame[7]}{tttgame[8]}"
                                                tttgameint = int(tttgameint)
                                                cur.execute(f"""UPDATE `{ctx.user.id}` SET tttgame={tttgameint}""")
                                                cur.execute(f"""UPDATE `{ctx.user.id}` SET tttturn=2""")
                                                cur.execute(f"""UPDATE `{ctx.user.id}` SET tttbot=1""")
                                                conn.commit()

                                            # 6 7 8

                                            elif tttgame[6] == 2 and tttgame[7] == 2 and tttgame[8] == 1:
                                                tttgame[8] = 3
                                                tttgameint = f"{tttgame[0]}{tttgame[1]}{tttgame[2]}{tttgame[3]}{tttgame[4]}{tttgame[5]}{tttgame[6]}{tttgame[7]}{tttgame[8]}"
                                                tttgameint = int(tttgameint)
                                                cur.execute(f"""UPDATE `{ctx.user.id}` SET tttgame={tttgameint}""")
                                                cur.execute(f"""UPDATE `{ctx.user.id}` SET tttturn=2""")
                                                cur.execute(f"""UPDATE `{ctx.user.id}` SET tttbot=1""")
                                                conn.commit()
                                            elif tttgame[6] == 2 and tttgame[8] == 2 and tttgame[7] == 1:
                                                tttgame[7] = 3
                                                tttgameint = f"{tttgame[0]}{tttgame[1]}{tttgame[2]}{tttgame[3]}{tttgame[4]}{tttgame[5]}{tttgame[6]}{tttgame[7]}{tttgame[8]}"
                                                tttgameint = int(tttgameint)
                                                cur.execute(f"""UPDATE `{ctx.user.id}` SET tttgame={tttgameint}""")
                                                cur.execute(f"""UPDATE `{ctx.user.id}` SET tttturn=2""")
                                                cur.execute(f"""UPDATE `{ctx.user.id}` SET tttbot=1""")
                                                conn.commit()
                                            elif tttgame[7] == 2 and tttgame[8] == 2 and tttgame[6] == 1:
                                                tttgame[6] = 3
                                                tttgameint = f"{tttgame[0]}{tttgame[1]}{tttgame[2]}{tttgame[3]}{tttgame[4]}{tttgame[5]}{tttgame[6]}{tttgame[7]}{tttgame[8]}"
                                                tttgameint = int(tttgameint)
                                                cur.execute(f"""UPDATE `{ctx.user.id}` SET tttgame={tttgameint}""")
                                                cur.execute(f"""UPDATE `{ctx.user.id}` SET tttturn=2""")
                                                cur.execute(f"""UPDATE `{ctx.user.id}` SET tttbot=1""")
                                                conn.commit()

                                            # 0
                                            #   4
                                            #     8

                                            elif tttgame[0] == 2 and tttgame[4] == 2 and tttgame[8] == 1:
                                                tttgame[8] = 3
                                                tttgameint = f"{tttgame[0]}{tttgame[1]}{tttgame[2]}{tttgame[3]}{tttgame[4]}{tttgame[5]}{tttgame[6]}{tttgame[7]}{tttgame[8]}"
                                                tttgameint = int(tttgameint)
                                                cur.execute(f"""UPDATE `{ctx.user.id}` SET tttgame={tttgameint}""")
                                                cur.execute(f"""UPDATE `{ctx.user.id}` SET tttturn=2""")
                                                cur.execute(f"""UPDATE `{ctx.user.id}` SET tttbot=1""")
                                                conn.commit()
                                            elif tttgame[0] == 2 and tttgame[8] == 2 and tttgame[4] == 1:
                                                tttgame[4] = 3
                                                tttgameint = f"{tttgame[0]}{tttgame[1]}{tttgame[2]}{tttgame[3]}{tttgame[4]}{tttgame[5]}{tttgame[6]}{tttgame[7]}{tttgame[8]}"
                                                tttgameint = int(tttgameint)
                                                cur.execute(f"""UPDATE `{ctx.user.id}` SET tttgame={tttgameint}""")
                                                cur.execute(f"""UPDATE `{ctx.user.id}` SET tttturn=2""")
                                                cur.execute(f"""UPDATE `{ctx.user.id}` SET tttbot=1""")
                                                conn.commit()
                                            elif tttgame[4] == 2 and tttgame[8] == 2 and tttgame[0] == 1:
                                                tttgame[0] = 3
                                                tttgameint = f"{tttgame[0]}{tttgame[1]}{tttgame[2]}{tttgame[3]}{tttgame[4]}{tttgame[5]}{tttgame[6]}{tttgame[7]}{tttgame[8]}"
                                                tttgameint = int(tttgameint)
                                                cur.execute(f"""UPDATE `{ctx.user.id}` SET tttgame={tttgameint}""")
                                                cur.execute(f"""UPDATE `{ctx.user.id}` SET tttturn=2""")
                                                cur.execute(f"""UPDATE `{ctx.user.id}` SET tttbot=1""")
                                                conn.commit()

                                            #     2
                                            #   4
                                            # 6

                                            elif tttgame[2] == 2 and tttgame[4] == 2 and tttgame[6] == 1:
                                                tttgame[6] = 3
                                                tttgameint = f"{tttgame[0]}{tttgame[1]}{tttgame[2]}{tttgame[3]}{tttgame[4]}{tttgame[5]}{tttgame[6]}{tttgame[7]}{tttgame[8]}"
                                                tttgameint = int(tttgameint)
                                                cur.execute(f"""UPDATE `{ctx.user.id}` SET tttgame={tttgameint}""")
                                                cur.execute(f"""UPDATE `{ctx.user.id}` SET tttturn=2""")
                                                cur.execute(f"""UPDATE `{ctx.user.id}` SET tttbot=1""")
                                                conn.commit()
                                            elif tttgame[2] == 2 and tttgame[6] == 2 and tttgame[4] == 1:
                                                tttgame[4] = 3
                                                tttgameint = f"{tttgame[0]}{tttgame[1]}{tttgame[2]}{tttgame[3]}{tttgame[4]}{tttgame[5]}{tttgame[6]}{tttgame[7]}{tttgame[8]}"
                                                tttgameint = int(tttgameint)
                                                cur.execute(f"""UPDATE `{ctx.user.id}` SET tttgame={tttgameint}""")
                                                cur.execute(f"""UPDATE `{ctx.user.id}` SET tttturn=2""")
                                                cur.execute(f"""UPDATE `{ctx.user.id}` SET tttbot=1""")
                                                conn.commit()
                                            elif tttgame[4] == 2 and tttgame[6] == 2 and tttgame[2] == 1:
                                                tttgame[2] = 3
                                                tttgameint = f"{tttgame[0]}{tttgame[1]}{tttgame[2]}{tttgame[3]}{tttgame[4]}{tttgame[5]}{tttgame[6]}{tttgame[7]}{tttgame[8]}"
                                                tttgameint = int(tttgameint)
                                                cur.execute(f"""UPDATE `{ctx.user.id}` SET tttgame={tttgameint}""")
                                                cur.execute(f"""UPDATE `{ctx.user.id}` SET tttturn=2""")
                                                cur.execute(f"""UPDATE `{ctx.user.id}` SET tttbot=1""")
                                                conn.commit()

                                            # If there is nothing to do and there are some empty place(s), pick a random empty field...
                                            elif 1 in tttgame:
                                                while True:
                                                    i = random.randint(0,8)
                                                    if tttgame[i] == 1:
                                                        tttgame[i] = 3
                                                        tttgameint = f"{tttgame[0]}{tttgame[1]}{tttgame[2]}{tttgame[3]}{tttgame[4]}{tttgame[5]}{tttgame[6]}{tttgame[7]}{tttgame[8]}"
                                                        tttgameint = int(tttgameint)
                                                        cur.execute(f"""UPDATE `{ctx.user.id}` SET tttgame={tttgameint}""")
                                                        cur.execute(f"""UPDATE `{ctx.user.id}` SET tttturn=2""")
                                                        cur.execute(f"""UPDATE `{ctx.user.id}` SET tttbot=1""")
                                                        conn.commit()
                                                        break

                                        if tttgame[0] == 1:
                                            one1 = "<:one1:1164986232841982003>"

                                        elif tttgame[0] == 2:
                                            one1 = "<:bluex:1164986327167672361>"
                                        
                                        else:
                                            one1 = "<:redo:1164986221118902362>"

                                        if tttgame[1] == 1:
                                            two2 = "<:two2:1164986146539970632>"

                                        elif tttgame[1] == 2:
                                            two2 = "<:bluex:1164986327167672361>"
                                        
                                        else:
                                            two2 = "<:redo:1164986221118902362>"

                                        if tttgame[2] == 1:
                                            three3 = "<:three3:1164986176487305356>"

                                        elif tttgame[2] == 2:
                                            three3 = "<:bluex:1164986327167672361>"
                                        
                                        else:
                                            three3 = "<:redo:1164986221118902362>"

                                        if tttgame[3] == 1:
                                            four4 = "<:four4:1164986285715365909>"

                                        elif tttgame[3] == 2:
                                            four4 = "<:bluex:1164986327167672361>"
                                        
                                        else:
                                            four4 = "<:redo:1164986221118902362>"

                                        if tttgame[4] == 1:
                                            five5 = "<:five5:1164986312667967608>"

                                        elif tttgame[4] == 2:
                                            five5 = "<:bluex:1164986327167672361>"
                                        
                                        else:
                                            five5 = "<:redo:1164986221118902362>"

                                        if tttgame[5] == 1:
                                            six6 = "<:six6:1164986175312896081>"

                                        elif tttgame[5] == 2:
                                            six6 = "<:bluex:1164986327167672361>"
                                        
                                        else:
                                            six6 = "<:redo:1164986221118902362>"

                                        if tttgame[6] == 1:
                                            seven7 = "<:seven7:1164986188873072660>"

                                        elif tttgame[6] == 2:
                                            seven7 = "<:bluex:1164986327167672361>"
                                        
                                        else:
                                            seven7 = "<:redo:1164986221118902362>"

                                        if tttgame[7] == 1:
                                            eight8 = "<:eight8:1164986320922361856>"

                                        elif tttgame[7] == 2:
                                            eight8 = "<:bluex:1164986327167672361>"
                                        
                                        else:
                                            eight8 = "<:redo:1164986221118902362>"

                                        if tttgame[8] == 1:
                                            nine9 = "<:nine9:1164986246884499569>"

                                        elif tttgame[8] == 2:
                                            nine9 = "<:bluex:1164986327167672361>"
                                        
                                        else:
                                            nine9 = "<:redo:1164986221118902362>"

                                        msgtext = f"{one1}<:whitelinevertical:1164986150113513624>{two2}<:whitelinevertical:1164986150113513624>{three3}\n<:whitelinehorizontal:1164986148205109308><:whiteplus:1164986151849959495><:whitelinehorizontal:1164986148205109308><:whiteplus:1164986151849959495><:whitelinehorizontal:1164986148205109308>\n{four4}<:whitelinevertical:1164986150113513624>{five5}<:whitelinevertical:1164986150113513624>{six6}\n<:whitelinehorizontal:1164986148205109308><:whiteplus:1164986151849959495><:whitelinehorizontal:1164986148205109308><:whiteplus:1164986151849959495><:whitelinehorizontal:1164986148205109308>\n{seven7}<:whitelinevertical:1164986150113513624>{eight8}<:whitelinevertical:1164986150113513624>{nine9}"
                                        
                                    # 0 1 2
                                    # 3 4 5
                                    # 6 7 8

                                    if tttbot == 3 and anywin:
                                        if tttgame[0] == 3 and tttgame[3] == 3 and tttgame [6] == 3:
                                            self.disable_all_items()
                                            await interaction.message.edit(f"<@{opponentid}> won and it's this user's turn to ping a ball! 🏓<:redo:1164986221118902362>\n\n{msgtext}", view=self)
                                            cur.execute(f"""UPDATE `{ctx.user.id}` SET tttgame=111111111""")
                                            cur.execute(f"""UPDATE `{ctx.user.id}` SET tttturn=0""")
                                            cur.execute(f"""UPDATE `{opponentid}` SET tttgame=111111111""")
                                            cur.execute(f"""UPDATE `{opponentid}` SET tttturn=0""")
                                            cur.execute(f"""UPDATE `{ctx.user.id}` SET turn=0""")
                                            cur.execute(f"""UPDATE `{opponentid}` SET turn=1""")
                                            upd1 = cur2.execute(f"""SELECT ballspinged FROM main""").fetchone()
                                            upd2 = sum(upd1)
                                            upd = int(upd2)
                                            upd += 1
                                            cur2.execute(f"""UPDATE main SET ballspinged={upd}""")
                                            conn.commit()
                                            conn.close()
                                            conn2.close()

                                        elif tttgame[1] == 3 and tttgame[4] == 3 and tttgame [7] == 3:
                                            self.disable_all_items()
                                            await interaction.message.edit(f"<@{opponentid}> won and it's this user's turn to ping a ball! 🏓<:redo:1164986221118902362>\n\n{msgtext}", view=self)
                                            cur.execute(f"""UPDATE `{ctx.user.id}` SET tttgame=111111111""")
                                            cur.execute(f"""UPDATE `{ctx.user.id}` SET tttturn=0""")
                                            cur.execute(f"""UPDATE `{opponentid}` SET tttgame=111111111""")
                                            cur.execute(f"""UPDATE `{opponentid}` SET tttturn=0""")
                                            cur.execute(f"""UPDATE `{ctx.user.id}` SET turn=0""")
                                            cur.execute(f"""UPDATE `{opponentid}` SET turn=1""")
                                            upd1 = cur2.execute(f"""SELECT ballspinged FROM main""").fetchone()
                                            upd2 = sum(upd1)
                                            upd = int(upd2)
                                            upd += 1
                                            cur2.execute(f"""UPDATE main SET ballspinged={upd}""")
                                            conn.commit()
                                            conn.close()
                                            conn2.close()

                                        elif tttgame[2] == 3 and tttgame[5] == 3 and tttgame [8] == 3:
                                            self.disable_all_items()
                                            await interaction.message.edit(f"<@{opponentid}> won and it's this user's turn to ping a ball! 🏓<:redo:1164986221118902362>\n\n{msgtext}", view=self)
                                            cur.execute(f"""UPDATE `{ctx.user.id}` SET tttgame=111111111""")
                                            cur.execute(f"""UPDATE `{ctx.user.id}` SET tttturn=0""")
                                            cur.execute(f"""UPDATE `{opponentid}` SET tttgame=111111111""")
                                            cur.execute(f"""UPDATE `{opponentid}` SET tttturn=0""")
                                            cur.execute(f"""UPDATE `{ctx.user.id}` SET turn=0""")
                                            cur.execute(f"""UPDATE `{opponentid}` SET turn=1""")
                                            upd1 = cur2.execute(f"""SELECT ballspinged FROM main""").fetchone()
                                            upd2 = sum(upd1)
                                            upd = int(upd2)
                                            upd += 1
                                            cur2.execute(f"""UPDATE main SET ballspinged={upd}""")
                                            conn.commit()
                                            conn.close()
                                            conn2.close()

                                        elif tttgame[0] == 3 and tttgame[1] == 3 and tttgame [2] == 3:
                                            self.disable_all_items()
                                            await interaction.message.edit(f"<@{opponentid}> won and it's this user's turn to ping a ball! 🏓<:redo:1164986221118902362>\n\n{msgtext}", view=self)
                                            cur.execute(f"""UPDATE `{ctx.user.id}` SET tttgame=111111111""")
                                            cur.execute(f"""UPDATE `{ctx.user.id}` SET tttturn=0""")
                                            cur.execute(f"""UPDATE `{opponentid}` SET tttgame=111111111""")
                                            cur.execute(f"""UPDATE `{opponentid}` SET tttturn=0""")
                                            cur.execute(f"""UPDATE `{ctx.user.id}` SET turn=0""")
                                            cur.execute(f"""UPDATE `{opponentid}` SET turn=1""")
                                            upd1 = cur2.execute(f"""SELECT ballspinged FROM main""").fetchone()
                                            upd2 = sum(upd1)
                                            upd = int(upd2)
                                            upd += 1
                                            cur2.execute(f"""UPDATE main SET ballspinged={upd}""")
                                            conn.commit()
                                            conn.close()
                                            conn2.close()

                                        elif tttgame[3] == 3 and tttgame[4] == 3 and tttgame [5] == 3:
                                            self.disable_all_items()
                                            await interaction.message.edit(f"<@{opponentid}> won and it's this user's turn to ping a ball! 🏓<:redo:1164986221118902362>\n\n{msgtext}", view=self)
                                            cur.execute(f"""UPDATE `{ctx.user.id}` SET tttgame=111111111""")
                                            cur.execute(f"""UPDATE `{ctx.user.id}` SET tttturn=0""")
                                            cur.execute(f"""UPDATE `{opponentid}` SET tttgame=111111111""")
                                            cur.execute(f"""UPDATE `{opponentid}` SET tttturn=0""")
                                            cur.execute(f"""UPDATE `{ctx.user.id}` SET turn=0""")
                                            cur.execute(f"""UPDATE `{opponentid}` SET turn=1""")
                                            upd1 = cur2.execute(f"""SELECT ballspinged FROM main""").fetchone()
                                            upd2 = sum(upd1)
                                            upd = int(upd2)
                                            upd += 1
                                            cur2.execute(f"""UPDATE main SET ballspinged={upd}""")
                                            conn.commit()
                                            conn.close()
                                            conn2.close()

                                        elif tttgame[6] == 3 and tttgame[7] == 3 and tttgame [8] == 3:
                                            self.disable_all_items()
                                            await interaction.message.edit(f"<@{opponentid}> won and it's this user's turn to ping a ball! 🏓<:redo:1164986221118902362>\n\n{msgtext}", view=self)
                                            cur.execute(f"""UPDATE `{ctx.user.id}` SET tttgame=111111111""")
                                            cur.execute(f"""UPDATE `{ctx.user.id}` SET tttturn=0""")
                                            cur.execute(f"""UPDATE `{opponentid}` SET tttgame=111111111""")
                                            cur.execute(f"""UPDATE `{opponentid}` SET tttturn=0""")
                                            cur.execute(f"""UPDATE `{ctx.user.id}` SET turn=0""")
                                            cur.execute(f"""UPDATE `{opponentid}` SET turn=1""")
                                            upd1 = cur2.execute(f"""SELECT ballspinged FROM main""").fetchone()
                                            upd2 = sum(upd1)
                                            upd = int(upd2)
                                            upd += 1
                                            cur2.execute(f"""UPDATE main SET ballspinged={upd}""")
                                            conn.commit()
                                            conn.close()
                                            conn2.close()

                                        elif tttgame[0] == 3 and tttgame[4] == 3 and tttgame [8] == 3:
                                            self.disable_all_items()
                                            await interaction.message.edit(f"<@{opponentid}> won and it's this user's turn to ping a ball! 🏓<:redo:1164986221118902362>\n\n{msgtext}", view=self)
                                            cur.execute(f"""UPDATE `{ctx.user.id}` SET tttgame=111111111""")
                                            cur.execute(f"""UPDATE `{ctx.user.id}` SET tttturn=0""")
                                            cur.execute(f"""UPDATE `{opponentid}` SET tttgame=111111111""")
                                            cur.execute(f"""UPDATE `{opponentid}` SET tttturn=0""")
                                            cur.execute(f"""UPDATE `{ctx.user.id}` SET turn=0""")
                                            cur.execute(f"""UPDATE `{opponentid}` SET turn=1""")
                                            upd1 = cur2.execute(f"""SELECT ballspinged FROM main""").fetchone()
                                            upd2 = sum(upd1)
                                            upd = int(upd2)
                                            upd += 1
                                            cur2.execute(f"""UPDATE main SET ballspinged={upd}""")
                                            conn.commit()
                                            conn.close()
                                            conn2.close()

                                        elif tttgame[2] == 3 and tttgame[4] == 3 and tttgame [6] == 3:
                                            self.disable_all_items()
                                            await interaction.message.edit(f"<@{opponentid}> won and it's this user's turn to ping a ball! 🏓<:redo:1164986221118902362>\n\n{msgtext}", view=self)
                                            cur.execute(f"""UPDATE `{ctx.user.id}` SET tttgame=111111111""")
                                            cur.execute(f"""UPDATE `{ctx.user.id}` SET tttturn=0""")
                                            cur.execute(f"""UPDATE `{opponentid}` SET tttgame=111111111""")
                                            cur.execute(f"""UPDATE `{opponentid}` SET tttturn=0""")
                                            cur.execute(f"""UPDATE `{ctx.user.id}` SET turn=0""")
                                            cur.execute(f"""UPDATE `{opponentid}` SET turn=1""")
                                            upd1 = cur2.execute(f"""SELECT ballspinged FROM main""").fetchone()
                                            upd2 = sum(upd1)
                                            upd = int(upd2)
                                            upd += 1
                                            cur2.execute(f"""UPDATE main SET ballspinged={upd}""")
                                            conn.commit()
                                            conn.close()
                                            conn2.close()

                                        elif not 1 in tttgame:
                                            self.disable_all_items()
                                            cur.execute(f"""UPDATE `{ctx.user.id}` SET tttgame=111111111""")
                                            cur.execute(f"""UPDATE `{ctx.user.id}` SET tttturn=0""")
                                            cur.execute(f"""UPDATE `{opponentid}` SET tttgame=111111111""")
                                            cur.execute(f"""UPDATE `{opponentid}` SET tttturn=0""")
                                            cur.execute(f"""UPDATE `{ctx.user.id}` SET turn=0""")
                                            cur.execute(f"""UPDATE `{opponentid}` SET turn=1""")
                                            upd1 = cur2.execute(f"""SELECT ballspinged FROM main""").fetchone()
                                            upd2 = sum(upd1)
                                            upd = int(upd2)
                                            upd += 1
                                            cur2.execute(f"""UPDATE main SET ballspinged={upd}""")
                                            await interaction.message.edit(f"It's draw! Now it's <@{opponentid}>'s turn to ping a ball! 🤜🤛\n\n{one1}<:whitelinevertical:1164986150113513624>{two2}<:whitelinevertical:1164986150113513624>{three3}\n<:whitelinehorizontal:1164986148205109308><:whiteplus:1164986151849959495><:whitelinehorizontal:1164986148205109308><:whiteplus:1164986151849959495><:whitelinehorizontal:1164986148205109308>\n{four4}<:whitelinevertical:1164986150113513624>{five5}<:whitelinevertical:1164986150113513624>{six6}\n<:whitelinehorizontal:1164986148205109308><:whiteplus:1164986151849959495><:whitelinehorizontal:1164986148205109308><:whiteplus:1164986151849959495><:whitelinehorizontal:1164986148205109308>\n{seven7}<:whitelinevertical:1164986150113513624>{eight8}<:whitelinevertical:1164986150113513624>{nine9}", view=self)
                                            conn.commit()
                                            conn.close()
                                            conn2.close()

                                        else:
                                            await interaction.message.edit(msgtext)
                                            conn.close()
                                            conn2.close()

                                        if needdefer:
                                            await interaction.response.defer()

                                    elif anywin:
                                        if tttgame[0] == 3 and tttgame[3] == 3 and tttgame [6] == 3:
                                            self.disable_all_items()
                                            await interaction.message.edit(f"Bot won! Now it's bot's turn to ping a ball! 🏓<:redo:1164986221118902362>\n\n{msgtext}", view=self)
                                            cur.execute(f"""UPDATE `{ctx.user.id}` SET tttgame=111111111""")
                                            cur.execute(f"""UPDATE `{ctx.user.id}` SET tttturn=0""")
                                            upd1 = cur2.execute(f"""SELECT ballspinged FROM main""").fetchone()
                                            upd2 = sum(upd1)
                                            upd = int(upd2)
                                            upd += 1
                                            cur2.execute(f"""UPDATE main SET ballspinged={upd}""")
                                            await ctx.respond("Pong! 🏓")
                                            cur.execute(f"""UPDATE `{ctx.user.id}` SET turn=1""")
                                            conn.commit()
                                            conn.close()
                                            conn2.commit()
                                            conn2.close()

                                        elif tttgame[1] == 3 and tttgame[4] == 3 and tttgame [7] == 3:
                                            self.disable_all_items()
                                            await interaction.message.edit(f"Bot won! Now it's bot's turn to ping a ball! 🏓<:redo:1164986221118902362>\n\n{msgtext}", view=self)
                                            cur.execute(f"""UPDATE `{ctx.user.id}` SET tttgame=111111111""")
                                            cur.execute(f"""UPDATE `{ctx.user.id}` SET tttturn=0""")
                                            upd1 = cur2.execute(f"""SELECT ballspinged FROM main""").fetchone()
                                            upd2 = sum(upd1)
                                            upd = int(upd2)
                                            upd += 1
                                            cur2.execute(f"""UPDATE main SET ballspinged={upd}""")
                                            await ctx.respond("Pong! 🏓")
                                            cur.execute(f"""UPDATE `{ctx.user.id}` SET turn=1""")
                                            conn.commit()
                                            conn.close()
                                            conn2.commit()
                                            conn2.close()

                                        elif tttgame[2] == 3 and tttgame[5] == 3 and tttgame [8] == 3:
                                            self.disable_all_items()
                                            await interaction.message.edit(f"Bot won! Now it's bot's turn to ping a ball! 🏓<:redo:1164986221118902362>\n\n{msgtext}", view=self)
                                            cur.execute(f"""UPDATE `{ctx.user.id}` SET tttgame=111111111""")
                                            cur.execute(f"""UPDATE `{ctx.user.id}` SET tttturn=0""")
                                            upd1 = cur2.execute(f"""SELECT ballspinged FROM main""").fetchone()
                                            upd2 = sum(upd1)
                                            upd = int(upd2)
                                            upd += 1
                                            cur2.execute(f"""UPDATE main SET ballspinged={upd}""")
                                            await ctx.respond("Pong! 🏓")
                                            cur.execute(f"""UPDATE `{ctx.user.id}` SET turn=1""")
                                            conn.commit()
                                            conn.close()
                                            conn2.commit()
                                            conn2.close()

                                        elif tttgame[0] == 3 and tttgame[1] == 3 and tttgame [2] == 3:
                                            self.disable_all_items()
                                            await interaction.message.edit(f"Bot won! Now it's bot's turn to ping a ball! 🏓<:redo:1164986221118902362>\n\n{msgtext}", view=self)
                                            cur.execute(f"""UPDATE `{ctx.user.id}` SET tttgame=111111111""")
                                            cur.execute(f"""UPDATE `{ctx.user.id}` SET tttturn=0""")
                                            upd1 = cur2.execute(f"""SELECT ballspinged FROM main""").fetchone()
                                            upd2 = sum(upd1)
                                            upd = int(upd2)
                                            upd += 1
                                            cur2.execute(f"""UPDATE main SET ballspinged={upd}""")
                                            await ctx.respond("Pong! 🏓")
                                            cur.execute(f"""UPDATE `{ctx.user.id}` SET turn=1""")
                                            conn.commit()
                                            conn.close()
                                            conn2.commit()
                                            conn2.close()

                                        elif tttgame[3] == 3 and tttgame[4] == 3 and tttgame [5] == 3:
                                            self.disable_all_items()
                                            await interaction.message.edit(f"Bot won! Now it's bot's turn to ping a ball! 🏓<:redo:1164986221118902362>\n\n{msgtext}", view=self)
                                            cur.execute(f"""UPDATE `{ctx.user.id}` SET tttgame=111111111""")
                                            cur.execute(f"""UPDATE `{ctx.user.id}` SET tttturn=0""")
                                            upd1 = cur2.execute(f"""SELECT ballspinged FROM main""").fetchone()
                                            upd2 = sum(upd1)
                                            upd = int(upd2)
                                            upd += 1
                                            cur2.execute(f"""UPDATE main SET ballspinged={upd}""")
                                            await ctx.respond("Pong! 🏓")
                                            cur.execute(f"""UPDATE `{ctx.user.id}` SET turn=1""")
                                            conn.commit()
                                            conn.close()
                                            conn2.commit()
                                            conn2.close()

                                        elif tttgame[6] == 3 and tttgame[7] == 3 and tttgame [8] == 3:
                                            self.disable_all_items()
                                            await interaction.message.edit(f"Bot won! Now it's bot's turn to ping a ball! 🏓<:redo:1164986221118902362>\n\n{msgtext}", view=self)
                                            cur.execute(f"""UPDATE `{ctx.user.id}` SET tttgame=111111111""")
                                            cur.execute(f"""UPDATE `{ctx.user.id}` SET tttturn=0""")
                                            upd1 = cur2.execute(f"""SELECT ballspinged FROM main""").fetchone()
                                            upd2 = sum(upd1)
                                            upd = int(upd2)
                                            upd += 1
                                            cur2.execute(f"""UPDATE main SET ballspinged={upd}""")
                                            await ctx.respond("Pong! 🏓")
                                            cur.execute(f"""UPDATE `{ctx.user.id}` SET turn=1""")
                                            conn.commit()
                                            conn.close()
                                            conn2.commit()
                                            conn2.close()

                                        elif tttgame[0] == 3 and tttgame[4] == 3 and tttgame [8] == 3:
                                            self.disable_all_items()
                                            await interaction.message.edit(f"Bot won! Now it's bot's turn to ping a ball! 🏓<:redo:1164986221118902362>\n\n{msgtext}", view=self)
                                            cur.execute(f"""UPDATE `{ctx.user.id}` SET tttgame=111111111""")
                                            cur.execute(f"""UPDATE `{ctx.user.id}` SET tttturn=0""")
                                            upd1 = cur2.execute(f"""SELECT ballspinged FROM main""").fetchone()
                                            upd2 = sum(upd1)
                                            upd = int(upd2)
                                            upd += 1
                                            cur2.execute(f"""UPDATE main SET ballspinged={upd}""")
                                            await ctx.respond("Pong! 🏓")
                                            cur.execute(f"""UPDATE `{ctx.user.id}` SET turn=1""")
                                            conn.commit()
                                            conn.close()
                                            conn2.commit()
                                            conn2.close()

                                        elif tttgame[2] == 3 and tttgame[4] == 3 and tttgame [6] == 3:
                                            self.disable_all_items()
                                            await interaction.message.edit(f"Bot won! Now it's bot's turn to ping a ball! 🏓<:redo:1164986221118902362>\n\n{msgtext}", view=self)
                                            cur.execute(f"""UPDATE `{ctx.user.id}` SET tttgame=111111111""")
                                            cur.execute(f"""UPDATE `{ctx.user.id}` SET tttturn=0""")
                                            upd1 = cur2.execute(f"""SELECT ballspinged FROM main""").fetchone()
                                            upd2 = sum(upd1)
                                            upd = int(upd2)
                                            upd += 1
                                            cur2.execute(f"""UPDATE main SET ballspinged={upd}""")
                                            await ctx.respond("Pong! 🏓")
                                            cur.execute(f"""UPDATE `{ctx.user.id}` SET turn=1""")
                                            conn.commit()
                                            conn.close()
                                            conn2.commit()
                                            conn2.close()

                                        elif not 1 in tttgame:
                                            self.disable_all_items()
                                            await interaction.message.edit(f"It's draw! Now it's bot's turn to ping a ball! 🤜🤛\n\n{one1}<:whitelinevertical:1164986150113513624>{two2}<:whitelinevertical:1164986150113513624>{three3}\n<:whitelinehorizontal:1164986148205109308><:whiteplus:1164986151849959495><:whitelinehorizontal:1164986148205109308><:whiteplus:1164986151849959495><:whitelinehorizontal:1164986148205109308>\n{four4}<:whitelinevertical:1164986150113513624>{five5}<:whitelinevertical:1164986150113513624>{six6}\n<:whitelinehorizontal:1164986148205109308><:whiteplus:1164986151849959495><:whitelinehorizontal:1164986148205109308><:whiteplus:1164986151849959495><:whitelinehorizontal:1164986148205109308>\n{seven7}<:whitelinevertical:1164986150113513624>{eight8}<:whitelinevertical:1164986150113513624>{nine9}", view=self)
                                            cur.execute(f"""UPDATE `{ctx.user.id}` SET tttgame=111111111""")
                                            cur.execute(f"""UPDATE `{ctx.user.id}` SET tttturn=0""")
                                            upd1 = cur2.execute(f"""SELECT ballspinged FROM main""").fetchone()
                                            upd2 = sum(upd1)
                                            upd = int(upd2)
                                            upd += 1
                                            cur2.execute(f"""UPDATE main SET ballspinged={upd}""")
                                            await ctx.respond("Pong! 🏓")
                                            cur.execute(f"""UPDATE `{ctx.user.id}` SET turn=1""")
                                            conn.commit()
                                            conn.close()
                                            conn2.commit()
                                            conn2.close()

                                        else:
                                            await interaction.message.edit(msgtext)
                                            conn.close()
                                            conn2.close()

                                        if needdefer:
                                            await interaction.response.defer()

                                else:
                                    await interaction.response.send_message("Sorry, but this action is not valid. Please check if you are playing this game or your opponent didn't leave the match. <:crosspong:1134110291311992962>", ephemeral=True)
                                    conn.close()
                                    conn2.close()
                                    consoleclear()

                            else:
                                await interaction.response.send_message("Sorry, but this action is not valid. Please check if you are playing this game or your opponent didn't leave the match. <:crosspong:1134110291311992962>", ephemeral=True)
                                conn.close()
                                conn2.close()
                                consoleclear()

                        else:
                            await interaction.response.send_message("Sorry, but it's not your turn. <:crosspong:1134110291311992962>", ephemeral=True)
                            conn.close()
                            conn2.close()
                            consoleclear()

                    except:
                        await interaction.response.send_message("Sorry, but this action is not valid. Please check if you are playing this game, it's your turn or your opponent didn't leave the match. <:crosspong:1134110291311992962>", ephemeral=True)
                        conn.close()
                        conn2.close()
                        consoleclear()

            inter = await ctx.respond(f"__**TIC-TAC-TOE TIME!**__ <:bluex:1164986327167672361><:redo:1164986221118902362>\n\nIf <@{ctx.user.id}> wins, the minigame ends and this user wins this match. Other situations ends with <@{opponentid}>'s turn. <@{ctx.user.id}> is playing with <:bluex:1164986327167672361> and <@{opponentid}> is playing with <:redo:1164986221118902362>. <@{ctx.user.id}> starts first. <:circlepong:1134110288438894654>\n\n{one1}<:whitelinevertical:1164986150113513624>{two2}<:whitelinevertical:1164986150113513624>{three3}\n<:whitelinehorizontal:1164986148205109308><:whiteplus:1164986151849959495><:whitelinehorizontal:1164986148205109308><:whiteplus:1164986151849959495><:whitelinehorizontal:1164986148205109308>\n{four4}<:whitelinevertical:1164986150113513624>{five5}<:whitelinevertical:1164986150113513624>{six6}\n<:whitelinehorizontal:1164986148205109308><:whiteplus:1164986151849959495><:whitelinehorizontal:1164986148205109308><:whiteplus:1164986151849959495><:whitelinehorizontal:1164986148205109308>\n{seven7}<:whitelinevertical:1164986150113513624>{eight8}<:whitelinevertical:1164986150113513624>{nine9}", view=menuView())
            originalmsg = await inter.original_response()
            cur.execute(f"""UPDATE `{ctx.user.id}` SET lastminigameid={originalmsg.id}""")

            tttbot1 = cur.execute(f"""SELECT tttbot FROM `{ctx.user.id}`""").fetchone()
            tttbot2 = sum(tttbot1)
            tttbot = int(tttbot2)

            if tttbot == 3:
                cur.execute(f"""UPDATE `{opponentid}` SET lastminigameid={originalmsg.id}""")
            
            conn.commit()
            conn.close()

        except:
            # I'll use this to print errors.
            pass
    
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

        ttt1 = curso.execute(f"""SELECT tttturn FROM `{ctx.user.id}`""").fetchone()
        ttt2 = sum(ttt1)
        tttturn = int(ttt2)

        gameover = random.randint(6,25)
        gamegen = 5#random.randint(3,7)

        if isplaying2 == 1:
            if opponentid2 != bot.user.id:
                if opponentid2 != ctx.user.id and turn2 == 0 and ctxrps == 0 and tttturn == 0:
                    await ctx.respond("Sorry, but it's not your turn. <:crosspong:1134110291311992962>", ephemeral=True)
                    conne.close()
                    connn2.close()
                    consoleclear()

                elif ctxrps != 0:
                    await ctx.respond("Sorry, but you're playing RPS right now. <:crosspong:1134110291311992962>", ephemeral=True)
                    conne.close()
                    connn2.close()

                elif tttturn != 0:
                    await ctx.respond("Sorry, but you're playing Tic-Tac-Toe right now. <:crosspong:1134110291311992962>", ephemeral=True)
                    conne.close()
                    connn2.close()
                
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
                    
                elif isplaying2 == 1 and opponentid2 != ctx.user.id and turn2 == 1 and gamegen == 6:
                    upd1 = curs2.execute(f"""SELECT rpsgames FROM main""").fetchone()
                    upd2 = sum(upd1)
                    upd = int(upd2)
                    upd += 1
                    curs2.execute(f"""UPDATE main SET rpsgames={upd}""")
                    conne.close()
                    connn2.commit()
                    connn2.close()
                    await rps()

                elif isplaying2 == 1 and opponentid2 != ctx.user.id and turn2 == 1 and gamegen == 5:
                    upd1 = curs2.execute(f"""SELECT tttgames FROM main""").fetchone()
                    upd2 = sum(upd1)
                    upd = int(upd2)
                    upd += 1
                    curs2.execute(f"""UPDATE main SET tttgames={upd}""")
                    conne.close()
                    connn2.commit()
                    connn2.close()
                    await ttt()
                    
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
                if isfirstping == 0 and ctxrps == 0 and tttturn == 0:
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

                elif tttturn != 0:
                    await ctx.respond("Sorry, but you're playing Tic-Tac-Toe right now. <:crosspong:1134110291311992962>", ephemeral=True)
                    conne.close()
                    connn2.close()

                elif gameover != 6 and gamegen != 6 and gamegen != 5:
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

                elif gameover != 6 and gamegen == 6:
                    upd1 = curs2.execute(f"""SELECT rpsgames FROM main""").fetchone()
                    upd2 = sum(upd1)
                    upd = int(upd2)
                    upd += 1
                    curs2.execute(f"""UPDATE main SET rpsgames={upd}""")
                    conne.close()
                    connn2.close()
                    await rps()

                elif gameover != 6 and gamegen == 5:
                    upd1 = curs2.execute(f"""SELECT tttgames FROM main""").fetchone()
                    upd2 = sum(upd1)
                    upd = int(upd2)
                    upd += 1
                    curs2.execute(f"""UPDATE main SET tttgames={upd}""")
                    conne.close()
                    connn2.close()
                    await ttt()
                    
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
        
    except:
        await ctx.respond("Sorry, but you are not playing with anyone. <:crosspong:1134110291311992962>", ephemeral=True)
        consoleclear()
   
# Singleplayer command (v1.1)
   
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
        cur.execute(f"""CREATE TABLE `{ctx.user.id}` (isplaying int, opponentid int, turn int, rps int, rpsbot int, isfirstping int, tttturn int, tttgame int, tttbot int, lastminigameid int)""")
        cur.execute(f"""INSERT INTO `{ctx.user.id}` VALUES (1, {bot.user.id}, 1, 0, 0, 0, 0, 111111111, 0, 0)""")
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
        
# Help command (v1.0)

@bot.slash_command(description="Get started playing with DisPong.")
async def help(ctx):
    showcase = discord.File("showcase.gif")
    await ctx.respond("Hello! Thank you for using my bot! I coded this bot in Python with Pycord library. Since this is an open-source bot, the script is available on GitHub. Also, there is another version of the bot: without minigames. Join the support server below if you are interested in one of these things.\n\nIf you are using DisPong for the first time, I recommend you watching the gif below.\n\nCurrent commands:\n</help:999334780732719244> - This message.\n</ping:999267081629487196> - Play Ping Pong.\n</duel:1085970985552978033> - Start new game with antoher player.\n</finish:999267081629487195> - Delete your request or finish a game.\n</singleplayer:1085970985552978034> - Play with the bot.\n</changelog:1085970985552978035> - DisPong updates log.\n</stats:1134139510070980648> - Games statistics.\n\nThat's all! I really hope you'll like my bot! If you need some help, want to report a bug, suggest something, or just want to play with others, join our support server: https://discord.gg/dduRC6cdy3", file=showcase)
    
# Changelog command (v1.0)

@bot.slash_command(description="DisPong updates log.")
async def changelog(ctx):
    await ctx.respond("__v1.1__: Added Singleplayer and better looking responses.\n__v1.2__: Added RPS minigame, games statistics and custom emojis (more emojis are going to be added soon). Fixed some bugs in </duel:1085970985552978033> command.\n__v1.3__: Added Tic-Tac-Toe minigame, updated </stats:1134139510070980648> with total RPS and Tic-Tac-Toe minigames played counter, implemented bugfix of </duel:1085970985552978033> and RPS minigame. Added showcase gif in </help:999334780732719244>\n\n*More comming soon!*")
    
# Statistics command (v1.2)

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

    rpsgames1 = cur.execute(f"""SELECT rpsgames FROM main""").fetchone()
    rpsgames2 = sum(rpsgames1)
    rpsgames = int(rpsgames2)

    tttgames1 = cur.execute(f"""SELECT tttgames FROM main""").fetchone()
    tttgames2 = sum(tttgames1)
    tttgames = int(tttgames2)

    await ctx.respond(f"__Statistics:__\nTotal games played: {totalgames}\nTotal RPS minigames played: {rpsgames}\nTotal Tic-Tac-Toe minigames played: {tttgames}\nCurrent games playing: {currentgames}\nCurrent singleplayer games: {botgames}\nTotal balls pinged: {ballspinged}")

    conn.close()
    consoleclear()
    
bot.run(token)
