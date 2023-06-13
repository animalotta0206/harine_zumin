import discord
import datetime
import pytz
import time
import requests
import ffmpeg
import asyncio
import random
import platform
import sys
import gomashio
from PIL import Image
from discord_slash import SlashCommand, SlashContext
from discord_slash.utils.manage_commands import create_option
from discord.ext import commands

#discord関連の変数
Intents = discord.Intents.default()
Intents.members = True
Intents.voice_states = True
Intents.reactions = True
Intents.guilds = True
bot = commands.Bot(command_prefix='z!')
client = discord.Client(intents=Intents) 
#slash = SlashCommand(client, sync_commands=True)
slash = SlashCommand(client, sync_commands=False)

#スラッシュコマンド
@slash.slash(name="help", description="botのヘルプを表示します")
async def help(ctx: SlashContext):
    embed=discord.Embed(title="ハリネズミン！v2 (β2)", description="ハリネズミン！v2(β2)は、現在試験的に稼働中のbotです。\r基本的にこのbotはスラッシュコマンドからの動作になります。",color=0x00ff00)
    embed.add_field(name="削除・メッセージ編集ログ機能", value="「削除ログ」という名前のチャンネルを作成すると、メッセージの削除・編集ログが残るようになります。", inline=False)
    embed.add_field(name="ボイスチャンネル入退出ログ機能", value="「ボイスチャンネルログ」という名前のチャンネルを作成すると、サーバー内でボイスチャンネルへの入退出があった場合に通知します。", inline=False)
    embed.add_field(name="サポートサーバーのご案内", value="サポートサーバーでは、製作者に直接お問い合わせすることができます。\n[サポートサーバーに参加](https://discord.gg/pFgBSt6MPX)", inline=False)
    await ctx.send(embed=embed)

@slash.slash(name="taiman", description="怠慢やね画像を送信します。")
async def taiman(ctx: SlashContext):
    embed = discord.Embed(title="怠慢やね😅",color=0x04ff00)
    embed.set_image(url="https://cdn.discordapp.com/attachments/992091661519827074/992091785331490826/20210726_212048.jpg")
    await ctx.send(embed=embed)

@slash.slash(name="bareta", description="ばれたかを送信します。")
async def bareta(ctx: SlashContext):
    embed = discord.Embed(title="バレたか😆",color=0x04ff00)
    embed.set_image(url="https://cdn.discordapp.com/attachments/992091661519827074/992091784761053240/20210726_212042.jpg")
    await ctx.send(embed=embed)
    
@slash.slash(name="tweet", description="ツイートを参考にしない😅")
async def tweet(ctx: SlashContext):
    embed = discord.Embed(title="ツイートを参考にしない😅",color=0x04ff00)
    embed.set_image(url="https://cdn.discordapp.com/attachments/992091661519827074/992091784521990164/20210726_212045.jpg")
    await ctx.send(embed=embed)
    
@slash.slash(name="goodnight", description="おやすみなさい画像を送信します。")
async def goodnight(ctx: SlashContext):
    embed = discord.Embed(title="おやすみなさい😴",color=0x04ff00)
    embed.set_image(url="https://cdn.discordapp.com/attachments/992091661519827074/992091785117585448/20210726_212039.jpg")
    await ctx.send(embed=embed)
    
@slash.slash(name="omikuji", description="おみくじが引けます。不正できます。")
async def omikuji(ctx: SlashContext):
     texts = [ #ランダムで返す文字列
      '大吉！すごいズミン！',
      '中吉！がんばったズミン！',
      '中吉！がんばったズミン！',
      '中吉！がんばったズミン！',
      '小吉！まぁまぁの結果ズミン！',
      '小吉！まぁまぁの結果ズミン！',
      '小吉！まぁまぁの結果ズミン！',
      '小吉！まぁまぁの結果ズミン！',
      '小吉！まぁまぁの結果ズミン！',
      '不正吉！不正は絶対ダメズミン！',
      ]
     index = random.randint(0, len(texts) - 1)
     text = texts[index]
     await ctx.send(text)

@slash.slash(name="number_game_easy", description="数当てゲームができます。成功率は1/100です。")
async def number_game_easy(ctx: SlashContext):
    answer = random.randint(1, 100)
    i = 0

    await ctx.send("数当てゲーム！\n1〜100の範囲の数字を当ててみましょう！\n続行するには1〜100の範囲で数字を送信してください。")

    def check(m):
        return m.author == ctx.author and m.channel == ctx.channel

    while True:
        try:
            message = await client.wait_for('message', check=check, timeout=30)  # メッセージの受け取り待機
            guess = int(message.content)
            if guess == answer:
                i += 1
                if i == 1:
                    rank = "数当てゲーム神"
                elif i <= 5:
                    rank = "数当てゲーム上級者"
                elif i <= 10:
                    rank = "数当てゲーム中級者"
                elif i <= 15:
                    rank = "数当てゲーム初級者"
                else:
                    rank = "数当てゲーム超初心者"
                await ctx.send(f"<@{message.author.id}>\n正解です！試行回数は{i}回でした！\n称号:「{rank}」")
                break
            elif guess >= 101:
                await ctx.send(f"<@{message.author.id}>\n100以下の数字で回答してください！")
            elif guess > answer:
                i += 1
                await ctx.send(f"<@{message.author.id}>\n残念！\nヒントはこれよりも小さい数です！")
            else:
                i += 1
                await ctx.send(f"<@{message.author.id}>\n残念！\nヒントはこれよりも大きい数です！")
        except asyncio.TimeoutError:
            await ctx.send(f"<@{message.author.id}>\nタイムアウトしました。もう一度やり直してください。")
            break
        except Exception as e:
            embed=discord.Embed(description=f"エラー出力\n```\n{str(e)}\n```", color=0xff0000)
            await ctx.send(f"<@{message.author.id}>\nエラーが発生しました。\nもう一度やり直してください。", embed=embed)
            break

@slash.slash(name="number_game_hard", description="(1発モード)数当てゲームができます。成功率は1/100です。")
async def number_game_hard(ctx: SlashContext):
    answer = random.randint(1, 100)

    await ctx.send("数当てゲーム！「一発勝負モード」\n1〜100の範囲の数字を当ててみましょう！チャンスは1回限り！\n続行するには1〜100の範囲で数字を送信してください。")

    def check(m):
        return m.author == ctx.author and m.channel == ctx.channel

    while True:
        try:
            message = await client.wait_for('message', check=check, timeout=30)  # メッセージの受け取り待機
            guess = int(message.content)
            if guess == answer:
                await ctx.send(f"<@{message.author.id}>正解です！おめでとうございます！")
                break
            else:
                await ctx.send(f"<@{message.author.id}>残念！不正解！\n今回の正解は「{answer}」でした。")
                break
        except asyncio.TimeoutError:
            await ctx.send(f"<@{message.author.id}>タイムアウトしました。もう一度やり直してください。")
            break
        except Exception as e:
            embed=discord.Embed(description=f"エラー出力\n```\n{str(e)}\n```", color=0xff0000)
            await ctx.send(f"<@{message.author.id}>\nエラーが発生しました。\nもう一度やり直してください。", embed=embed)
            break

@slash.slash(name="number_game_expert", description="数当てゲームができます(難易度エキスパート)。成功率は1/1000です。")
async def number_game_expert(ctx: SlashContext):
    answer = random.randint(1, 1000)
    i = 0

    await ctx.send("数当てゲーム！\n1〜1000の範囲の数字を当ててみましょう！\n続行するには1〜1000の範囲で数字を送信してください。")

    def check(m):
        return m.author == ctx.author and m.channel == ctx.channel

    while True:
        try:
            message = await client.wait_for('message', check=check, timeout=30)  # メッセージの受け取り待機
            guess = int(message.content)
            if guess == answer:
                i += 1
                if i == 1:
                    rank = "数当てゲームを極めし神-Legend of number-"
                elif i <= 10:
                    rank = "ド派手に数当てゲームになってみた！"
                elif i <= 20:
                    rank = "下積み時代辛い時も、諦めそうな時も、数当てゲームをやればすぐ元気になれた。"
                elif i <= 50:
                    rank = "数当てゲーム先生"
                else:
                    rank = "数当てゲーム凡人"
                await ctx.send(f"<@{message.author.id}>\n正解です！試行回数は{i}回でした！\n称号:「{rank}」")
                break
            elif guess >= 1001:
                await ctx.send(f"<@{message.author.id}>\n100以下の数字で回答してください！")
            elif guess > answer:
                i += 1
                await ctx.send(f"<@{message.author.id}>\n残念！\nヒントはこれよりも小さい数です！")
            else:
                i += 1
                await ctx.send(f"<@{message.author.id}>\n残念！\nヒントはこれよりも大きい数です！")
        except asyncio.TimeoutError:
            await ctx.send(f"<@{message.author.id}>\nタイムアウトしました。もう一度やり直してください。")
            break
        except Exception as e:
            embed=discord.Embed(description=f"エラー出力\n```\n{str(e)}\n```", color=0xff0000)
            await ctx.send(f"<@{message.author.id}>\nエラーが発生しました。\nもう一度やり直してください。", embed=embed)
            break

@slash.slash(name="number_game_Worlds_end", description="数当てゲームができます。成功率は1/1000です。答えるたびに回答が変わります。")
async def number_game_Worlds_end(ctx: SlashContext):
    i = 0

    await ctx.send("数当てゲーム！(難易度MAX)\n1〜1000の範囲の数字を当ててみましょう！\n毎回答えが変わる鬼畜仕様となっております。")

    def check(m):
        return m.author == ctx.author and m.channel == ctx.channel

    while True:
        try:
            answer = random.randint(1, 1000)
            message = await client.wait_for('message', check=check, timeout=30)  # メッセージの受け取り待機
            guess = int(message.content)
            if guess == answer:
                i += 1
                if i == 1:
                    rank = "もしかしたら超能力者の才能が自分にはあるのかもしれない…"
                elif i <= 10:
                    rank = "1/1000なんてちょろかった"
                elif i <= 50:
                    rank = "確率の収束ッ！"
                elif i <= 100:
                    rank = "試行回数って大事"
                elif i <= 200:
                    rank = "変数`answer`君…どうして君はそんなに動きたがるんだ…！じっとしてくれ！！！"
                elif i <= 350:
                    rank = "```py\nanswer = random.randint(1, 1000)\nmessage = await client.wait_for('message', check=check, timeout=30)\nguess = int(message.content)\n```"
                else:
                    rank = f"ここまで…{i}回…長かった…"
                await ctx.send(f"<@{message.author.id}>\n正解です！試行回数は{i}回でした！\n称号:「{rank}」")
                break
            elif guess >= 101:
                await ctx.send(f"<@{message.author.id}>\n100以下の数字で回答してください！")
            elif guess > answer:
                i += 1
                await ctx.send(f"<@{message.author.id}>\n残念！\n答えが変わりました！")
            else:
                i += 1
                await ctx.send(f"<@{message.author.id}>\n残念！\n答えが変わりました！")
        except asyncio.TimeoutError:
            await ctx.send(f"<@{message.author.id}>\nタイムアウトしました。もう一度やり直してください。")
            break
        except Exception as e:
            embed=discord.Embed(description=f"エラー出力\n```\n{str(e)}\n```", color=0xff0000)
            await ctx.send(f"<@{message.author.id}>\nエラーが発生しました。\nもう一度やり直してください。", embed=embed)
            break

@slash.slash(name="oumu", 
             description="オウム返しします。", 
             options=[
                 create_option(
                     name="say",
                     description="改行はたぶんできません。",
                     option_type=3,
                     required=True
                 ),
             ])
async def oumu(ctx: SlashContext, say: str):
     await ctx.send(f"{say}")
     
@slash.slash(name="ping",description="botの反応速度を測定できます。")
async def ping(ctx: SlashContext):
    # Ping値を秒単位で取得
    raw_ping = client.latency
    # ミリ秒に変換して丸める
    ping = round(raw_ping * 1000)
    embed=discord.Embed(title="Ping!", color=0x00ff00)
    embed.add_field(name="Pong!🏓", value=f'{ping}ms', inline=False)
    await ctx.send(embed=embed)
    
@slash.slash(name="reminder_set", description="指定した時刻に、指定したメッセージを予約送信することができます。", options=[
    {
        "name": "time",
        "description": "2023-01-01 12:00の24時間形式で指定してください。",
        "type": 3,
        "required": True
    },
    {
        "name": "message",
        "description": "予約送信したい文章を入力してください。(改行不可)",
        "type": 3,
        "required": True
    }
])
async def reminder_set(ctx: SlashContext, time: str, message: str):
    
    jst = pytz.timezone('Asia/Tokyo')
    target_time = datetime.datetime.strptime(time, '%Y-%m-%d %H:%M')
    target_time = jst.localize(target_time)
    now = datetime.datetime.now(jst)
    await ctx.send("送信予約が完了しました！")
    sleep_time = (target_time - now).total_seconds()
    await discord.utils.sleep_until(target_time)
    await ctx.channel.send(message)
    
@slash.slash(name="bot_info",description="botの情報を表示します。")
async def bot_info(ctx: SlashContext):

    num_of_servers = len(client.guilds)

    embed=discord.Embed(title="ハリネズミン！v2 bot info", color=0x00fa1d)
    embed.set_author(name="ハリネズミン！v2 #0624", icon_url="https://cdn.discordapp.com/avatars/990987427818651648/708788930a3cf8dd9e70349f47a110c6.png?size=4096")
    embed.add_field(name="Python バージョン:", value=sys.version, inline=True)
    embed.add_field(name="OS:", value=f"{platform.system()}\n{platform.release()}\n{platform.version()}", inline=True)
    embed.add_field(name="プロセッサー情報:", value=platform.processor(), inline=True)
    embed.add_field(name="所属しているサーバーの数:", value=num_of_servers, inline=True)
    await ctx.send(embed=embed)
    
@slash.slash(name="userinfo", description="ユーザー情報を取得します")
async def userinfo(ctx: SlashContext, member: discord.Member):
    embed = discord.Embed(title="ユーザー情報", description=member.mention, color=member.color)
    embed.add_field(name="ユーザー名", value=member.name, inline=True)
    embed.add_field(name="ニックネーム", value=member.nick, inline=True)
    embed.add_field(name="ID", value=member.id, inline=True)
    embed.add_field(name="サーバー参加日時", value=member.joined_at.strftime("%Y-%m-%d %H:%M:%S"), inline=True)
    embed.add_field(name="アカウント作成日時", value=member.created_at.strftime("%Y-%m-%d %H:%M:%S"), inline=True)
    embed.set_thumbnail(url=member.avatar_url)
    await ctx.send(embed=embed)
    
#メッセージ送信時
@client.event
async def on_message(message):
    if message.author.bot:#BOTの場合は何もせず終了
     return
    if message.content.find('<@990987427818651648>') != -1:
      texts = [ #ランダムで返す文字列
      'ひどいズミン………',
      'すごくひどいズミン………'
      ]
      index = random.randint(0, len(texts) - 1)
      reply = texts[index]
      await message.channel.send(reply)
    if message.content == 'ぱとぇvsKONAMI':
     await message.channel.send("ただいまより、「株式会社ぱとえ」🆚「株式会社コナミアミューズメント」の裁判を開廷します。\rLet's Start!")
     await asyncio.sleep(10)
     await message.channel.send("裁判の結果が出ました！\r運命やいかに………")
     rand1 = [
         '株式会社コナミアミューズメント',
         '株式会社コナミアミューズメント',
         '株式会社コナミアミューズメント',
         '株式会社コナミアミューズメント',
         '株式会社コナミアミューズメント',
         '株式会社コナミアミューズメント',
         '株式会社コナミアミューズメント',
         '株式会社コナミアミューズメント',
         '株式会社コナミアミューズメント',
         '株式会社ぱとえ']
     index = random.randint(0, len(rand1) - 1)
     text1 = rand1[index] 
     async with message.channel.typing():
         await asyncio.sleep(5)
     await message.channel.send(f"Winner:「{text1}」\r対戦ありがとうございました。")
    if message.content.find("台パン" ) != -1:
     await message.channel.send("台パンだめ、ぜったい")
     print (f"ユーザー:{message.author.name}\n台パンコマンドが実行されました。\n-------------------------------")
    if message.content == "z!join":
        if message.author.voice is None or message.author.voice.channel is None:
            await message.channel.send("あなたはボイスチャンネルに接続していません。")
            return
        9# ボイスチャンネルに接続する
        await message.author.voice.channel.connect()


#ボイスチャンネル関連
@client.event
async def on_voice_state_update(member, before, after):
    # 参加した場合
    if not before.channel and after.channel:
        # ログに出力するメッセージ
        message = f'<@{member.id}>が<#{after.channel.id}>に参加しました。'
        embed=discord.Embed(description=message,color=0x009dff)
        embed.set_author(name="{}#{}".format(member.name, member.discriminator),icon_url="https://media.discordapp.net/avatars/{}/{}.png?size=1024".format(member.id,member.avatar))
        embed.set_footer(text=f"ID:{member.id}")
        embed.timestamp = datetime.datetime.utcnow()
        # テキストチャンネルを取得
        channel = discord.utils.get(member.guild.text_channels, name='ボイスチャンネルログ')
        if channel is not None:
            # ログをテキストチャンネルに送信
            await channel.send(embed=embed)

    # 退出した場合
    elif before.channel and not after.channel:
        # ログに出力するメッセージ
        message = f'<@{member.id}>が<#{before.channel.id}>から退出しました。'
        embed=discord.Embed(description=message,color=0xff0000)
        embed.set_author(name="{}#{}".format(member.name, member.discriminator),icon_url="https://media.discordapp.net/avatars/{}/{}.png?size=1024".format(member.id,member.avatar))
        embed.set_footer(text=f"ID:{member.id}")
        embed.timestamp = datetime.datetime.utcnow()
        # テキストチャンネルを取得
        channel = discord.utils.get(member.guild.text_channels, name='ボイスチャンネルログ')
        if channel is not None:
            # ログをテキストチャンネルに送信
            await channel.send(embed=embed)
            return
    if before.channel and after.channel and before.channel != after.channel:
        # ボイスチャンネルから移動した場合
        message = f'<@{member.id}>が\n<#{before.channel.id}>から<#{after.channel.id}>へ移動しました。'
        embed=discord.Embed(description=message,color=0x00ff00)
        embed.set_author(name="{}#{}".format(member.name, member.discriminator),icon_url="https://media.discordapp.net/avatars/{}/{}.png?size=1024".format(member.id,member.avatar))
        embed.set_footer(text=f"ID:{member.id}")
        embed.timestamp = datetime.datetime.utcnow()
        channel = discord.utils.get(member.guild.text_channels, name='ボイスチャンネルログ')
        if channel is not None:
            # ログをテキストチャンネルに送信
            await channel.send(embed=embed)
            return

#メッセージ削除
@client.event
async def on_message_delete(message):
    # メッセージを削除したユーザーがボットの場合は無視
    if message.author.bot:
        return

    # 削除ログチャンネルを取得
    channel = discord.utils.get(message.guild.channels, name="削除ログ")

    # 削除されたメッセージの情報を取得
    embed = discord.Embed(title="メッセージ削除", color=discord.Color.red())
    embed.add_field(name="チャンネル", value=message.channel.mention, inline=False)
    embed.add_field(name="メッセージ内容", value=message.content, inline=False)
    embed.set_author(name="{}#{}".format(message.author.name, message.author.discriminator),icon_url="https://media.discordapp.net/avatars/{}/{}.png?size=1024".format(message.author.id, message.author.avatar))
    embed.set_footer(text="{} / UserID:{}".format(message.guild.name, message.author.id),icon_url="https://media.discordapp.net/icons/{}/{}.png?size=1024".format(message.guild.id, message.guild.icon))
    embed.timestamp = datetime.datetime.utcnow()

    # 削除ログにメッセージを送信
    await channel.send(embed=embed)
    
#メッセージ編集
@client.event
async def on_message_edit(before, after):
    if after.author.bot:
        return
    if after.content == before.content:
        return
    channel = discord.utils.get(after.guild.channels, name="削除ログ")
    if channel is not None:
        embed = discord.Embed(title="メッセージ編集",
                              color=0x00ff00)
        embed.add_field(name="チャンネル", value=after.channel.mention, inline=False)
        embed.add_field(name="編集前のメッセージ", value=before.content, inline=False)
        embed.add_field(name="編集後のメッセージ", value=after.content, inline=False)
        embed.set_author(name="{}#{}".format(after.author.name, after.author.discriminator),icon_url="https://media.discordapp.net/avatars/{}/{}.png?size=1024".format(after.author.id, after.author.avatar))
        embed.set_footer(text="{} / UserID:{}".format(after.guild.name, after.author.id),icon_url="https://media.discordapp.net/icons/{}/{}.png?size=1024".format(after.guild.id, after.guild.icon))
        embed.timestamp = datetime.datetime.utcnow()
        await channel.send(embed=embed)

#サーバーログ
@client.event
async def on_guild_join(guild):
    channel = client.get_channel(1108597602766827561)
    embed=discord.Embed(title="新規bot参加", description=f"Botが「{guild.name}」に参加しました。", color=0x00ffe1)
    embed.set_footer(text=f"GuildID:{guild.id}", icon_url=guild.icon_url)
    embed.timestamp = datetime.datetime.utcnow()
    await channel.send(embed=embed)

#起動時処理
@client.event
async def on_ready():
    game = discord.Game(f'アニマロッタ 夢のアニマランド')
    await client.change_presence(status=discord.Status.online, activity=game)
    print('ログインしました')
    print('------')
    print(client.user.name)  # Botの名前
    print(discord.__version__)  # discord.pyのバージョン
    print('------')
    
client.run("TOKEN here")
