import csv

# 定义要保存的数据
data = [
    ['author', 'book'],
    ['J R R Tolkien', 'The Hobbit'],
    ['Lynne Truss', 'Eats, Shoots & Leaves']
]

# 写入CSV文件
with open('books.csv', 'w', newline='', encoding='utf-8') as file:
    writer = csv.writer(file)
    writer.writerows(data)

print("books.csv 文件已成功创建！")

# 验证文件内容
print("\n文件内容：")
with open('books.csv', 'r', encoding='utf-8') as file:
    content = file.read()
    print(content)


# 使用DictReader读取CSV文件
with open('books.csv', 'r', encoding='utf-8') as file:
    books = list(csv.DictReader(file))

# 输出变量books的值
print("books变量的值:")
print(books)
print("\n详细内容:")
for i, book in enumerate(books, 1):
    print(f"第{i}本书: 作者={book['author']}, 书名={book['book']}")

# 验证DictReader是否能正确处理引号和逗号
print("\n验证第二本书的处理:")
second_book = books[1]
print(f"作者: {second_book['author']}")
print(f"书名: {second_book['book']}")
print(f"书名类型: {type(second_book['book'])}")
print(f"书名长度: {len(second_book['book'])}")
print(f"书名是否包含逗号: {',' in second_book['book']}")

import csv

# 定义要保存的数据
data = [
    ['title', 'author', 'year'],
    ['The Weirdstone of Brisingamen', 'Alan Garner', '1960'],
    ['Perdido Street Station', 'China Miéville', '2000'],
    ['Thud!', 'Terry Pratchett', '2005'],
    ['The Spellman Files', 'Lisa Lutz', '2007'],
    ['Small Gods', 'Terry Pratchett', '1992']
]

# 写入CSV文件
with open('books.csv', 'w', newline='', encoding='utf-8') as file:
    writer = csv.writer(file)
    writer.writerows(data)

print("books.csv 文件已成功创建！")

# 验证文件内容
print("\n文件内容：")
with open('books.csv', 'r', encoding='utf-8') as file:
    content = file.read()
    print(content)

# 使用DictReader读取并显示数据
print("\n使用DictReader读取数据：")
with open('books.csv', 'r', encoding='utf-8') as file:
    reader = csv.DictReader(file)
    books = list(reader)
    for book in books:
        print(f"书名: {book['title']}, 作者: {book['author']}, 年份: {book['year']}")