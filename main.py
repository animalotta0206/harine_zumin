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
import animalotta_sim
from discord import app_commands
from discord_buttons_plugin import *
from googletrans import Translator

#discord関連の変数
Intents = discord.Intents.all()
client = discord.Client(intents=Intents)
tree = app_commands.CommandTree(client)
#コマンド同期の設定
sync_command = False

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
    
#コンテキストメニューのテスト
@tree.context_menu()
async def user_info(interaction: discord.Interaction, member: discord.Member):
    embed=discord.Embed(color=member.color)
    embed.set_author(name=member.name)
    embed.set_thumbnail(url=member.avatar.url)
    embed.add_field(name='アカウント登録日', value=member.created_at, inline=True)
    embed.add_field(name='サーバー参加日時', value=member.joined_at, inline=True)
    embed.add_field(name='サーバーブースト開始日', value=member.premium_since, inline=True)
    embed.add_field(name='アカウントがSPAMとして認証されているか', value=f'`{member.public_flags.spammer}`', inline=True)
    embed.add_field(name='BOTアカウントとしてフラグされているか', value=f'`{member.bot}`', inline=True)
    await interaction.response.send_message(embed=embed)

#スラッシュコマンド
@tree.command(name="help", description="botのヘルプを表示します")
async def help(ctx: discord.Interaction):
    embed=discord.Embed(title="ハリネズミン！v2 (β2)", description="ハリネズミン！v2(β2)は、現在試験的に稼働中のbotです。\r基本的にこのbotはスラッシュコマンドからの動作になります。",color=0x00ff00)
    embed.add_field(name="削除・メッセージ編集ログ機能", value="「削除ログ」という名前のチャンネルを作成すると、メッセージの削除・編集ログが残るようになります。", inline=False)
    embed.add_field(name="ボイスチャンネル入退出ログ機能", value="「ボイスチャンネルログ」という名前のチャンネルを作成すると、サーバー内でボイスチャンネルへの入退出があった場合に通知します。", inline=False)
    embed.add_field(name="サポートサーバーのご案内", value="サポートサーバーでは、製作者に直接お問い合わせすることができます。\n[サポートサーバーに参加](https://discord.gg/pFgBSt6MPX)", inline=False)
    embed.add_field(name="git hubリポジトリ", value="ハリネズミン！v2のコードを見ることができます。\n[リポジトリを見る](https://github.com/animalotta0206/harine_zumin/)", inline=False)
    await ctx.response.send_message(embed=embed)

@tree.command(name="taiman", description="怠慢やね画像を送信します。")
async def taiman(ctx: discord.Interaction):
    embed = discord.Embed(title="怠慢やね😅",color=0x04ff00)
    embed.set_image(url="https://cdn.discordapp.com/attachments/992091661519827074/992091785331490826/20210726_212048.jpg")
    await ctx.response.send_message(embed=embed)

@tree.command(name="bareta", description="ばれたかを送信します。")
async def bareta(ctx: discord.Interaction):
    embed = discord.Embed(title="バレたか😆",color=0x04ff00)
    embed.set_image(url="https://cdn.discordapp.com/attachments/992091661519827074/992091784761053240/20210726_212042.jpg")
    await ctx.response.send_message(embed=embed)
    
@tree.command(name="tweet", description="ツイートを参考にしない😅")
async def tweet(ctx: discord.Interaction):
    embed = discord.Embed(title="ツイートを参考にしない😅",color=0x04ff00)
    embed.set_image(url="https://cdn.discordapp.com/attachments/992091661519827074/992091784521990164/20210726_212045.jpg")
    await ctx.response.send_message(embed=embed)
    
@tree.command(name="goodnight", description="おやすみなさい画像を送信します。")
async def goodnight(ctx: discord.Interaction):
    embed = discord.Embed(title="おやすみなさい😴",color=0x04ff00)
    embed.set_image(url="https://cdn.discordapp.com/attachments/992091661519827074/992091785117585448/20210726_212039.jpg")
    await ctx.response.send_message(embed=embed)
    
@tree.command(name="omikuji", description="おみくじが引けます。不正できます。")
async def omikuji(ctx: discord.Interaction):
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
     await ctx.response.send_message(text)

@tree.command(name="ping",description="botの反応速度を測定できます。")
async def ping(ctx: discord.Interaction):
    # Ping値を秒単位で取得
    raw_ping = client.latency
    # ミリ秒に変換して丸める
    ping = round(raw_ping * 1000)
    embed=discord.Embed(title="Ping!", color=0x00ff00)
    embed.add_field(name="Pong!🏓", value=f'{ping}ms', inline=False)
    await ctx.response.send_message(embed=embed)
    
@tree.command(name="bot_info",description="botの情報を表示します。")
async def bot_info(ctx: discord.Interaction):

    num_of_servers = len(client.guilds)

    embed=discord.Embed(title="ハリネズミン！v2 bot info", color=0x00fa1d)
    embed.set_author(name="ハリネズミン！v2 #0624", icon_url="https://cdn.discordapp.com/avatars/990987427818651648/708788930a3cf8dd9e70349f47a110c6.png?size=4096")
    embed.add_field(name="Python バージョン:", value=sys.version, inline=True)
    embed.add_field(name="OS:", value=f"{platform.system()}\n{platform.release()}\n{platform.version()}", inline=True)
    embed.add_field(name="プロセッサー情報:", value=platform.processor(), inline=True)
    embed.add_field(name="所属しているサーバーの数:", value=num_of_servers, inline=True)
    await ctx.response.send_message(embed=embed)

@tree.command(name="userinfo", description="ユーザー情報を取得します")
async def userinfo(ctx: discord.Interaction, member: discord.Member):
    embed = discord.Embed(title="ユーザー情報", description=member.mention, color=member.color)
    embed.add_field(name="ユーザー名", value=member.name, inline=True)
    embed.add_field(name="ニックネーム", value=member.nick, inline=True)
    embed.add_field(name="ID", value=member.id, inline=True)
    embed.add_field(name="サーバー参加日時", value=member.joined_at.strftime("%Y-%m-%d %H:%M:%S"), inline=True)
    embed.add_field(name="アカウント作成日時", value=member.created_at.strftime("%Y-%m-%d %H:%M:%S"), inline=True)
    embed.set_thumbnail(url=member.avatar_url)
    await ctx.response.send_message(embed=embed)

@tree.command(name="usercheck", description="ユーザ識別子から一意の文字列に変更されているかを確認できます。")
async def usercheck(ctx: discord.Interaction):
    original_response = await ctx.response.send_message("<a:b_sending:1108227693230702642>読み込み中です…")
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

@tree.command(name="share_discord_profile", description="あなたのDiscordプロフィールをほかのSNSで簡単に共有できるURLを生成します。")
async def share_discord_profile(ctx: discord.Interaction):
    await ctx.response.send_message(f"{ctx.author.mention}のDiscordプロフィールリンクはこちらです。\nhttps://discord.com/users/{ctx.author.id}")

@tree.command(name="purge_message", description="最大2000件までのメッセージを削除できます。",)
async def purge_message(ctx: discord.Interaction, about: int):
    if ctx.author.guild_permissions.manage_messages:
        if about >= 2001:
            await ctx.send('メッセージの削除は2000件までに制限されています。')
            return
        try:
            target_channel = client.get_channel(ctx.channel.id)
            if about >= 500:
                w_message = await ctx.response.send_message(f'<a:b_sending:1108227693230702642>{about}件のメッセージを削除しています………\n>>> この処理には数分かかることがあ��ます。\nこれ以降のメッセージは削除対象になりませんので、いつも通りチャットをすることができます。')    
            else:
                w_message = await ctx.response.send_message(f'<a:b_sending:1108227693230702642>{about}件のメッセージを削除しています………')
            deleted = await target_channel.purge(limit=about, before=discord.Object(id=w_message.id), bulk=bool(True))
            await w_message.edit(content=f'<:b_check:1043897762590236704>{len(deleted)}件のメッセージを削除しました。')
        except discord.Forbidden:
            await w_message.edit(content="Botに「メッセージの管理権限」がありません。\nBotの「メッセージの管理権限」を有効化してください。")
        except discord.HTTPException as e:
            embed=discord.Embed(description=f"例外処理されていないエラーが詳細:\n```\n{str(e)}\n```", color=0xff0000)
            embed.add_field(name="何度もエラー発生する場合は…", value="bot開発者の`anima_zumin_0206`までお知らせください。", inline=True)
            embed.add_field(name="サポートサーバーに参加してみませんか？", value=f"サポートサーバーではより迅速に対応できます。\n{support_guild}", inline=True)
            embed.timestamp = datetime.datetime.utcnow()
            await ctx.response.send_message(content=f'エラーが発生しました。\nここまで{len(deleted)}件のメッセージを削除しました。', embed=embed)
    else:
        await ctx.response.send_message(f"コマンド実行者に「メッセージの管理権限」が無いため、リクエストは拒否されました。")

@tree.command(name='panel_create', description='役職パネルを作成します。')
@app_commands.describe(role='役職パネルに追加するロールを指定してください', panel_title='パネルのタイトルを指定できます。', emoji="ロールの絵文字を追加します。", color='役職パネルの色を指定します(16進数で指定してください。)')
async def panel_create(ctx: discord.Interaction, role: discord.Role, panel_title: str, emoji: str, color: str = None):
    if ctx.author.guild_permissions.manage_roles:
        m = await ctx.channel.send('<a:b_sending:1108227693230702642>役職パネルを作成しています………')
        if color is not None:
            embed = discord.Embed(title=panel_title, color=int(color, 16))
        else:
            embed = discord.Embed(title=panel_title)
        embed.add_field(name=emoji, value=f"<@&{role.id}>", inline=True)
        embed.set_footer(text=f'最終更新者:{ctx.author.name}')
        await m.add_reaction(f'{emoji}')
        await m.edit(content='ロールに対応する絵文字にリアクションするとロールを受け取ることができます。', embed=embed)
        reply = await ctx.response.send_message("役職パネルを作成しました！")
        await asyncio.sleep(3)
        await reply.delete()
    else:
        await ctx.response.send_message("ロールの管理権限を持っていないため実行できません。")

@tree.command(name='panel_edit', description='役職パネルを編集します。')
@app_commands.describe(url='役職パネルのメッセージURLを入力してください。', title='役職パネルのタイトルを編集できます。', color='役職パネルの色を指定します。(16進数で指定してください。)')
async def panel_edit(ctx: discord.Interaction, url: str, title: str = None, color: str = None):
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
                if title is not None and color is not None:
                    existing_embed.title = title
                    existing_embed.color = discord.Color(int(color, 16))
                elif title is not None:
                    existing_embed.title = title
                else:
                    existing_embed.color = discord.Color(int(color, 16))
                await message.edit(embed=existing_embed)
                m = await ctx.response.send_message("変更が完了しました。")
                await asyncio.sleep(5)
                await m.delete()
            else:
                await ctx.response.send_message("指定されたメッセージは役職パネルではありません。")
        else:
            await ctx.response.send_message("指定されたメッセージURLはbotのメッセージではないため利用できません。")
    else:
        await ctx.response.send_message("ロールの管理権限を持っていないため実行できません。")

@tree.command(name="panel_add_role", description="役職パネルにロールを追加します(一度につき最大5つまで同時追加が可能です。)")
@app_commands.describe(role1='追加する役職を入力(1つめ)', emoji1='役職に追加する絵文字を指定(1つめ)', role2='追加する役職を入力(2つめ)', emoji2='役職に追加する絵文字を指定(2つめ)', role3='追加する役職を入力(3つめ)', emoji3='役職に追加する絵文字を指定(3つめ)', role4='追加する役職を入力(4つめ)', emoji4='役職に追加する絵文字を指定(4つめ)', role5='追加する役職を入力(5つめ)', emoji5='役職に追加する絵文字を指定(5つめ)', )
async def panel_add_role(ctx: discord.Interaction, url: str, role1: discord.Role, emoji1: str, role2: discord.Role = None, emoji2: str = None, role3: discord.Role = None, emoji3: str = None, role4: discord.Role = None, emoji4: str = None, role5: discord.Role = None, emoji5: str =None):
    if ctx.author.guild_permissions.manage_roles:
        m = await ctx.response.send_message("<a:b_sending:1108227693230702642>処理中…")
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
                if role5 and emoji5 and role4 and emoji4 and role3 and emoji3 and role2 and emoji2 and emoji1 and role1:
                    fields = [
                        {"name": emoji1, "value": f"<@&{role1.id}>", "inline": True},
                        {"name": emoji2, "value": f"<@&{role2.id}>", "inline": True},
                        {"name": emoji3, "value": f"<@&{role3.id}>", "inline": True},
                        {"name": emoji4, "value": f"<@&{role4.id}>", "inline": True},
                        {"name": emoji5, "value": f"<@&{role5.id}>", "inline": True},
                            ]
                if role4 and emoji4 and role3 and emoji3 and role2 and emoji2 and emoji1 and role1:
                    fields = [
                        {"name": emoji1, "value": f"<@&{role1.id}>", "inline": True},
                        {"name": emoji2, "value": f"<@&{role2.id}>", "inline": True},
                        {"name": emoji3, "value": f"<@&{role3.id}>", "inline": True},
                        {"name": emoji4, "value": f"<@&{role4.id}>", "inline": True},
                            ]
                elif role3 and emoji3 and role2 and emoji2 and emoji1 and role1:
                    fields = [
                        {"name": emoji1, "value": f"<@&{role1.id}>", "inline": True},
                        {"name": emoji2, "value": f"<@&{role2.id}>", "inline": True},
                        {"name": emoji3, "value": f"<@&{role3.id}>", "inline": True},
                            ]
                elif role2 and emoji2 and role1 and emoji1:
                    fields = [
                        {"name": emoji1, "value": f"<@&{role1.id}>", "inline": True},
                        {"name": emoji2, "value": f"<@&{role2.id}>", "inline": True},
                            ]
                else:
                  fields = [
                      {"name": emoji1, "value": f"<@&{role1.id}>", "inline": True},
                  ]
            try:
                for field in fields:
                    existing_embed.add_field(name=field["name"], value=field["value"], inline=field["inline"])
                    await message.add_reaction(field["name"])

                await message.edit(embed=existing_embed)
                await m.delete()
            except:
                await m.edit(content="エラーが発生しました。\n引数不足もしくは、絵文字が利用不可のサーバーで作成されたものです。")
    else: 
        await ctx.response.send_message("ロールの管理権限がないため実行できません。")

@tree.command(name="panel_remove_role", description="指定した役職を削除します。")
@app_commands.describe(url='パネルのメッセージURL', role='パネルから削除するロール')
async def panel_remove_role(ctx: discord.Interaction, url: str, role: discord.Role):
    if ctx.author.guild_permissions.manage_roles:
        m = await ctx.response.send_message("<a:b_sending:1108227693230702642>処理中…")
        message_id = extract_message_id(url)
        channel = ctx.channel
        try:
            message = await channel.fetch_message(message_id)
        except discord.NotFound:
            await m.edit(content="指定されたメッセージは見つかりませんでした。")
            return

        if message.author.id == client.user:
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
                    await m.edit(content="指定されたロールは役職パネルに存在しません。")
            else:
                await m.edit(content="指定したメッセージは役職パネルではありません。")
        else:
            await m.edit(content="指定されたメッセージはbotのメッセージではないため利用できません。")
    else:
        await ctx.response.send_message(content="ロールの管理権限がないため実行できません。")

@tree.command(name="afk_set",description="AFKチャンネルに移動したユーザーに通知を送信するか設定できます。")
async def afk_set(ctx: discord.Interaction):
    if ctx.author.guild_permissions.manage_roles:
        with open('harine_zumin/settings.json', 'r') as f:
            data = json.load(f)
        guild = ctx.guild.id
        if guild in data:
            await ctx.send("設定は既に`True`です。")
            return
        data.append(guild)
        with open('harine_zumin/settings.json', 'w') as f:
            json.dump(data, f)
        await ctx.response.send_message("設定が完了しました。")
    else:
        await ctx.response.send_message("この操作には管理者権限が必要になります！")

@tree.command(name='guild_info', description='サーバー情報を取得します。')
async def guild_info(ctx: discord.Interaction):
    guild=client.get_guild(ctx.guild.id)
    name=guild.name
    reader=guild.owner.name
    image=guild.icon.url
    count=guild.member_count

    embed=discord.Embed(color=0x00ff04)
    embed.set_author(name=name, icon_url=image)
    embed.set_thumbnail(url=image)
    embed.add_field(name=サーバーの所有者, value=reader, inline=True)
    embed.add_field(name=メンバーの数, value=count, inline=True)
    await ctx.response.send_message(embed=embed)
    
@tree.command(name='seaver_boostters', description='サーバーにブーストしているユーザーを返します。')
async def seaver_boostters (ctx: discord.Interaction):
    guild=client.get_guild(ctx.guild.id)
    boost_users=guild.premium_subscribers
    embed=discord.Embed(title='サーバーブースターのリスト', color=0xff00f7)
    embed.from_dict(boost_users)
    await ctx.response.send_message(embed=embed)
    
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

#ボイスチャンネル関連
@client.event
async def on_voice_state_update(member, before, after):
    #ミュートとかで呼び出されたときに重複を回避するための条件分岐
    if after.deaf != before.deaf or after.mute != before.mute or after.self_deaf != before.self_deaf or after.self_mute != before.self_mute:
        return
    # 参加した場合
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
    #AFK移動時
    if after.afk is not False:
        embed=discord.Embed(title="寝落ち通知", description=f"あなたは、「{member.guild.name}」でAFKチャンネルに移動されました。", color=int('adff2f', 16))
        embed.timestamp = datetime.datetime.utcnow()
        await member.send(embed=embed)
    #配信開始時
    if after.self_stream is True:
        send_message = discord.utils.get(member.guild.text_channels, name='ボイスチャンネルログ')
        activities = member.activities
        embed=discord.Embed(title="Go Live Stream", description="Activityの詳細",color=int('ffa500', 16))
        if str(member.mobile_status) != 'offline':
            user_client = "📱モバイルクライアント"
        elif str(member.desktop_status) != 'offline':
	        user_client = "🖥デスクトップクライアント"
        elif str(member.web_status) != 'offline':
	        user_client = "🌐ブラウザクライアント"
        else:
	        user_client = "❓不明なクライアント"
        if activities:
            for activity in activities:
                if activity.type == discord.ActivityType.playing:
                    game_name = activity.name
                    game_state = activity.state
                    embed=discord.Embed(title="Go Live Stream", description="Activityの詳細",color=int('ffa500', 16))
                    embed.add_field(name="プレイ中のゲーム", value=game_name, inline=False)
                    embed.add_field(name="ゲームのステータス", value=game_state, inline=True)
                    break
                elif activity.type == discord.ActivityType.streaming:
                    game_name = activity.name
                    game_state = activity.state
                    embed=discord.Embed(title="Go Live Stream", description="Activityの詳細",color=int('ffa500', 16))
                    embed.add_field(name="twich Stream", value=game_name, inline=False)
                    embed.add_field(name="twich state", value=game_state, inline=True)
                    break
                elif activity.type == discord.ActivityType.listening:
                    game_name = activity.title
                    game_state = activity.artist
                    embed=discord.Embed(title="Go Live Stream", description="Activityの詳細",color=int('ffa500', 16))
                    embed.add_field(name="Spotify Listen to", value=game_name, inline=False)
                    embed.add_field(name="Spotify state", value=game_state, inline=True)
                    break
                elif activity.type == discord.ActivityType.watching:
                    game_name = activity.name
                    game_state = activity.state
                    embed=discord.Embed(title="Go Live Stream", description="Activityの詳細",color=int('ffa500', 16))
                    embed.add_field(name="Spotify Listen to", value=game_name, inline=False)
                    embed.add_field(name="Spotify state", value=game_state, inline=True)
                break
            else:
                embed.add_field(name="プレイ中のゲーム", value="Activity���情報はありませんでした。", inline=False)
                embed.add_field(name="ユーザーのクライアント", value=user_client, inline=False)
                embed.set_author(name=f"{member.name}", icon_url="https://media.discordapp.net/avatars/{}/{}.png?size=1024".format(member.id,member.avatar))
                embed.timestamp = datetime.datetime.utcnow()
            if send_message is not None:
                embed.add_field(name="ユーザーのクライアント", value=user_client, inline=False)
                embed.set_author(name=f"{member.name}", icon_url="https://media.discordapp.net/avatars/{}/{}.png?size=1024".format(member.id,member.avatar))
                embed.timestamp = datetime.datetime.utcnow()
                await send_message.send(content=f'Go Live Stream in <#{after.channel.id}>', embed=embed)
    #配信終了時
    elif before.self_stream != after.self_stream :
        send_message = discord.utils.get(member.guild.text_channels, name='ボイスチャンネルログ')
        embed=discord.Embed(title='Go Live Stream',description="配信は終了しました。(し〜ん)",color=0xfbff00)
        embed.set_author(name=f"{member.name}", icon_url="https://media.discordapp.net/avatars/{}/{}.png?size=1024".format(member.id,member.avatar))
        embed.timestamp = datetime.datetime.utcnow()
        if send_message is not None:
            await send_message.send(embed=embed)

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
    if payload.user_id == client.user.id or payload.member.bot:
        return
    try:
        channel = client.get_channel(payload.channel_id)
        message = await channel.fetch_message(payload.message_id)
    except Exception as e:
        channel = client.get_channel(1118756012351029358)
        embed=discord.Embed(title="例外処理エラー(役職パネル)", description=f"詳細:\n```\n{str(e)}```\n")
        await channel.send(embed=embed)
        pass
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
    except Exception as e:
        embed=discord.Embed(description="ロールの付与でエラーが発生しました。\n付与しようとしたロールがbotよりも順位が高いもしくは、アプリケーションに関連付けられたロールの可能性があります。")
        m = await channel.send(f"<@{payload.user_id}>", embed=embed)
        await asyncio.sleep(5)
        await m.delete()
        channel = client.get_channel(1118756012351029358)
        embed=discord.Embed(title="例外処理エラー(役職パネル)", description=f"詳細:\n```\n{str(e)}```\n")
        await channel.send(embed=embed)

@client.event
async def on_reaction_add(reaction, user):
    if reaction.message.author.id == client.user.id:
        return
    if str(reaction.emoji) == '🤔':
        channel = discord.utils.get(reaction.message.guild.channels, name="thinking-channel")
        channel_message = f'<#{reaction.message.channel.id}>'
        count = reaction.count
        content = reaction.message.content
        if count >= 15:
            msg_content = f'🤔🥇 **{count}** {channel_message} [Jump to message](https://discord.com/channels/{reaction.message.guild.id}/{reaction.message.channel.id}/{reaction.message.id})'
        elif count >= 10:
            msg_content = f'🤔🥈 **{count}** {channel_message} [Jump to message](https://discord.com/channels/{reaction.message.guild.id}/{reaction.message.channel.id}/{reaction.message.id})'
        elif count >= 5:
            msg_content = f'🤔🥉 **{count}** {channel_message} [Jump to message](https://discord.com/channels/{reaction.message.guild.id}/{reaction.message.channel.id}/{reaction.message.id})'
        else:
            msg_content = f'🤔 **{count}** {channel_message} [Jump to message](https://discord.com/channels/{reaction.message.guild.id}/{reaction.message.channel.id}/{reaction.message.id})'
        if channel is not None:
            embed=discord.Embed(description=content,color=0x00ff2a)
            embed.set_author(name=f"{reaction.message.author.name}", url=f'https://discord.com/channels/{reaction.message.guild.id}/{reaction.message.channel.id}/{reaction.message.id}', icon_url=f"https://media.discordapp.net/avatars/{reaction.message.author.id}/{reaction.message.author.avatar}.png?size=1024")
            embed.set_footer(text=f'ID:{reaction.message.id}')
            embed.timestamp = datetime.datetime.utcnow()
            reaction_message = await channel.send(content=msg_content, embed=embed)
            await reaction_message.add_reaction('🤔')
        else:
            return
        

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
    if sync_command:
        await tree.sync()
        print('コマンド同期を実行しました！')

client.run('TOKEN')
