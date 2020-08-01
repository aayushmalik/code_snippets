import pandas as pd
import numpy as np
from PIL import Image, ImageDraw, ImageFont
import textwrap

df = pd.read_csv('WordsGermanWithAayush100VerbsEncoded.csv', encoding="ANSI")

import random, os
path = r"C:\Users\AayushMalik\Desktop\germany_photos"

def image_generator(word, meaning, sentence_de, sentence_en, index):
    '''
    this function takes four values: word, meaning, example sentece in German and example sentence in English
    and returns an image that contains those things along with the branding
    '''
    random_filename = random.choice([
        x for x in os.listdir(path)
        if os.path.isfile(os.path.join(path, x))
    ])
    randomfile_address = r"C:\Users\AayushMalik\Desktop\germany_photos"+"\\"+random_filename
    
    img = Image.open(randomfile_address)
    
    basewidth = 800
    wpercent = (basewidth/float(img.size[0]))
    hsize = int((float(img.size[1])*float(wpercent)))
    img = img.resize((basewidth,hsize), Image.ANTIALIAS) 

    width, height = img.size[0], img.size[1]

    if width > height:
        img_cropped = img.crop((0, 0, height, height))
    else:
        img_cropped = img.crop((0, 0, width, width))

    new_width = img_cropped.size[0]
    new_height = img_cropped.size[1]

    draw = ImageDraw.Draw(img_cropped, "RGBA")
    draw.rectangle((0.15*new_width, 0.15*new_height, 0.85*new_width, 0.85*new_height), fill = (0, 0, 0, 200))

    FONT_WORD = ImageFont.truetype('FuturaLT.ttf', 30)
    FONT_MEANING = ImageFont.truetype('FuturaLT.ttf', 20)
    FONT_FOOTER = ImageFont.truetype('FuturaLT.ttf', 15)

    draw.text((0.2*new_width, 0.2*new_height), word, font=FONT_WORD, fill=(255, 255, 255))
    
    draw.text((0.2*new_width, 0.28*new_height), meaning, font=FONT_MEANING, fill=(255, 255, 255))
    
    lines = textwrap.wrap(sentence_de, width=35)
    y_text = 0.48*new_height
    for line in lines:
        width, height = FONT_MEANING.getsize(line)
        draw.text((0.2*new_width, y_text), line, font=FONT_MEANING, fill=(255, 255, 255))
        y_text += height

    lines = textwrap.wrap(sentence_en, width=35)
    y_text = 0.63*new_height
    for line in lines:
        width, height = FONT_MEANING.getsize(line)
        draw.text((0.2*new_width, y_text), line, font=FONT_MEANING, fill=(255, 255, 255))
        y_text += height

    draw.text((0.2*new_width, 0.77*new_height), "@germanwithaayush\nTop 100 German Verbs", font=FONT_FOOTER, fill=(255, 255, 255))

    img_cropped.save(f'verb{index}.png') #something to make names different
    
for index, row in df.iterrows():
    print(index,"\n", row[0], row[1], row[2], row[3])
    image_generator(row[0], row[1], row[2], row[3], index)