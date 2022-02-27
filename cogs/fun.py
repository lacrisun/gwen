import nextcord
import random
import os
from aiohttp import ClientSession
from nextcord.ext import commands

class Coinflip(nextcord.ui.View):
    def __init__(self):
        super().__init__()
        self.value = None

    @nextcord.ui.button(label='heads', style=nextcord.ButtonStyle.green)
    async def heads(self, button:nextcord.ui.Button, interaction:nextcord.Interaction):
        await interaction.response.send_message('flipping..', ephemeral=False)
        self.value = 1
        self.stop()
    @nextcord.ui.button(label='tails', style=nextcord.ButtonStyle.green)
    async def tails(self, button:nextcord.ui.Button, interaction:nextcord.Interaction):
        await interaction.response.send_message('flipping..', ephemeral=False)
        self.value = 2
        self.stop()

class Fun(commands.Cog):
    def __init__(self, client):
        self.client = client

    #command to dislay a user's avatar
    @commands.command(aliases=['pfp'])
    async def avatar(self, ctx, member : nextcord.Member=None):
        if member == None:
            member = ctx.author

        pfp = member.display_avatar
        await ctx.send(pfp)

    #command to simulate messaging for the bot
    @commands.command()
    async def say(self, ctx, *, message=None):
        if message == None:
            return ctx.reply("what do you want me to say..")
        else:
            await ctx.send(message)
            await ctx.message.delete()

    #command to ask a question
    @commands.command(aliases=['ask'])
    async def question(self, ctx):
        responses = ['ugh, yes..',
                    'yeah, maybe.',
                    "we'll see.",
                    'yeah, yeah whatever.',
                    'oh god just kill me already',
                    'no, go fuck yourself.',
                    'maybe? i dunno',
                    'what? hell no',
                    'hell yeah',
                    'how the hell am i supposed to know',
                    "I. DON'T. KNOW.",
                    "can't you bother me when i'm not busy??",
                    'YESS',
                    "please don't ask me about this ever again.",
                    'no.',
                    'probably.',
                    "i don't like it.",
                    "i can't tell"]
        await ctx.reply(random.choice(responses))

    # command to reveal info about a user
    @commands.command()
    async def whois(self, ctx, member : nextcord.Member):
        info_embed = nextcord.Embed(title=member.name, description=member.mention, colour=nextcord.Color.from_rgb(87, 7, 0))
        joinedat = member.joined_at.strftime('%A, %B %d %Y')
        createdat = member.created_at.strftime('%A, %B %d %Y')
        info_embed.set_thumbnail(url=member.display_avatar)
        info_embed.add_field(name="- ID", value=f'```{member.id}```', inline=False)
        info_embed.add_field(name=f'- Discriminator :', value=f'```#{member.discriminator}```', inline=False)
        
        mention = []
        for role in member.roles:
            if role.name != "@everyone":
                mention.append(role.mention)

        ok = "\u200b".join(mention)        

        info_embed.add_field(name='- Created at : ', value=f'```{createdat}```', inline=False)
        info_embed.add_field(name='- Joined at : ', value=f'```{joinedat}```', inline=False)
        if mention == []:
            info_embed.add_field(name='- Roles :', value='```no roles```', inline=False)
        else:    
            info_embed.add_field(name='- Roles :', value=ok, inline=False) 
        info_embed.set_footer(text= f'requested by {ctx.author.name}', icon_url=ctx.author.display_avatar)
        await ctx.send(embed=info_embed)

    @commands.command(aliases=['urban'])
    async def urbandictionary(self, ctx, term):
        url = "https://mashape-community-urban-dictionary.p.rapidapi.com/define"
        querystring = {"term":term}

        headers = {
        'x-rapidapi-host': "mashape-community-urban-dictionary.p.rapidapi.com",
        'x-rapidapi-key': "a78e8a6be1mshc0296c15e52ea11p1b27cdjsna9602af63066"
        }
        async with ClientSession() as session:
            async with session.get(url, headers=headers, params=querystring) as response:
                r = await response.json()
                embed = nextcord.Embed(title=f"first result for : {term}", colour=nextcord.Color.from_rgb(87, 7, 0))
                definition = r['list'][0]['definition']
                embed.add_field(name=term, value=definition, inline=False)
                await ctx.send(embed=embed)
        
    @commands.command()
    @commands.guild_only()
    @commands.cooldown(1, 30, commands.BucketType.user)
    async def coinflip(self, ctx):
        view = Coinflip()
        await ctx.send("heads or tails?", view=view)
        await view.wait()
            
        if view.value == 1:
            num = random.randint(1, 2)
            if num == 1:
                await ctx.reply("**it's heads!**")
            else:
                return await ctx.reply("it's tails, better luck next time..")
        if view.value == 2:
            num = random.randint(1, 2)
            if num == 2:
                await ctx.reply("**it's tails!**")
            else:
                return await ctx.reply("it's heads, better luck next time..")

    #error handling for beg
    @coinflip.error
    async def on_command_error(self, ctx, error):
        if isinstance(error, commands.CommandOnCooldown):
            await ctx.reply(f"you're in cooldown for {round(error.retry_after * 1)}s, wait a few moment then try again.")

def setup(client):
    client.add_cog(Fun(client))