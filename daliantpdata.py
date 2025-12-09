import requests
import json
import time
import pandas as pd
from datetime import datetime

# ========== 用户配置 ==========
API_KEY     = "替换成你的高德Key"  # 👉 去 https://lbs.amap.com 注册92c513d891e281c6c9a3446f7eda7565
API_URL     = "https://restapi.amap.com/v3/traffic/status/rectangle"

# 大连主城区范围（中山区-西岗区-沙河口区）
RECTANGLE   = "121.55,38.85;121.70,38.95"

OUTPUT_CSV  = "dalian_traffic.csv"
INTERVAL    = 300  # 每5分钟采一次
# ===============================

def fetch_traffic():
    """从高德API获取大连实时交通数据"""
    params = {
        "key": API_KEY,
        "rectangle": RECTANGLE,
        "output": "json",
        "extensions": "all"
    }
    resp = requests.get(API_URL, params=params, timeout=10)
    resp.raise_for_status()
    data = resp.json()
    return data

def parse_data(raw):
    """解析高德返回的JSON数据"""
    traffic_info = raw.get("trafficinfo", {})
    roads = traffic_info.get("roads", [])

    rows = []
    for r in roads:
        rows.append({
            "time": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
            "name": r.get("name"),
            "status": r.get("status"),  # 状态（畅通、缓行、拥堵等）
            "direction": r.get("direction"),
            "speed": r.get("speed"),    # 平均速度 km/h
            "angle": r.get("angle")
        })
    df = pd.DataFrame(rows)
    return df

def save_data(df):
    """将结果追加保存为CSV文件"""
    header = False
    try:
        with open(OUTPUT_CSV, "r", encoding="utf-8"):
            header = True
    except FileNotFoundError:
        header = False

    df.to_csv(OUTPUT_CSV, mode='a', index=False, header=not header, encoding='utf-8-sig')
    print(f"✅ {datetime.now()} 已保存 {len(df)} 条数据。")

def main_loop():
    print(f"🚦 开始采集大连实时交通数据：{RECTANGLE}")
    while True:
        try:
            raw = fetch_traffic()
            df = parse_data(raw)
            if not df.empty:
                save_data(df)
            else:
                print("⚠️ 未返回有效道路数据。")
        except Exception as e:
            print("❌ 发生错误：", e)

        print(f"⏳ 等待下次采集 ({INTERVAL} 秒)...\n")
        time.sleep(INTERVAL)

if __name__ == "__main__":
    main_loop()
