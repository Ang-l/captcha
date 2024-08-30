import sqlite3
import time
import random
import os
import json
from PIL import Image, ImageDraw, ImageFont
import base64
import hashlib


config = {
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
        self.config = config  # 配置字典，例如：背景路径、字体路径、图标字典等
        self.expire = expire  # 验证码的过期时间，默认为300秒
        self.bg_paths = config['bg_paths']  # 背景图片路径列表
        self.font_paths = config['font_paths']  # 字体文件路径列表
        self.icon_dict = config['icon_dict']  # 图标字典
        self.conn = sqlite3.connect('captcha.db')  # SQLite数据库连接
        self._create_table()  # 创建表

    def _create_table(self):
        cursor = self.conn.cursor()
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS captcha (
                key TEXT PRIMARY KEY,
                code TEXT,
                captcha TEXT,
                create_time INTEGER,
                expire_time INTEGER
            )
        ''')
        self.conn.commit()

    def create(self, id: str):
        # 随机选择背景和字体
        bg_path = random.choice(self.bg_paths)
        font_path = random.choice(self.font_paths)

        # 打开背景图片
        image = Image.open(bg_path)
        draw = ImageDraw.Draw(image)

        # 生成固定数量的验证码文本
        num_text = self.config['length']
        num_icons = min(len(self.icon_dict), num_text)
        num_text_chars = num_text - num_icons

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
                # 绘制图标
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
                # 绘制文本
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

        # 截取指定长度的文本和图标
        text_arr = text_arr[:self.config['arr_len']]
        text = [item['text'] for item in text_arr]

        # 保存验证码到数据库
        now_time = int(time.time())
        cursor = self.conn.cursor()
        cursor.execute('''
        INSERT OR REPLACE INTO captcha (key, code, captcha, create_time, expire_time)
        VALUES (?, ?, ?, ?, ?)
        ''', (hashlib.md5(id.encode()).hexdigest(), hashlib.md5(''.join(text).encode()).hexdigest(), json.dumps(text_arr), now_time, now_time + self.expire))
        self.conn.commit()

        # 将图片保存到本地文件系统
        image_filename = f"{id}.png"
        image.save(image_filename, format="PNG")

        # 将图片转换为Base64编码
        with open(image_filename, "rb") as img_file:
            base64_image = base64.b64encode(img_file.read()).decode()

        return {
            'id': id,
            'text': text,  # 返回详细信息的文本列表
            'base64': 'data:image/png;base64,' + base64_image,
            'width': image.width,
            'height': image.height,
            'text_arr': text_arr
        }

    def _is_overlapping(self, x1, y1, w1, h1, x2, y2, w2, h2):
        return not (x1 > x2 + w2 or x1 + w1 < x2 or y1 > y2 + h2 or y1 + h1 < y2)


