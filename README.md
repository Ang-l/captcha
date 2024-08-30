# captcha

- 此脚本是一个模拟captche生成一个校验图片的脚本

## 效果
<img width="373" alt="image" src="https://github.com/user-attachments/assets/e3baae53-6f3d-4810-9dab-fdb55c474061">


## 调用示例
- main.py  # 生成文件

```python
### 调用方式

captcha_instance = Captcha(config)

# 生成验证码
captcha_data = captcha_instance.create("02587a53-1b49-4497-9896-b88b1c50fa4b")

print(captcha_data)

```

- check.py # 校验坐标 
```python
### 调用方式

correct_coords = [      # ### 需要点击的正确坐标、这里设置两个
  {
    "size": 21,
    "name": "fire",
    "text": "<火>",
    "width": 32,
    "height": 32,
    "x": 23,
    "y": 25
  },
  {
    "size": 22,
    "name": "rocket",
    "text": "<火箭>",
    "width": 32,
    "height": 32,
    "x": 138,
    "y": 53
  }
]

# 示例数据
user_click_data_str = "104,37-164,76;350;200"   # 104,37 第一个点击的x、y。164,76第二个点击的x、y。350;200图片宽高
is_valid = validate_click(user_click_data_str, correct_coords)

print("点击正确" if is_valid else "点击错误")

```

- 如果想生成中文而非英文的、调整以下
```python
text = ''.join(random.choices('ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz0123456789', k=num_text_chars))

#将此代码调整文
text = ''.join(random.choices('需要生成的中文信息不限字数', k=num_text_chars))

```
