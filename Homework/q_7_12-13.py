from binascii import unhexlify

# 将两行十六进制字符串合并
hex_string = '47494638396101000100800000000000ffffff21f9' + '0401000000002c000000000100010000020144003b'

# 使用 unhexlify 转换为 bytes
gif = unhexlify(hex_string)

# 打印结果
print("gif 变量类型:", type(gif))
print("gif 内容:", gif)
print("gif 长度:", len(gif), "字节")
print("gif 十六进制表示:", gif.hex())
# 验证是否是GIF文件
if gif.startswith(b'GIF'):
    print("这是一个有效的GIF文件!")
    print("GIF版本:", gif[3:6].decode())
else:
    print("这不是一个GIF文件")