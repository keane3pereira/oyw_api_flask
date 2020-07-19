from PIL import Image,ImageDraw,ImageFont
import os, png, pyqrcode, fnvhash


hd = ImageFont.truetype("graphics/fonts/Anita.ttf",60)#set headingfont
fnt = ImageFont.truetype("graphics/fonts/Anita.ttf",34)#set headingfont

def create_pass():
    
    back = Image.open('graphics/templates/back.jpg')#open back
    d = ImageDraw.Draw(back)
    
    name_width = d.textsize("OYW'19",hd)[0]
    pos_x = (470 - name_width)/2
    d.text((pos_x-3,30),"OYW'19",fill=(255,255,255),font=hd)
    d.text((pos_x+3,30),"OYW'19",fill=(0,0,0),font=hd)
   
    name_width = d.textsize('DAY PASS',fnt)[0]
    pos_x = (470 - name_width)/2
    d.text((pos_x,230),"DAY PASS",fill=(0,0,0),font=fnt)

    name_width = d.textsize('WEEK PASS',fnt)[0]
    pos_x = (470 - name_width)/2
    d.text((pos_x,530),"WEEK PASS",fill=(0,0,0),font=fnt)

    back.save("graphics/templates/pass.png")

create_pass()