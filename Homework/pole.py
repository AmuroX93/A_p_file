import math

def dms_to_decimal(degrees, minutes, seconds, direction):
    """
    将 度-分-秒 (DMS) 格式转换为 十进制度 (DD) 格式。
    
    参数:
    degrees (int): 度
    minutes (int): 分
    seconds (float): 秒
    direction (str): 方向 ('N', 'S', 'E', 'W')
    
    返回:
    float: 十进制度格式的坐标
    """
    decimal_degrees = degrees + (minutes / 60) + (seconds / 3600)
    
    # 南纬和西经为负值
    if direction.upper() in ('S', 'W'):
        decimal_degrees *= -1
        
    return decimal_degrees

def decimal_to_dms_course(dd):
    """
    将 十进制度 (0-360) 转换为 度-分-秒 格式 (用于航向)。
    
    参数:
    dd (float): 十进制度 (0-360)
    
    返回:
    str: 格式化为 "DDD° MM' SS.SS\"" 的字符串
    """
    # 确保在 0-360 范围内
    dd = dd % 360
    
    degrees = int(dd)
    minutes_decimal = (dd - degrees) * 60
    minutes = int(minutes_decimal)
    seconds = (minutes_decimal - minutes) * 60
    
    # 处理舍入问题，防止出现 60 秒
    if seconds > 59.999:
        seconds = 0.0
        minutes += 1
        if minutes == 60:
            minutes = 0
            degrees = (degrees + 1) % 360
            
    # 格式化输出:
    # 航向的度数通常补全为3位 (e.g., 061°)
    # 分和秒补全为2位
    return f"{degrees:03d}° {minutes:02d}' {seconds:05.2f}\""


def calculate_great_circle(lat_a_dms, lon_a_dms, lat_b_dms, lon_b_dms):
    
    # --- 1. 将 DMS 转换为十进制度 (DD) ---
    lat_a_dd = dms_to_decimal(*lat_a_dms)
    lon_a_dd = dms_to_decimal(*lon_a_dms)
    lat_b_dd = dms_to_decimal(*lat_b_dms)
    lon_b_dd = dms_to_decimal(*lon_b_dms)

    # --- 2. 将十进制度转换为弧度 ---
    lat_a_rad = math.radians(lat_a_dd)
    lon_a_rad = math.radians(lon_a_dd)
    lat_b_rad = math.radians(lat_b_dd)
    lon_b_rad = math.radians(lon_b_dd)

    # --- 3. 计算经差 (Dλ) ---
    d_lon_rad = lon_b_rad - lon_a_rad
    if d_lon_rad > math.pi:
        d_lon_rad -= 2 * math.pi
    elif d_lon_rad < -math.pi:
        d_lon_rad += 2 * math.pi

    # --- 4. 计算航程 (Distance) ---
    cos_d = (math.sin(lat_a_rad) * math.sin(lat_b_rad)) + \
            (math.cos(lat_a_rad) * math.cos(lat_b_rad) * math.cos(d_lon_rad))
    cos_d = max(-1.0, min(1.0, cos_d))
    d_rad = math.acos(cos_d)
    distance_nm = math.degrees(d_rad) * 60

    # --- 5. 计算初始航向 (Initial Course) ---
    y_a = math.sin(d_lon_rad) * math.cos(lat_b_rad)
    x_a = (math.cos(lat_a_rad) * math.sin(lat_b_rad)) - \
          (math.sin(lat_a_rad) * math.cos(lat_b_rad) * math.cos(d_lon_rad))
    initial_course_rad = math.atan2(y_a, x_a)
    initial_course_deg = (math.degrees(initial_course_rad) + 360) % 360

    # --- 6. 计算到达航向 (Final Course) ---
    y_b = math.sin(-d_lon_rad) * math.cos(lat_a_rad)
    x_b = (math.cos(lat_b_rad) * math.sin(lat_a_rad)) - \
          (math.sin(lat_b_rad) * math.cos(lat_a_rad) * math.cos(d_lon_rad))
    course_b_to_a_rad = math.atan2(y_b, x_b)
    course_b_to_a_deg = (math.degrees(course_b_to_a_rad) + 360) % 360
    final_course_deg = (course_b_to_a_deg + 180) % 360

    # --- 7. 格式化输出 (将航向转为 DMS 字符串) ---
    initial_course_dms_str = decimal_to_dms_course(initial_course_deg)
    final_course_dms_str = decimal_to_dms_course(final_course_deg)

    return {
        "distance_nm": distance_nm,
        "initial_course_dms_str": initial_course_dms_str,
        "final_course_dms_str": final_course_dms_str,
        "inputs": {
            "lat_a_dms": lat_a_dms,
            "lon_a_dms": lon_a_dms,
            "lat_b_dms": lat_b_dms,
            "lon_b_dms": lon_b_dms
        }
    }

if __name__ == "__main__":
    
    # 起始点
    lat_a = (28, 16, 30.0, 'S')
    lon_a = (155, 30, 0, 'W')

    # 到达点
    lat_b = (26, 23, 48.0, 'N')
    lon_b = (143, 12, 0, 'E')

    # 执行计算
    results = calculate_great_circle(lat_a, lon_a, lat_b, lon_b)
    
    # --- 格式化输入显示 ---
    print("--- 航海计算器：大圆航线 ---")
    in_a_lat = f"{results['inputs']['lat_a_dms'][0]}° {results['inputs']['lat_a_dms'][1]}' {results['inputs']['lat_a_dms'][2]:.0f}\" {results['inputs']['lat_a_dms'][3]}"
    in_a_lon = f"{results['inputs']['lon_a_dms'][0]}° {results['inputs']['lon_a_dms'][1]}' {results['inputs']['lon_a_dms'][2]:.0f}\" {results['inputs']['lon_a_dms'][3]}"
    in_b_lat = f"{results['inputs']['lat_b_dms'][0]}° {results['inputs']['lat_b_dms'][1]}' {results['inputs']['lat_b_dms'][2]:.0f}\" {results['inputs']['lat_b_dms'][3]}"
    in_b_lon = f"{results['inputs']['lon_b_dms'][0]}° {results['inputs']['lon_b_dms'][1]}' {results['inputs']['lon_b_dms'][2]:.0f}\" {results['inputs']['lon_b_dms'][3]}"
    
    print(f"出发点 A: {in_a_lat}, {in_a_lon}")
    print(f"到达点 B: {in_b_lat}, {in_b_lon}")
    print("-" * 35)

    # --- 格式化输出显示 ---
    print(f"  航迹大圆航程: {results['distance_nm']:.2f} 海里 (NM)")
    print(f"  起始航向 (A): {results['initial_course_dms_str']} (真航向)")
    print(f"  到达航向 (B): {results['final_course_dms_str']} (真航向)")