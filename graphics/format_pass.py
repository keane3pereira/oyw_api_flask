from PIL import Image,ImageDraw,ImageFont
import os, png, pyqrcode, fnvhash


fnt = ImageFont.truetype("graphics/fonts/Anita.ttf",46)#set headingfont

def create_pass(pid, name, daycode, weekcode):
    
    back = Image.open('graphics/templates/pass.png')#open back
    d = ImageDraw.Draw(back)
    
    name_width = d.textsize(name,fnt)[0]
    pos_x = (470 - name_width)/2
    d.text((pos_x,130),name,fill=(0,0,0),font=fnt,align="center")

    day_qr = pyqrcode.create(daycode)
    day_qr.png("graphics/qr_codes/qr"+str(pid)+".png", scale = 4)
    day_qr_pic = Image.open("graphics/qr_codes/qr"+str(pid)+".png")
    back.paste(day_qr_pic,(125,270))
    
    week_qr = pyqrcode.create(weekcode)
    week_qr.png("graphics/qr_codes/qr"+str(pid)+".png", scale = 4)
    week_qr_pic = Image.open("graphics/qr_codes/qr"+str(pid)+".png")

    back.paste(week_qr_pic,(125,570))
    back.save("graphics/created_passes/pass"+str(pid)+".png")



def find_created_pass_pic(pid):
    if "pass"+str(pid)+".png" in os.listdir('graphics/created_passes'):
        return True
    else:
        return False
    
