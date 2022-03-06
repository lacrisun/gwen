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
        await member.kick(reason=reason)
        await ctx.reply(f'**{member.mention} kicked.\nreason: {reason}**')

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
        await member.ban(reason=reason)
        await ctx.reply(f'**{member} banned.\nreason: {reason}**')

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
        banned_users = await ctx.guild.bans()
        member_name, member_discriminator = member.split('#')

        for ban_entry in banned_users:
            user = ban_entry.user

            if (user.name, user.discriminator) == (member_name, member_discriminator):
                await ctx.guild.unban(user)
                await ctx.reply(f'**{user.name}#{user.discriminator} has been unbanned.**')
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
    async def timeout(self, ctx, member : nextcord.Member, time, *, reason=None):
        time = humanfriendly.parse_timespan(time)
        await member.edit(timeout=nextcord.utils.utcnow()+datetime.timedelta(seconds=time), reason=reason)
        await ctx.reply(f'**{member.mention} is on timeout.\nreason: {reason}**')

    #error handling for timeout
    @timeout.error
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
    async def untimeout(self, ctx, member : nextcord.Member):
        await member.edit(timeout=None)
        await ctx.reply(f'**timeout removed for {member.mention}**')

    #untimeout error handling
    @untimeout.error
    async def untimeout_error(self, ctx, error):
        if isinstance(error, commands.MissingPermissions):
            await ctx.reply("you don't have permissions to timeout members, shithead.")
        if isinstance(error, commands.MissingRequiredArgument):
            await ctx.reply("please type the command correctly $untimeout @target.")
        if isinstance(error, commands.BadArgument):
            await ctx.reply("sorry, there has been an error.")

def setup(client):
    client.add_cog(Moderation(client))