import time
import random
import os
import json
import base64
import hashlib

from PIL import Image, ImageDraw, ImageFont


config = {    # ###### 配置字典，例如：背景路径、字体路径、图标字典、生成图标长度、结果长度
    "bg_paths": [
        'static/images/captcha/click/bgs/1.png',
        'static/images/captcha/click/bgs/2.png',
        'static/images/captcha/click/bgs/3.png',
    ],
    "font_paths": [
        'static/fonts/zhttfs/SourceHanSansCN-Normal.ttf'
    ],
    "icon_dict": {
        "aeroplane": "飞机",
        "apple": "苹果"
    },
    "length": 4,
    "arr_len": 2
}


class Captcha:
    def __init__(self, config, expire=300):
        self.config = config  
        self.expire = expire
        self.bg_paths = self.config['bg_paths']
        self.font_paths = self.config['font_paths']
        self.icon_dict = self.config['icon_dict']

    def create(self, id: str):
        bg_path = random.choice(self.bg_paths)
        font_path = random.choice(self.font_paths)
        image = Image.open(bg_path)
        draw = ImageDraw.Draw(image)
        num_text = self.config['length']
        num_icons = min(len(self.icon_dict), num_text)
        num_text_chars = num_text - num_icons

        # ####### Select the text information, if necessary, it can be adjusted to any type of text such as Chinese, etc.
        text = ''.join(random.choices('ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz0123456789', k=num_text_chars))
        icons = random.sample(list(self.icon_dict.keys()), num_icons) if num_icons > 0 else []

        rand_points = list(text) + icons
        random.shuffle(rand_points)

        text_arr = []

        icon_base_path = 'static/images/captcha/click/icons/'

        occupied = []

        for v in rand_points:
            tmp = {}
            tmp['size'] = random.randint(15, 30)

            if v in self.icon_dict:
                # #### Draw Icon
                icon_path = os.path.join(icon_base_path, f"{v}.png")
                if os.path.exists(icon_path):
                    icon = Image.open(icon_path)
                    icon_width, icon_height = icon.size

                    placed = False
                    while not placed:
                        x = random.randint(0, image.width - icon_width)
                        y = random.randint(0, image.height - icon_height)
                        if all(not self._is_overlapping(x, y, icon_width, icon_height, ox, oy, ow, oh) for (ox, oy, ow, oh) in occupied):
                            image.paste(icon, (x, y), icon.convert('RGBA'))
                            tmp['icon'] = True
                            tmp['name'] = v
                            tmp['text'] = f"<{self.icon_dict[v]}>"
                            tmp['width'] = icon_width
                            tmp['height'] = icon_height
                            tmp['x'] = x
                            tmp['y'] = y
                            occupied.append((x, y, icon_width, icon_height))
                            placed = True
                else:
                    tmp['icon'] = False
                    tmp['text'] = v
                    tmp['width'] = 0
                    tmp['height'] = 0
                    tmp['x'] = 0
                    tmp['y'] = 0
            else:
                # ###### Drawing Text
                font = ImageFont.truetype(font_path, tmp['size'])
                text_width, text_height = draw.textsize(v, font=font)

                placed = False
                while not placed:
                    x = random.randint(0, image.width - text_width)
                    y = random.randint(0, image.height - text_height)
                    if all(not self._is_overlapping(x, y, text_width, text_height, ox, oy, ow, oh) for (ox, oy, ow, oh) in occupied):
                        draw.text((x, y), v, font=font, fill=(239, 239, 234))
                        tmp['icon'] = False
                        tmp['text'] = v
                        tmp['width'] = text_width
                        tmp['height'] = text_height
                        tmp['x'] = x
                        tmp['y'] = y
                        occupied.append((x, y, text_width, text_height))
                        placed = True

            text_arr.append(tmp)

        # ####### Split the first two into select answers
        text_arr = text_arr[:self.config['arr_len']]
        text = [item['text'] for item in text_arr]

        # ###### Save the image locally and delete it if necessary
        image_filename = f"{id}.png"
        image.save(image_filename, format="PNG")

        with open(image_filename, "rb") as img_file:
            base64_image = base64.b64encode(img_file.read()).decode()

        os.remove(image_filename)

        return {
            'id': id,
            'text': text,
            'base64': 'data:image/png;base64,' + base64_image,
            'width': image.width,
            'height': image.height,
            'text_arr': text_arr
        }

    # ########### Collision detection to avoid icon overlap
    def _is_overlapping(self, x1, y1, w1, h1, x2, y2, w2, h2):
        return not (x1 > x2 + w2 or x1 + w1 < x2 or y1 > y2 + h2 or y1 + h1 < y2)


