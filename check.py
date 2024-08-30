# 正确的点击坐标
correct_coords = [
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

def parse_user_clicks(user_click_data_str):
    # 分割字符串，获取用户点击坐标和图像尺寸部分
    parts = user_click_data_str.split(';')
    
    coords_str = parts[0]
    image_width = int(parts[1])
    image_height = int(parts[2])
    
    # 分割坐标
    click_coords = coords_str.split('-')
    click1_x, click1_y = map(int, click_coords[0].split(','))
    click2_x, click2_y = map(int, click_coords[1].split(','))
    
    return [(click1_x, click1_y), (click2_x, click2_y)], (image_width, image_height)

def is_within_tolerance(user_coord, correct_coord):
    # 容错范围为图标的宽度和高度
    tolerance_x = correct_coord['width']
    tolerance_y = correct_coord['height']
    
    return (abs(user_coord[0] - correct_coord['x']) <= tolerance_x and
            abs(user_coord[1] - correct_coord['y']) <= tolerance_y)

def validate_click(user_click_data_str, correct_coords):
    try:
        user_clicks, _ = parse_user_clicks(user_click_data_str)
    except ValueError as e:
        print("错误:", e)
        return False
    
    # 确保用户点击数量与正确坐标数量一致
    if len(user_clicks) != len(correct_coords):
        return False
    
    # 确保每个用户点击坐标都与对应的正确坐标匹配
    for i, user_click in enumerate(user_clicks):
        correct_coord = correct_coords[i]
        if not is_within_tolerance(user_click, correct_coord):
            return False
    
    return True

# 示例数据
user_click_data_str = "104,37-164,76;350;200"
is_valid = validate_click(user_click_data_str, correct_coords)

print("点击正确" if is_valid else "点击错误")
