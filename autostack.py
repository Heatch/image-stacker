from tkinter import filedialog
from PIL import Image, ImageFont, ImageDraw 
from datetime import datetime

#getting images and defining variables
imgs = filedialog.askopenfilenames()

total_width = 0
total_height = 0
max_width = 0
max_height = 0
ix =[]

#calculating dimensions required for new image
for img in imgs:
    im = (Image.open(img).resize((1296, 864)))
    size = im.size
    w = size[0]
    h = size[1]
    total_width += w 
    total_height += h
    
    if h > max_height:
        max_height = h
    if w > max_width:
        max_width = w
    ix.append(im) 

#creating new image and pasting composing images
target_vertical = Image.new('RGB', (max_width, total_height))

pre_w = 0
pre_h = 0
for img in ix:
    target_vertical.paste(img, (pre_w, pre_h, pre_w+max_width, pre_h + img.size[1]))
    pre_h += img.size[1]

#adding the year titles then opening final image
image_editable = ImageDraw.Draw(target_vertical)

currentYear = datetime.now().year
startYear = currentYear - len(imgs) + 1
yearTitle = ImageFont.truetype('Ubuntu-Regular.ttf', 100)
baby_blue = (137, 207, 240)  # Baby blue color
rich_blue = (0, 51, 102)     # Dark rich blue color

i = 0
pos = 0
padding = 15  # Padding around text
vertical_adjustment = 20  # Pixels to move text upward
highlight_padding = 25  # Additional padding for highlight box
while i < len(imgs):
    title_text = str(startYear + i)
    # Calculate text size
    text_bbox = image_editable.textbbox((0, 0), title_text, font=yearTitle)
    text_width = text_bbox[2] - text_bbox[0]
    text_height = text_bbox[3] - text_bbox[1]
    # Position text at bottom left with padding, 20 pixels higher
    x = padding
    y = pos + 864 - text_height - padding - vertical_adjustment  # 20 pixels higher
    
    # Draw highlight rectangle with increased size
    highlight_bbox = [
        x - highlight_padding,
        y - highlight_padding,
        x + text_width + highlight_padding,
        y + text_height + highlight_padding
    ]
    image_editable.rectangle(highlight_bbox, fill=rich_blue)
    
    # Draw text
    image_editable.text((x, y), title_text, baby_blue, font=yearTitle)
    
    i += 1
    pos += 864

target_vertical.show()
target_vertical.save('evolution.png', quality=100)
