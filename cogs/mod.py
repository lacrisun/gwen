import nextcord
import humanfriendly
import datetime
from nextcord.ext import commands


class Moderation(commands.Cog):
    def __init__(self, client):
        self.client = client

    #command to kick a member
    @commands.command()
    @commands.guild_only()
    @commands.has_permissions(kick_members=True) #checking if the caller has kick permissions
    async def kick(self, ctx, member : nextcord.Member, *, reason=None):
        channel = self.client.get_channel(887951374367752202)
        await member.kick(reason=reason)
        await ctx.reply(f'**{member.mention} kicked.\nreason: {reason}**')
        em = nextcord.Embed(title="gwen logs", colour=nextcord.Color.from_rgb(87, 7, 0))
        em.add_field(name="Moderation", value=f"{member.mention} kicked", inline=False)
        em.add_field(name="Reason", value=reason, inline=False)
        await channel.send(embed=em)


    #error handling for kicking    
    @kick.error
    async def kick_error(self, ctx, error):
        if isinstance(error, commands.MissingPermissions):
            await ctx.reply("you don't have permission to kick members, dumbass.") 
        if isinstance(error, commands.MissingRequiredArgument):
            await ctx.reply("you forgot to mention someone.")
        if isinstance(error, commands.BadArgument):
            await ctx.reply("sorry, there has been an error.")           
    
    #command to ban a member   
    @commands.command()
    @commands.guild_only()
    @commands.has_permissions(ban_members=True) #checking if the caller has ban permissions
    async def ban(self, ctx, member : nextcord.Member, *, reason=None):
        channel = self.client.get_channel(887951374367752202)
        await member.ban(reason=reason)
        await ctx.reply(f'**{member} banned.\nreason: {reason}**')
        em = nextcord.Embed(title="gwen logs", colour=nextcord.Color.from_rgb(87, 7, 0))
        em.add_field(name="Moderation", value=f"{member.mention} banned", inline=False)
        em.add_field(name="Reason", value=reason, inline=False)
        await channel.send(embed=em)

    #error handling for bans     
    @ban.error
    async def ban_error(self, ctx, error):
        if isinstance(error, commands.MissingPermissions):
            await ctx.reply("you don't have permission to ban members, dumbass.")    
        if isinstance(error, commands.MissingRequiredArgument):
            await ctx.reply("you forgot to mention someone.")
        if isinstance(error, commands.BadArgument):
            await ctx.reply("sorry, there has been an error.")   

    #command to unban a member
    @commands.command()
    @commands.guild_only()
    @commands.has_permissions(ban_members=True) #checking if the caller has ban permissions
    async def unban(self, ctx, *, member):
        channel = self.client.get_channel(887951374367752202) 
        banned_users = await ctx.guild.bans()
        member_name, member_discriminator = member.split('#')

        for ban_entry in banned_users:
            user = ban_entry.user

            if (user.name, user.discriminator) == (member_name, member_discriminator):
                await ctx.guild.unban(user)
                await ctx.reply(f'**{user.name}#{user.discriminator} has been unbanned.**')
                em = nextcord.Embed(title="gwen logs", colour=nextcord.Color.from_rgb(87, 7, 0))
                em.add_field(name="Moderation", value=f"{member.mention} unbanned", inline=False)
                await channel.send(embed=em)
                return

    #called when the caller don't have ban permissions
    @unban.error
    async def unban_error(self, ctx, error):
        if isinstance(error, commands.MissingPermissions):
            await ctx.reply("you don't have permission to ban members, dumbass.")
        if isinstance(error, commands.BadArgument):
            await ctx.reply("sorry, there has been an error.")
            
    #command a put a user in timeout
    @commands.command()
    @commands.guild_only()
    @commands.has_permissions(manage_messages=True)
    async def mute(self, ctx, member : nextcord.Member, time, *, reason=None):
        channel = self.client.get_channel(887951374367752202)
        time = humanfriendly.parse_timespan(time)
        await member.edit(timeout=nextcord.utils.utcnow()+datetime.timedelta(seconds=time), reason=reason)
        await ctx.reply(f'**{member.mention} is on timeout.\nreason: {reason}**')
        em = nextcord.Embed(title="gwen logs", colour=nextcord.Color.from_rgb(87, 7, 0))
        em.add_field(name="Moderation", value=f"{member.mention} was muted for {time}", inline=False)
        em.add_field(name="Reason", value=reason, inline=False)
        await channel.send(embed=em)

    #error handling for timeout
    @mute.error
    async def timeout_error(self, ctx, error):
        if isinstance(error, commands.MissingPermissions):
            await ctx.reply("you don't have permissions to timeout members, shithead.") 
        if isinstance(error, commands.MissingRequiredArgument):
            await ctx.reply("please type the command correctly $timeout @target time(m/s) reason(optional).")
        if isinstance(error, commands.BadArgument):
            await ctx.reply("sorry, there has been an error.")

    #command to untimeout a user
    @commands.command()
    @commands.guild_only()
    @commands.has_permissions(manage_messages=True)
    async def unmute(self, ctx, member : nextcord.Member):
        channel = self.client.get_channel(887951374367752202)
        await member.edit(timeout=None)
        await ctx.reply(f'**timeout removed for {member.mention}**')
        em = nextcord.Embed(title="gwen logs", colour=nextcord.Color.from_rgb(87, 7, 0))
        em.add_field(name="Moderation", value=f"{member.mention} was unmuted", inline=False)
        await channel.send(embed=em)

    #untimeout error handling
    @unmute.error
    async def untimeout_error(self, ctx, error):
        if isinstance(error, commands.MissingPermissions):
            await ctx.reply("you don't have permissions to timeout members, shithead.")
        if isinstance(error, commands.MissingRequiredArgument):
            await ctx.reply("please type the command correctly $untimeout @target.")
        if isinstance(error, commands.BadArgument):
            await ctx.reply("sorry, there has been an error.")

def setup(client):
    client.add_cog(Moderation(client))