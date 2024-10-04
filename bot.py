#extensiones
from PIL import Image,ImageFont,ImageDraw

import json
import os
import discord
import asyncio
import logging
import requests
from io import BytesIO
from discord.ext import commands
from math import cos, sin, radians

intents = discord.Intents.default()
intents.message_content = True
intents.members = True
    
bot = commands.Bot(command_prefix='!porpol ', intents=intents, activity=discord.Game(name='SapoDeRana'))
#Funcion de imagen de bienvenida
def avatar_wo(user):

    imgno = Image.open('basewo.jpeg')
    url = user.avatar.url
    response = requests.get(url)
    icon = Image.open(BytesIO(response.content)).convert("RGBA")
    font = ImageFont.truetype("bold.otf", 80)

    img = imgno.resize((1632, 920))

    W = img.width
    H = img.height

    draw = ImageDraw.Draw(img)

    # Dibujar el círculo principal
    draw.ellipse((610, 138, 1010, 538), outline="white", width=10)

    # Dibujar los "pétalos" alrededor del círculo
    cx, cy = 810, 340  # Centro del círculo
    radius = 210  # Radio del círculo
    num_petals = 12
    small_radius = 54  # Tamaño de los pétalos
    petal_distance = 0.84  # Factor de distancia de los pétalos al centro del círculo

    for i in range(num_petals):
        angle = (i / num_petals) * 360
        x_offset = int(radius * petal_distance * cos(radians(angle)))
        y_offset = int(radius * petal_distance * sin(radians(angle)))
        draw.ellipse(
            (cx + x_offset - small_radius, cy + y_offset - small_radius,
             cx + x_offset + small_radius, cy + y_offset + small_radius),
            fill="white"
        )

    fontColor = "#F5F7B0"
    text = "Bienvenido al servidor"

    _, _, w, h = draw.textbbox((0, -550), text, font=font)
    draw.text(((W - w) / 2, (H - h) / 2), text, font=font, fill=fontColor, stroke_width=8, stroke_fill="black")

    font = ImageFont.truetype("bold.otf", 120)
    text = user.name
    fontColor = "#BFE1FE"
    _, _, w, h = draw.textbbox((0, -350), text, font=font)
    draw.text(((W - w) / 2, (H - h) / 2), text, font=font, fill=fontColor, stroke_width=8, stroke_fill="black")

    vre = icon.resize((380, 380))

    copy = img.copy()
    mask = Image.new("L", vre.size, 0)
    draw = ImageDraw.Draw(mask)
    draw.ellipse((0, 0, 380, 380), fill=1000)
    copy.paste(vre, (620, 150), mask)

    copy.save("sopabuena.png")

#Funcion de imagen de despedida
def avatar_go(user):

    # Cargar la imagen base y el icono
    imgno = Image.open('basego.jpeg')
    url = user.avatar.url
    response = requests.get(url)
    icon = Image.open(BytesIO(response.content)).convert("RGBA")
    font = ImageFont.truetype("bold.otf", 80)

    img = imgno.resize((1632, 920))

    W = img.width
    H = img.height

    draw = ImageDraw.Draw(img)

    # Dibujar el círculo principal
    draw.ellipse((610, 140, 1010, 540), outline="#1b1d23", width=10)

    # Dibujar las hojas alrededor del círculo
    cx, cy = 820, 360  # Centro del círculo
    radius = 160  # Radio del círculo
    num_leaves = 11  # Número de hojas
    leaf_length = 80  # Longitud de las hojas
    leaf_width = 28   # Ancho de las hojas

    for i in range(num_leaves):
        angle = (i / num_leaves) * 360
        x_offset = int(radius * cos(radians(angle)))
        y_offset = int(radius * sin(radians(angle)))

        # Coordenadas de la hoja como una elipse inclinada
        leaf_bbox = [
            (cx + x_offset - leaf_width, cy + y_offset - leaf_length),
            (cx + x_offset + leaf_width, cy + y_offset + leaf_length)
        ]

        # Dibujar la hoja con un ángulo de rotación
        draw.ellipse(leaf_bbox, fill="#1b1d23")

    # Añadir el texto en la imagen
    fontColor = "#BAE1D3"
    text = "Abandonó el servidor"

    _, _, w, h = draw.textbbox((0, -550), text, font=font)
    draw.text(((W - w) / 2, (H - h) / 2), text, font=font, fill=fontColor, stroke_width=8, stroke_fill="black")

    font = ImageFont.truetype("bold.otf", 120)
    text = user.name
    fontColor = "#BFE1FE"
    _, _, w, h = draw.textbbox((0, -350), text, font=font)
    draw.text(((W - w) / 2, (H - h) / 2), text, font=font, fill=fontColor, stroke_width=8, stroke_fill="black")

    # Ajustar el icono y superponerlo en la imagen
    vre = icon.resize((380, 380))

    copy = img.copy()
    mask = Image.new("L", vre.size, 0)
    draw = ImageDraw.Draw(mask)
    draw.ellipse((0, 0, 380, 380), fill=1000)
    copy.paste(vre, (620, 150), mask)

    copy.save("sopamala.png")

#Esto no sirve aqui
def newData(user):
  with open("data.json", "r+") as outfile:
    objto = json.load(outfile)
    numIntegrante = objto['numeroIntegrantes']
    numIntegrante += 1
    objto['numeroIntegrantes'] = numIntegrante
    outfile.seek(0)
    json.dump(objto, outfile, indent=4)
  
  y = {
      "user": user.name,
      "id": user.id,
      "name": user.name,
      "num": numIntegrante,
      "coins": 10,
      "level": 1,    
      "xp": 0
  }
  
  with open("data.json", "r+") as outfile:
    file_data = json.load(outfile)
    # Join new_data with file_data inside emp_details
    file_data['integrantes'].append(y)
    # Sets file's current position at offset.
    outfile.seek(0)


    json.dump(file_data, outfile, indent=4)

  avatar_wo(user)
  
#BOT COMMANDS
@bot.event
async def on_ready():
    print(f'We have logged in as {bot.user}')

    global welcome, goodbye, server, role, cmal
    welcome = bot.get_channel(1269399272978255872)
    goodbye = bot.get_channel(1269399506399531019)
    server = bot.get_guild(1124106111893643328)
    cmal = bot.get_channel(1159987278601539595)

@bot.event
async def on_member_join(member):
    avatar_wo(member)

    await welcome.send(f"<a:lili:1159721858418081802>{member.mention} se ha unido al servidor. ¡Bienvenido! ", file=discord.File("sopabuena.png"))

@bot.event
async def on_member_remove(member):
    avatar_go(member)
    
    await goodbye.send(f"☆Adios {member.name}, hasta pronto!", file=discord.File("sopamala.png"))



#@bot.event
#async def on_message(message):
    #if message.author == bot.user:
        #return

    #if message.content.startswith('s'):
       # await message.channel.send('Hello!')


@bot.listen('on_message')
async def whatever_you_want_to_call_it(message):
  if message.author == bot.user:
      return

#Sincronizar comandos slash
@bot.command(name="syncCommands")
async def sync(ctx):
    await ctx.send("syncing... check log")
    await bot.tree.sync()
    await asyncio.sleep(4)
    await ctx.message.delete()
    print("SYNCED")

@bot.hybrid_command(name="coins", description="Ver tus monedas rana o las de otro miembro")
async def checkCoins(ctx, member: discord.Member = None):
  if member is None:
    member = ctx.author
  with open("data.json", "r+") as outfile:
    objto = json.load(outfile)
    for wallet in objto['wallets']:
      if(wallet['id'] == member.id):
        await ctx.send(f"**{member.name}** tiene {wallet['coins']} monedas rana")
        return
    await ctx.send(f"{member.name} no tiene monedas rana" )
    

  
@bot.hybrid_command(name="navidad", description="Feliz navidad!")
async def navidad(ctx, member: discord.Member = None):
  if member is None:
    member = ctx.author
  await ctx.send(f"Feliz navidad! {member.mention}")

@bot.command(name="kick", description="Expulsa a un usuario")
async def kick(ctx, user: discord.Member, reason = None):
  await user.kick(reason=reason)
  

@bot.hybrid_command(name="newc", description="Crear un pajaroto")
async def newCharacter(ctx, extra):
  character = {
    "name": ctx.author.name,
    "id": ctx.author.id,
    "extra": extra
  }
  
  json_object = json.dumps(character, indent=3)
  
  
  with open("data.json", "w") as outfile:
    outfile.write(json_object)

@bot.hybrid_command(name="integrantes", description="Revisa la lista de integrantes en el servidor")
async def IntegrantesSend(ctx):
  mensaje = ""
  with open('data.json', 'r') as openfile:
      # Reading from json file
      objto = json.load(openfile)
      integrantes = objto['integrantes']
      for integrante in integrantes:
          mensaje += f"**{integrante['num']}-** {integrante['name']} \n"
      await ctx.send(mensaje)
    
@bot.command(name="addrole", description="Añade un rol a un usuario (mediante el id)")
async def rolesAdd(ctx, roleid, user: discord.Member):
  roleP = server.get_role(roleid)
  await user.add_roles(roleP)

@bot.command(name="welcomeM")
async def welcomeM(ctx, user):
    member = bot.get_user(int(user))
    avatar_wo(member)

    await welcome.send(f"<:shiny:1159722247905357844><a:lili:1159721858418081802>{member.mention} se ha unido al servidor. ¡Bienvenido! ", file=discord.File("sopa.png"))

@bot.command(name="send")
async def sendMessage(ctx, chan, *args):
    if ctx.channel == cmal:
        channel = bot.get_channel(int(chan))
        message = " ".join(args)
        await channel.send(message)
    else:
        await ctx.send("You dont have permission")
    
@bot.command(name="welcomeTest")
async def welcomeTest(ctx, user):
    member = bot.get_user(int(user))
    avatar_wo(member)

    await welcome.send(f"<a:lili:1159721858418081802>{member.mention} se ha unido al servidor. ¡Bienvenido! ", file=discord.File("sopabuena.png"))
@bot.command(name="goodbyeTest")
async def goodbyeTest(ctx, user):
    member = bot.get_user(int(user))
    avatar_go(member)

    await ctx.send(f"☆Adios {member.name}, hasta pronto!", file=discord.File("sopamala.png"))



# Import the token from secrets.txt
with open('secrets.txt', 'r') as file:
  token = file.read().strip()

bot.run(token)