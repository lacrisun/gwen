import nextcord
import os
import datetime
import random
from nextcord.ext import commands
from dotenv import load_dotenv
load_dotenv()

activity = nextcord.Activity(activity=nextcord, type=nextcord.ActivityType.watching, name="$porn")
client = commands.Bot(command_prefix="$", activity=activity, status=nextcord.Status.online)
client.remove_command('help')
versionbot = "1.2.0"

#On ready
@client.event
async def on_ready():
    print(f'{client.user.name} is logged in.')

for filename in os.listdir('./cogs'):
    if filename.endswith('.py'):
        client.load_extension(f'cogs.{filename[:-3]}')

@client.command()
async def unload(ctx, extension):
    client.unload_extension(f'cogs.{extension}')

@client.command()
async def load(ctx, extension):
    client.load_extension(f'cogs.{extension}')

@client.command()
async def reload(ctx, extension):
    client.unload_extension(f'cogs.{extension}')
    client.load_extension(f'cogs.{extension}')

#error handling if user called an unlisted command
@client.event
async def on_command_error(ctx, error):
    if isinstance(error, commands.errors.CommandNotFound):
        await ctx.reply("command not found, please read the command list using $help")

#test the latency of the bot
@client.command()
async def ping(ctx):
    await ctx.reply(f'**pong! message sent in {round(client.latency * 1000)}ms**')

@client.command()
async def porn(ctx):
    await ctx.reply('no')

#info bot
@client.command()
async def info(ctx):
    server_amt = len(client.guilds)
    em = nextcord.Embed(title=f"gwen v{versionbot}", description="hello.\ni am CampCorp's personal assistant. totally not a dead person's brain digitalized into code.", colour=nextcord.Color.from_rgb(87, 7, 0))
    em.add_field(name=f"currently serving :", value=f"{server_amt} servers.", inline=False)
    em.add_field(name="made by :", value="lacrisun", inline=False)
    em.add_field(name="source code :", value="you can view gwen's source code on [GitHub](https://github.com/gustcode/gwen).", inline=False)
    em.add_field(name="support my creator on :", value="[Instagram](https://instagram.com/lacrisun)\n[Ko-Fi](https://ko-fi.com/lacri)")
    await ctx.send(embed=em)

player1 = ""
player2 = ""
turn = ""
gameOver = True

board = []

winningConditions = [
    [0, 1, 2],
    [3, 4, 5],
    [6, 7, 8],
    [0, 3, 6],
    [1, 4, 7],
    [2, 5, 8],
    [0, 4, 8],
    [2, 4, 6]
]

@client.command(aliases=['ttt'])
@commands.guild_only()
@commands.cooldown(1, 60, commands.BucketType.user)
async def tictactoe(ctx, p1: nextcord.Member=None, p2: nextcord.Member=None):
    global count
    global player1
    global player2
    global turn
    global gameOver

    if gameOver:
        global board
        board = [":white_large_square:", ":white_large_square:", ":white_large_square:",
                ":white_large_square:", ":white_large_square:", ":white_large_square:",
                ":white_large_square:", ":white_large_square:", ":white_large_square:"]
        turn = ""
        gameOver = False
        count = 0

        if p1 == None:
            p1 = ctx.author
        if p2 == None:
            p2 = ctx.author
            
        player1 = p1
        player2 = p2

            # print the board
        line = ""
        for x in range(len(board)):
            if x == 2 or x == 5 or x == 8:
                line += " " + board[x]
                await ctx.send(line)
                line = ""
            else:
                line += " " + board[x]

            # determine who goes first
        num = random.randint(1, 2)
        if num == 1:
            turn = player1
            await ctx.send("**it's tictactoe. use the $place command to place your piece, eg : $place 3**")
            await ctx.send("**it is <@" + str(player1.id) + ">'s turn.**")
        elif num == 2:
            turn = player2
            await ctx.send("**it's tictactoe. use the $place command to place your piece, eg : $place 3**")
            await ctx.send("**it is <@" + str(player2.id) + ">'s turn.**")
    else:
        await ctx.send("a game is in progress. but if you want to reset, type $abort_ttt")

@client.command()
@commands.guild_only()
async def abort_ttt(ctx):
    global turn
    global player1
    global player2
    global board
    global count
    global gameOver

    gameOver = True
    await ctx.reply("game has been aborted, type $ttt to play again.")

@client.command()
@commands.guild_only()
async def place(ctx, pos: int):
    global turn
    global player1
    global player2
    global board
    global count
    global gameOver

    def checkWinner(winningConditions, mark):
        global gameOver
        for condition in winningConditions:
            if board[condition[0]] == mark and board[condition[1]] == mark and board[condition[2]] == mark:
                gameOver = True

    if not gameOver:
        mark = ""
        if turn == ctx.author:
            if turn == player1:
                mark = ":regional_indicator_x:"
            elif turn == player2:
                mark = ":o2:"
            if 0 < pos < 10 and board[pos - 1] == ":white_large_square:" :
                board[pos - 1] = mark
                count += 1

                    # print the board
                line = ""
                for x in range(len(board)):
                    if x == 2 or x == 5 or x == 8:
                        line += " " + board[x]
                        await ctx.send(line)
                        line = ""
                    else:
                        line += " " + board[x]

                checkWinner(winningConditions, mark)
                print(count)
                if gameOver == True:
                    await ctx.send(mark + "** wins.**")
                elif count >= 9:
                    gameOver = True
                    await ctx.send("what a bunch of losers.")

                    # switch turns
                if turn == player1:
                    turn = player2
                elif turn == player2:
                    turn = player1
            else:
                await ctx.reply("be sure to choose an integer between 1 and 9 (inclusive) and an unmarked tile.")
        else:
            await ctx.reply("it is not your turn.")
    else:
        await ctx.reply("please start a new game using the !tictactoe command.")

@tictactoe.error
async def tictactoe_error(self, ctx, error):
    if isinstance(error, commands.MissingRequiredArgument):
        await ctx.reply("please mention 2 players for this command.")
    elif isinstance(error, commands.BadArgument):
        await ctx.reply("please make sure to mention/ping players.")
    if isinstance(error, commands.CommandOnCooldown):
        await ctx.reply(f"you're in cooldown for {round(error.retry_after * 1)}s, wait a few moment then try again.")

@place.error
async def place_error(self, ctx, error):
    if isinstance(error, commands.MissingRequiredArgument):
        await ctx.reply("please enter a position you would like to mark.")
    elif isinstance(error, commands.BadArgument):
        await ctx.reply("please make sure to enter an integer.")

@client.command()
async def help(ctx):
    user = ctx.author
    em = nextcord.Embed(title="List of commands", colour=nextcord.Color.from_rgb(87, 7, 0))
    em.add_field(name="Admin", value="- $kick\nkicks a member\n\n- $ban\nbans a member\n\n- $mute\nputs a member in timeout\n\n- $unban\nunbans a member\n\n- $unmute\nputs a member out from timeout\n\n", inline=False)
    em.add_field(name="General", value="- $ping\ndisplays the bot's latency\n\n- $info\ndisplays info about the bot\n\n- $whois\ndisplays info about a user\n\n- $inbox\ndisplay the bot's patch note\n\n", inline=False)
    em.add_field(name="Fun", value="- $avatar\nposts the user's avatar\n\n- $say\ndo i really have to explain this?\n\n- $question\nask gwen a question\n\n- $urban\nlook a definition of a word\n\n- $qrcode\ncreate a qrcode from text\n\n", inline=False)
    await user.send(embed=em)

client.run(os.getenv('TOKEN'))