from PIL import Image, ImageFont, ImageDraw

font = ImageFont.truetype("F25_Bank_Printer.ttf", 16)

img = Image.open('background.png')

title_text = "AUUUUUGH"
image_editable = ImageDraw.Draw(img)
image_editable.text((15,15), title_text, (237,230,211), font=font)

img.show()
img.save('fuckyou.png')
