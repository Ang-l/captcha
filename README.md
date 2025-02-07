# captcha

- This script is a Python simulation captche to generate a verification image, which can be introduced separately into the project
  
- Pull project, install dependencies, and generate
```python
git clone git@github.com:Ang-l/captcha.git
cd captcha
pip install Pillow    # ###### Install dependencies
python main.py
```

## effect
<img width="373" alt="image" src="https://github.com/user-attachments/assets/e3baae53-6f3d-4810-9dab-fdb55c474061">


## Call Example
- main.py  # Generate files

```python
### Call Method

captcha_instance = Captcha(config)

# Generate verification code
captcha_data = captcha_instance.create("02587a53-1b49-4497-9896-b88b1c50fa4b")

print(captcha_data)

```

- # Verify coordinates
```python
###  Call Method

correct_coords = [      # ### The correct coordinates that need to be clicked, set two here
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
user_click_data_str = "104,37-164,76;350;200"   # 104,37 The first clicked x y。164, 76. The second click on x y。350; 200 picture width and height
is_valid = validate_click(user_click_data_str, correct_coords)

print("secc" if is_valid else "fai")

```

- If you want to generate Chinese instead of English, adjust the following
```python
text = ''.join(random.choices('ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz0123456789', k=num_text_chars))

# 将此代码调整文
text = ''.join(random.choices('需要生成的中文信息不限字数', k=num_text_chars))

```
