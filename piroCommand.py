from string import ascii_uppercase
import piro3112bot
import piroYoutube

@piro3112bot.bot.command()
async def gank(ctx, song_num = 0, channel_name = None):
    print(song_num)
    print(type(song_num))
    if(channel_name == None):
        if(ctx.author.voice == None):
            await ctx.send("チャンネルに繋ぐかチャンネルを指定するかしてください")
        else:
            if (ctx.bot not in ctx.author.voice.channel.members):  
                if (ctx.guild.voice_client != None):
                    await ctx.guild.voice_client.disconnect()              
                await ctx.author.voice.channel.connect()
            if (not ctx.guild.voice_client.is_playing()):
                if (song_num == 0):
                    url = "https://www.youtube.com/watch?v=WHzs3yPHL9I"
                    await ctx.send("わんわんディスコフィーバー")
                elif (song_num == 1):
                    url = "https://www.youtube.com/watch?v=ERkSupJS7-Q"
                    await ctx.send("ポケットからきゅんです")
                else:
                    await ctx.send("0: わんわんディスコフィーバー\n1: ポケットからきゅんです")
                    return
                player = await piroYoutube.YTDLSource.from_url(url, loop=piro3112bot.bot.loop)
                ctx.guild.voice_client.play(player)
    else:
        for channel in ctx.guild.voice_channels:
            if(channel.name == channel_name):
                if (ctx.bot not in channel.members):
                    if (ctx.guild.voice_client != None):
                        await ctx.guild.voice_client.disconnect()                
                    await channel.connect()
                if (not ctx.guild.voice_client.is_playing()):
                    if (song_num == 0):
                        url = "https://www.youtube.com/watch?v=WHzs3yPHL9I"
                        await ctx.send("わんわんディスコフィーバー")
                    elif (song_num == 1):
                        url = "https://www.youtube.com/watch?v=ERkSupJS7-Q"
                        await ctx.send("ポケットからきゅんです")
                    else:
                        await ctx.send("0: わんわんディスコフィーバー\n1: ポケットからきゅんです")
                        return
                    player = await piroYoutube.YTDLSource.from_url(url, loop=piro3112bot.bot.loop)
                    ctx.guild.voice_client.play(player)
                return
        await ctx.send("チャンネルが見つかりませんでした")

@piro3112bot.bot.command()
async def stop(ctx):
    if(ctx.guild.voice_client == None):
        await ctx.send("接続していません")
        return
    elif(not ctx.guild.voice_client.is_playing()):
        await ctx.send("再生していません")
        return
    else:
        ctx.guild.voice_client.stop()
        await ctx.send("再生停止")

@piro3112bot.bot.command()
async def summon(ctx, channel_name = None):
    if(channel_name == None):
        if(ctx.author.voice == None):
            await ctx.send("チャンネルに繋ぐかチャンネルを指定するかしてください")
        elif (ctx.bot not in ctx.author.voice.channel.members):  
            if (ctx.guild.voice_client != None):
                await ctx.guild.voice_client.disconnect()              
            await ctx.author.voice.channel.connect()
        else:
            await ctx.send("もう接続されています")
    else:
        for channel in ctx.guild.voice_channels:
            if(channel.name == channel_name):
                if (ctx.bot not in channel.members):
                    if (ctx.guild.voice_client != None):
                        await ctx.guild.voice_client.disconnect()
                    await channel.connect()
                else:
                    await ctx.send("もう接続されています")
                return
        await ctx.send("チャンネルが見つかりませんでした")

@piro3112bot.bot.command()
async def disconnect(ctx):
    if (ctx.guild.voice_client == None):
        await ctx.send("接続されていません")
    else:
        await ctx.guild.voice_client.disconnect()
    return

@piro3112bot.bot.command()
async def play(ctx):
    await ctx.send("実装中")