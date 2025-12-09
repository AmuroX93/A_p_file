import unicodedata

# 创建Unicode字符串
mystery = '\U0001f4a9'

# 打印字符串
print(mystery)

# 查看Unicode名称
name = unicodedata.name(mystery)
print(f"Unicode名称: {name}")

pop_bytes=mystery.encode('utf-8')
print(f"字节型：{pop_bytes}")

pop_string=pop_bytes.decode('utf-8')
print(f"字符型：{pop_string}")