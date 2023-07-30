import discord
import datetime
import pytz
import time
import requests
import asyncio
import random
import platform
import sys
import json
import threading
import gomashio
import animalotta_sim
from discord_slash import SlashCommand, SlashContext
from discord_slash.utils.manage_commands import create_option
from discord.ext import commands
from googletrans import Translator

#discord関連の変数
Intents = discord.Intents.default()
Intents.members = True
Intents.voice_states = True
Intents.reactions = True
Intents.guilds = True
bot = commands.Bot(command_prefix='z!', intents=Intents)
client = discord.Client(intents=Intents) 
#slash = SlashCommand(client, sync_commands=True)
slash = SlashCommand(client, sync_commands=False)

#その他の変数
semaphore = threading.BoundedSemaphore(value=2)

#サポート鯖リンク
support_guild = '[サポートサーバーに参加する](https://discord.gg/pFgBSt6MPX)'

#役職パネルの関数とか
def extract_message_id(url):
    import re
    pattern = r"\/(\d+)\/(\d+)\/(\d+)$"
    match = re.search(pattern, url)
    if match:
        message_id = int(match.group(3))
        return message_id
    else:
        return None

#スラッシュコマンド
@slash.slash(name="help", description="botのヘルプを表示します")
async def help(ctx: SlashContext):
    embed=discord.Embed(title="ハリネズミン！v2 (β2)", description="ハリネズミン！v2(β2)は、現在試験的に稼働中のbotです。\r基本的にこのbotはスラッシュコマンドからの動作になります。",color=0x00ff00)
    embed.add_field(name="削除・メッセージ編集ログ機能", value="「削除ログ」という名前のチャンネルを作成すると、メッセージの削除・編集ログが残るようになります。", inline=False)
    embed.add_field(name="ボイスチャンネル入退出ログ機能", value="「ボイスチャンネルログ」という名前のチャンネルを作成すると、サーバー内でボイスチャンネルへの入退出があった場合に通知します。", inline=False)
    embed.add_field(name="サポートサーバーのご案内", value="サポートサーバーでは、製作者に直接お問い合わせすることができます。\n[サポートサーバーに参加](https://discord.gg/pFgBSt6MPX)", inline=False)
    embed.add_field(name="git hubリポジトリ", value="ハリネズミン！v2のコードを見ることができます。\n[リポジトリを見る](https://github.com/animalotta0206/harine_zumin/)", inline=False)
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
                    rank = f"ここまで長かった…"
                await ctx.send(f"<@{message.author.id}>\n正解です！試行回数は{i}回でした！\n称号:「{rank}」")
                break
            elif guess >= 1001:
                await ctx.send(f"<@{message.author.id}>\n1000以下の数字で回答してください！")
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

@slash.slash(name="usercheck", description="ユーザ識別子から一意の文字列に変更されているかを確認できます。")
async def usercheck(ctx: SlashContext):
    original_response = await ctx.send("<a:b_sending:1108227693230702642>読み込み中です…")
    guild = client.get_guild(ctx.guild.id)  # サーバーIDを指定
    edit_id = 0
    noedit_id = 0
    bot_count = 0
    for member in guild.members:
        if member.bot:
            bot_count += 1
        if member.discriminator == "0":
            edit_id += 1
        else:
            noedit_id += 1
    noedit_id -= bot_count
    embed = discord.Embed(title=f"{ctx.guild.name}のユーザ識別子変更状況", description="識別子変更に関する情報は[こちらから](https://support.discord.com/hc/ja/articles/12620128861463-%E6%96%B0%E3%81%97%E3%81%84%E3%83%A6%E3%83%BC%E3%82%B6%E3%83%BC%E5%90%8D-%E8%A1%A8%E7%A4%BA%E3%81%95%E3%82%8C%E3%82%8B%E5%90%8D%E5%89%8D)ご確認ください。", color=0x387aff)
    embed.add_field(name="識別子変更済みユーザー数", value=f"{edit_id}", inline=False)
    embed.add_field(name="識別子変更がまだのユーザ数", value=f"{noedit_id}", inline=True)
    await original_response.edit(content="<:b_check:1043897762590236704>読み込みが完了しました。", embed=embed)

@slash.slash(name="share_discord_profile", description="あなたのDiscordプロフィールをほかのSNSで簡単に共有できるURLを生成します。")
async def share_discord_profile(ctx: SlashContext):
    await ctx.send(f"{ctx.author.mention}のDiscordプロフィールリンクはこちらです。\nhttps://discord.com/users/{ctx.author.id}")

@slash.slash(name="purge_message", description="最大2000件までのメッセージを削除できます。",)
async def purge_message(ctx: SlashContext, about: int):
    if ctx.author.guild_permissions.manage_messages:
        if about >= 2001:
            await ctx.send('メッセージの削除は2000件までに制限されています。')
            return
        try:
            target_channel = client.get_channel(ctx.channel.id)
            if about >= 500:
                w_message = await ctx.send(f'<a:b_sending:1108227693230702642>{about}件のメッセージを削除しています………\n>>> この処理には数分かかることがあります。\nこれ以降のメッセージは削除対象になりませんので、いつも通りチャットをすることができます。')    
            else:
                w_message = await ctx.send(f'<a:b_sending:1108227693230702642>{about}件のメッセージを削除しています………')
            deleted = await target_channel.purge(limit=about, before=discord.Object(id=w_message.id), bulk=bool(True))
            await w_message.edit(content=f'<:b_check:1043897762590236704>{len(deleted)}件のメッセージを削除しました。')
        except discord.Forbidden:
            await w_message.edit(content="Botに「メッセージの管理権限」がありません。\nBotの「メッセージの管理権限」を有効化してください。")
        except discord.HTTPException as e:
            embed=discord.Embed(description=f"例外処理されていないエラーが発生しました\n詳細:\n```\n{str(e)}\n```", color=0xff0000)
            embed.add_field(name="何度もエラー発生する場合は…", value="bot開発者の`anima_zumin_0206`までお知らせください。", inline=True)
            embed.add_field(name="サポートサーバーに参加してみませんか？", value=f"サポートサーバーではより迅速に対応できます。\n{support_guild}", inline=True)
            embed.timestamp = datetime.datetime.utcnow()
            await ctx.send(content=f'エラーが発生しました。\nここまで{len(deleted)}件のメッセージを削除しました。', embed=embed)
    else:
        await ctx.send(f"コマンド実行者に「メッセージの管理権限」が無いため、リクエストは拒否されました。")

@slash.slash(name='panel_create', description='役職パネルを作成します。', options=[
    {
      "name":'role',
      "description":"役職パネルに追加するロールを指定してください。",
      "type": 8,
      "required": True
    },
    {
        "name":'panel_title',
        "description":'パネルのタイトルを指定できます。',
        "type": 3,
        "required": True
    },
    {
        "name":'emoji',
        "description":"ロールの絵文字を追加します。",
        "type":3,
        "required": True
    }
    ])
async def panel_create(ctx: SlashContext, role: discord.Role, panel_title: str, emoji: str):
    if ctx.author.guild_permissions.manage_roles:
        m = await ctx.channel.send('<a:b_sending:1108227693230702642>役職パネルを作成しています………')
        embed = discord.Embed(title=panel_title)
        embed.add_field(name=emoji, value=f"<@&{role.id}>", inline=True)
        embed.set_footer(text=f'最終更新者:{ctx.author.name}')
        await m.add_reaction(f'{emoji}')
        await m.edit(content='ロールに対応する絵文字にリアクションするとロールを受け取ることができます。', embed=embed)
        reply = await ctx.send("役職パネルを作成しました！")
        await asyncio.sleep(3)
        await reply.delete()
    else:
        await ctx.send("ロールの管理権限を持っていないため実行できません。")

@slash.slash(name='panel_edit', description='役職パネルを編集します。', options=[
    {
        "name":"url",
        "description":"役職パネルのメッセージURLを入力してください。",
        "type": 3,
        "required": True
    },
    {
        "name":"title",
        "description":"パネルのタイトルを編集できます。",
        "type": 3,
        "required": True
    }
    ])
async def panel_edit(ctx: SlashContext, url: str, title: str):
    if ctx.author.guild_permissions.manage_roles:
        message_id = extract_message_id(url)
        channel = ctx.channel
        try:
            message = await channel.fetch_message(message_id)
        except discord.NotFound:
            await ctx.send("指定されたメッセージは見つかりませんでした。")
            return
        if message.author.id != client.user:
            if message.content == "ロールに対応する絵文字にリアクションするとロールを受け取ることができます。":
                existing_embed = message.embeds[0]
                existing_embed.title = title
                await message.edit(embed=existing_embed)
                m = await ctx.send("変更が完了しました。")
                await asyncio.sleep(5)
                await m.delete()
            else:
                await ctx.send("指定されたメッセージは役職パネルではありません。")
        else:
            await ctx.send("指定されたメッセージURLはbotのメッセージではないため利用できません。")
    else:
        await ctx.send("ロールの管理権限を持っていないため実行できません。")

@slash.slash(name="panel_add_role", description="役職パネルにロールを追加します(一度につき最大3つまで同時追加が可能です。)", options=[
    {
        "name":"url",
        "description":"役職を追加するパネルのメッセージURLを入力してください。",
        "type": 3,
        "required": True
    },
    {
        "name":"role1",
        "description":"追加する役職を入力",
        "type": 8,
        "required": True
    },
    {
        "name":"emoji1",
        "description":"役職に追加する絵文字を指定",
        "type": 3,
        "required": True
    },
        {
        "name":"role2",
        "description":"追加する役職を入力(2つめ)",
        "type": 8,
        "required": False
    },
    {
        "name":"emoji2",
        "description":"役職に追加する絵文字を指定(2つめ)",
        "type": 3,
        "required": False
    },
        {
        "name":"role3",
        "description":"追加する役職を入力(3つめ)",
        "type": 8,
        "required": False
    },
    {
        "name":"emoji3",
        "description":"役職に追加する絵文字を指定(3つめ)",
        "type": 3,
        "required": False
    },])
async def panel_add_role(ctx: SlashContext, url: str, role1: discord.Role, emoji1: str, role2: discord.Role = None, emoji2: str = None, role3: discord.Role = None, emoji3: str = None):
    if ctx.author.guild_permissions.manage_roles:
        m = await ctx.send("<a:b_sending:1108227693230702642>処理中…")
        message_id = extract_message_id(url)
        channel = ctx.channel
        try:
            message = await channel.fetch_message(message_id)
        except discord.NotFound:
            await m.edit("指定されたメッセージは見つかりませんでした。")
            return
        if message.author.id != client.user:
            if message.content == "ロールに対応する絵文字にリアクションするとロールを受け取ることができます。":
                existing_embed = message.embeds[0]
                if role3:
                    if emoji3:
                        if role2:
                            if emoji2:
                                fields = [
                                    {"name": emoji1, "value": f"<@&{role1.id}>", "inline": True},
                                    {"name": emoji2, "value": f"<@&{role2.id}>", "inline": True},
                                    {"name": emoji3, "value": f"<@&{role3.id}>", "inline": True},
                                ]
                            else:
                                await m.edit(content="エラー:値「emoji2」が指定されていません。")
                                return
                        else:
                            await m.edit(content="エラー:値「role2」が指定されていません。")
                            return
                    else:
                        await m.edit(content="エラー:値「emoji3」が指定されていません。")
                        return
                elif role2:
                    if emoji2:
                        fields = [
                                {"name": emoji1, "value": f"<@&{role1.id}>", "inline": True},
                                {"name": emoji2, "value": f"<@&{role2.id}>", "inline": True},
                                ]
                    else:
                        await m.edit(content="エラー:値「emoji2」が指定されていません。")
                        return
                else:
                  fields = [
                      {"name": emoji1, "value": f"<@&{role1.id}>", "inline": True},
                  ]

                for field in fields:
                    existing_embed.add_field(name=field["name"], value=field["value"], inline=field["inline"])
                    await message.add_reaction(field["name"])

                await message.edit(embed=existing_embed)
                await m.delete()
    else: 
        await ctx.send("ロールの管理権限がないため実行できません。")

@slash.slash(name="panel_remove_role", description="指定した役職を削除します。", options=[
    {
        "name":"url",
        "description":"パネルのメッセージURL",
        "type": 3,
        "required": True
    },
    {
        "name":"role",
        "description":"パネルから削除するロール",
        "type": 8,
        "required": True
    }])
async def panel_remove_role(ctx: SlashContext, url: str, role: discord.Role):
    if ctx.author.guild_permissions.manage_roles:
        m = await ctx.send("<a:b_sending:1108227693230702642>処理中…")
        message_id = extract_message_id(url)
        channel = ctx.channel
        try:
            message = await channel.fetch_message(message_id)
        except discord.NotFound:
            await m.edit(content="指定されたメッセージは見つかりませんでした。")
            return

        if message.author.id != client.user:
            if message.content == "ロールに対応する絵文字にリアクションするとロールを受け取ることができます。":
                embed = message.embeds[0]
                target_field_name = f"<@&{role.id}>"
                field_index = None  # 初期化を行う
                for index, field in enumerate(embed.fields):
                    if field.value == target_field_name:
                        emoji_name = field.name
                        field_index = index
                        break

                if field_index is not None:
                    embed.remove_field(field_index)
                    await message.remove_reaction(emoji_name, client.user)
                    await message.edit(embed=embed)
                    await m.delete()
                else:
                    await m.edit(content="指定したロールは役職パネルに存在しません。")
            else:
                await m.edit(content="指定したメッセージは役職パネルではありません。")
        else:
            await m.edit(content="指定されたメッセージはbotのメッセージではないため利用できません。")
    else:
        await m.edit(content="ロールの管理権限がないため実行できません。")

#メッセージ送信時
@client.event
async def on_message(message):
    if message.author.id == client.user.id:
        return
    
    if message.content.find('<@990987427818651648>') != -1:
      texts = [ #ランダムで返す文字列
      'ひどいズミン………',
      'すごくひどいズミン………'
      ]
      index = random.randint(0, len(texts) - 1)
      reply = texts[index]
      await message.reply(reply)

    if message.channel.name in "逆翻訳チャンネル":
        if message.author.id == 1:
            if message.reference:
                return
            await message.author.send("現在、あなたは「**予期しないBOTの動作を意図的に複数回誘発した**」として、利用制限を受けております。\n制限の詳細については、`anima_zumin_0206`までお願いします。")
            return
        channelid = message.channel.id
        channel = client.get_channel(channelid)
        is_nsfw = channel.is_nsfw()
        max_attempts = 4  # 最大再試行回数
        attempt = 0
        if message.author.bot:
            return
        if message.reference:
            return
        wait_message = await message.reply("<a:b_sending:1108227693230702642>読み込み中です…\nこの読み込みには数分かかることがあります…。")
        if is_nsfw is False:
            with open('harine_zumin/ward_filter.json', 'r') as f:
                ward_f = json.load(f)
            if str(ward_f).find(message.content) != -1:
                await wait_message.edit(content="不適切な単語を検出しました。翻訳を中止します。\nワードフィルタリングを無効化するには、NSFWチャンネルをご利用ください。")
                return
        while attempt < max_attempts:
            async with message.channel.typing():
                try:
                    text1 = message.content
                    translator = Translator()
                    translated1 = translator.translate(text1, dest='ko')
                    await wait_message.edit(content=f"処理中…\nSTEP (1/5)\nTry ({attempt+1}/{max_attempts-1})")
                    translated2 = translator.translate(translated1.text, dest='ar')
                    await wait_message.edit(content=f"処理中…\nSTEP (2/5)\nTry ({attempt+1}/{max_attempts-1})")
                    translated3 = translator.translate(translated2.text, dest='ja')
                    await wait_message.edit(content=f"処理中…\nSTEP (3/5)\nTry ({attempt+1}/{max_attempts-1})")
                    translated4 = translator.translate(translated3.text, dest='sd')
                    await wait_message.edit(content=f"処理中…\nSTEP (4/5)\nTry ({attempt+1}/{max_attempts-1})")
                    translated5 = translator.translate(translated4.text, dest='en')
                    await wait_message.edit(content=f"<a:b_sending:1108227693230702642>しばらくお待ち下さい…\n日本語に戻しています…\nSTEP (5/5)\nTry ({attempt+1}/{max_attempts-1})")
                    translated11 = translator.translate(translated5.text, dest='ja')
                except Exception as e:
                    if attempt == 0:
                        e_message = f"エラーが発生しました。5秒後に再試行します…<a:b_restart:1126125262430552064>\nTry ({attempt+1}/{max_attempts-1})"
                        slep = 5
                        #エラーログをハリネズミン！の巣！へ送信する処理
                        channel = client.get_channel(1118756012351029358)
                        embed=discord.Embed(description=f"例外処理されていないエラーが発生しました。\n詳細:\n```\n{str(e)}\n```", color=0xff0000)
                        embed.add_field(name="エラーが発生したサーバー", value=f"「{message.guild.name}」\nGuild ID:({message.guild.id})", inline=True)
                        embed.timestamp = datetime.datetime.utcnow()
                        await channel.send(content=f"逆翻訳機能のエラー\n処理試行回数:({attempt+1}/{max_attempts-1})", embed=embed)
                        #エラーログの処理はここまで
                    elif attempt == 1:
                        e_message = f"エラーが発生しました。10秒後に再試行します…<a:b_restart:1126125262430552064>\nTry ({attempt+1}/{max_attempts-1})"
                        slep = 10
                        #エラーログをハリネズミン！の巣！へ送信する処理
                        channel = client.get_channel(1118756012351029358)
                        embed=discord.Embed(description=f"例外処理されていないエラーが発生しました。\n詳細:\n```\n{str(e)}\n```", color=0xff0000)
                        embed.add_field(name="エラーが発生したサーバー", value=f"「{message.guild.name}」\nGuild ID:({message.guild.id})", inline=True)
                        embed.timestamp = datetime.datetime.utcnow()
                        await channel.send(content=f"逆翻訳機能のエラー\n処理試行回数:({attempt+1}/{max_attempts-1})", embed=embed)
                        #エラーログの処理はここまで
                    elif attempt == 2:
                        e_message = f"エラーが発生しました。15秒後に再試行します…<a:b_restart:1126125262430552064>\nTry ({attempt+1}/{max_attempts-1})"
                        slep = 15
                        #エラーログをハリネズミン！の巣！へ送信する処理
                        channel = client.get_channel(1118756012351029358)
                        embed=discord.Embed(description=f"例外処理されていないエラーが発生しました。\n詳細:\n```\n{str(e)}\n```", color=0xff0000)
                        embed.add_field(name="エラーが発生したサーバー", value=f"「{message.guild.name}」\nGuild ID:({message.guild.id})", inline=True)
                        embed.timestamp = datetime.datetime.utcnow()
                        await channel.send(content=f"逆翻訳機能のエラー\n処理試行回数:({attempt+1}/{max_attempts-1})", embed=embed)
                        #エラーログの処理はここまで
                    else:
                        e_message = f"最大試行回数に到達しました。処理を中断し、エラー情報を収集しています…<a:b_restart:1126125262430552064>"
                        slep = 3
                        #エラーログをハリネズミン！の巣！へ送信する処理
                        channel = client.get_channel(1118756012351029358)
                        embed=discord.Embed(description=f"例外処理されていないエラーが発生しました。\n詳細:\n```\n{str(e)}\n```", color=0xff0000)
                        embed.add_field(name="エラーが発生したサーバー", value=f"「{message.guild.name}」\nGuild ID:({message.guild.id})", inline=True)
                        embed.timestamp = datetime.datetime.utcnow()
                        await channel.send(content=f"逆翻訳機能のエラー\n処理に失敗しました。", embed=embed)
                        #エラーログの処理はここまで
                    await wait_message.edit(content=e_message)
                    attempt += 1
                    time.sleep(slep)
                    e_text = str(e)
                else:
                    #翻訳が正常に終了したときの処理
                    if is_nsfw is False:
                        if str(ward_f).find(str(translated11.text)) != -1:
                            await wait_message.edit(content="不適切な翻訳を検出しました。\nワードフィルタリングを無効化するには、NSFWチャンネルをご利用ください。")
                            return
                        else:
                            await wait_message.edit(content=translated11.text)
                    else:
                        await wait_message.edit(content=translated11.text)
                    break
        else:
            embed=discord.Embed(description=f"例外処理されていないエラーが発生しました\n詳細:\n```\n{e_text}\n```", color=0xff0000)
            embed.add_field(name="何度もエラー発生する場合は…", value="bot開発者の`anima_zumin_0206`までお知らせください。", inline=True)
            embed.add_field(name="サポートサーバーに参加してみませんか？", value=f"サポートサーバーではより迅速に対応できます。\n{support_guild}", inline=True)
            embed.timestamp = datetime.datetime.utcnow()
            await wait_message.edit(content="<:b_error:1041554270958387220>transrate is Faild", embed=embed)
    elif message.channel.id == '1127941083855343636':
        
        text = message.content
        translator = Translator()
        translated = translator.translate(text, dest='en')
        await message.reply(translated)
    else:
        return

#ボイスチャンネル関連
@client.event
async def on_voice_state_update(member, before, after):
    # 参��した場合
    if not before.channel and after.channel:
        # ログに出力するメッセージ
        message = f'<@{member.id}>が<#{after.channel.id}>に参加しました。'
        embed=discord.Embed(description=message,color=0x009dff)
        embed.set_author(name=f"{member.name}",icon_url="https://media.discordapp.net/avatars/{}/{}.png?size=1024".format(member.id,member.avatar))
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
        embed.set_author(name=f"{member.name}",icon_url="https://media.discordapp.net/avatars/{}/{}.png?size=1024".format(member.id,member.avatar))
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
        embed.set_author(name=f"{member.name}", icon_url="https://media.discordapp.net/avatars/{}/{}.png?size=1024".format(member.id,member.avatar))
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
    if channel is not None:
    # 削除されたメッセージの情報を取得
        embed = discord.Embed(title="メッセージ削除", color=discord.Color.red())
        embed.add_field(name="チャンネル", value=message.channel.mention, inline=False)
        embed.add_field(name="メッセージ内容", value=message.content, inline=False)
        embed.set_author(name=f"{message.author.name}",icon_url="https://media.discordapp.net/avatars/{}/{}.png?size=1024".format(message.author.id, message.author.avatar))
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
                              description=f"[元のメッセージを見る](https://discord.com/channels/{after.guild.id}/{after.channel.id}/{after.id})",
                              color=0x00ff00)
        embed.add_field(name="チャンネル", value=after.channel.mention, inline=False)
        embed.add_field(name="編集前のメッセージ", value=before.content, inline=False)
        embed.add_field(name="編集後のメッセージ", value=after.content, inline=False)
        embed.set_author(name=f"{after.author.name}",icon_url="https://media.discordapp.net/avatars/{}/{}.png?size=1024".format(after.author.id, after.author.avatar))
        embed.set_footer(text="{} / UserID:{}".format(after.guild.name, after.author.id),icon_url="https://media.discordapp.net/icons/{}/{}.png?size=1024".format(after.guild.id, after.guild.icon))
        embed.timestamp = datetime.datetime.utcnow()
        await channel.send(embed=embed)

#サーバーログ
@client.event
async def on_guild_join(guild):
    system_channel = guild.system_channel
    if system_channel is not None:
        message = "はじめまして！ハリネズミン！です！"
        embed=discord.Embed(title="ハリネズミン！v2 ", description="ここでは、botの基本的な機能について軽く紹介します。\nまたこの内容は</help:1082678201194664117>でもご確認いただけます。", color=0x00ff04)
        embed.add_field(name="削除・メッセージ編集ログ機能", value="「削除ログ」という名前のチャンネルを作成すると、メッセージの削除・編集ログが残るようになります。", inline=False)
        embed.add_field(name="ボイスチャンネル入退出ログ機能", value="「ボイスチャンネルログ」という名前のチャンネルを作成すると、サーバー内でボイスチャンネルへの入退出があった場合に通知します。", inline=False)
        embed.add_field(name="サポートサーバーのご案内", value="サポートサーバーでは、製作者に直接お問い合わせすることができます。\n[サポートサーバーに参加](https://discord.gg/pFgBSt6MPX)", inline=False)
        await system_channel.send(message, embed=embed)
    channel = client.get_channel(1108597602766827561)
    embed=discord.Embed(title="新規bot参加", description=f"Botが「{guild.name}」に参加しました。", color=0x00ffe1)
    embed.set_footer(text=f"GuildID:{guild.id}", icon_url=guild.icon_url)
    embed.timestamp = datetime.datetime.utcnow()
    await channel.send(embed=embed)

#役職パネル用リアクションが追加されたときのイベントハンドラ
@client.event
async def on_raw_reaction_add(payload):
    if payload.user_id == client.user.id:
        return
    channel = client.get_channel(payload.channel_id)
    message = await channel.fetch_message(payload.message_id)
    try:
        if message.author.id == client.user.id:
            if message.content == 'ロールに対応する絵文字にリアクションするとロールを受け取ることができます。':
                embed = message.embeds[0]
                fields = embed.fields
                field_value = None 
                for field in fields:
                    if str(field.name) == str(payload.emoji):
                        field_name = field.name
                        field_value = field.value
                        break
                if field_value is not None:
                    role_id = ''.join(char for char in field_value if char.isdigit())
                    guild = client.get_guild(payload.guild_id)
                    role = guild.get_role(int(role_id))
                    member = payload.member
                    if role in member.roles:
                        emoji = payload.emoji
                        await message.remove_reaction(emoji, member)
                        await member.remove_roles(role)
                        channel = client.get_channel(payload.channel_id)
                        embed = discord.Embed(description=f"ロール<@&{role_id}>を解除しました。")
                        m = await channel.send(f"<@{payload.user_id}>", embed=embed)
                        await asyncio.sleep(5)
                        await m.delete()
                    else:
                        emoji = payload.emoji
                        await message.remove_reaction(emoji, member)
                        await member.add_roles(role)
                        channel = client.get_channel(payload.channel_id)
                        embed = discord.Embed(description=f"ロール<@&{role_id}>を付与しました。")
                        m = await channel.send(f"<@{payload.user_id}>", embed=embed)
                        await asyncio.sleep(5)
                        await m.delete()
                else:
                    member = payload.member
                    emoji = payload.emoji
                    await message.remove_reaction(emoji, member)
    except:
        embed=discord.Embed(description="ロールの付与でエラーが発生しました。\n一時的なエラーの可能性もありますので再度お試しください。")
        m = await channel.send(f"<@{payload.user_id}>", embed=embed)
        await asyncio.sleep(5)
        await m.delete()

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

client.run(TOKEN)
