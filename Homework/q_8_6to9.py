import sqlite3
import csv

def create_books_table():
    """创建books表（如果不存在）"""
    try:
        conn = sqlite3.connect('books.db')
        cursor = conn.cursor()
    
        create_table_sql = """
        CREATE TABLE IF NOT EXISTS books (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            title TEXT NOT NULL,
            author TEXT NOT NULL,
            year INTEGER
        )
        """
        cursor.execute(create_table_sql)
        conn.commit()
        print("表 'books' 已准备好")
        
    except sqlite3.Error as e:
        print(f"创建表时出错：{e}")
    finally:
        if conn:
            conn.close()
1
def import_csv_to_database(csv_filename):
    """从CSV文件读取数据并插入到数据库"""
    try:
        # 连接到数据库
        conn = sqlite3.connect('books.db')
        cursor = conn.cursor()
        
        #更新覆盖文本(自增)
        update_sql="TRUNCATE TABLE books"
        cursor.execute(update_sql)


        # 读取CSV文件
        with open(csv_filename, 'r', encoding='utf-8') as csv_file:
            csv_reader = csv.reader(csv_file)
            
            # 跳过标题行
            next(csv_reader)
            
            # 准备插入数据的SQL语句
            insert_sql = "INSERT INTO books (title, author, year) VALUES (?, ?, ?)"
            
            # 计数器
            success_count = 0
            error_count = 0
            
            # 遍历CSV文件的每一行
            for row in csv_reader:
                try:
                    # 确保行有足够的数据
                    if len(row) >= 3:
                        title = row[0].strip()
                        author = row[1].strip()
                        
                        # 处理年份（确保是整数）
                        try:
                            year = int(row[2].strip()) if row[2].strip() else None
                        except ValueError:
                            year = None
                            print(f"警告：'{title}' 的年份格式不正确: {row[2]}")
                        
                        # 插入数据
                        cursor.execute(insert_sql, (title, author, year))
                        success_count += 1
                    else:
                        print(f"跳过不完整的行: {row}")
                        error_count += 1
                        
                except Exception as e:
                    print(f"插入行时出错 {row}: {e}")
                    error_count += 1
                    continue
        
        # 提交事务
        conn.commit()
        print(f"\n数据导入完成！")
        print(f"成功插入: {success_count} 条记录")
        print(f"失败: {error_count} 条记录")
        
        # 显示插入的数据
        display_inserted_data(cursor)
        
    except FileNotFoundError:
        print(f"错误：找不到文件 '{csv_filename}'")
    except Exception as e:
        print(f"导入数据时发生错误：{e}")
        conn.rollback()  # 回滚事务
    finally:
        if conn:
            conn.close()

def display_inserted_data(cursor):
    """显示已插入的数据"""
    cursor.execute("SELECT * FROM books ORDER BY id")
    books = cursor.fetchall()
    
    print("\n当前数据库中的所有图书：")
    print("-" * 80)
    print(f"{'ID':<4} | {'Title':<40} | {'Author':<20} | {'Year'}")
    print("-" * 80)
    
    for book in books:
        print(f"{book[0]:<4} | {book[1]:<40} | {book[2]:<20} | {book[3]:<5}")
    
    print(f"\n总共 {len(books)} 本书籍")



# 主程序
if __name__ == "__main__":
    # 创建数据库表
    create_books_table()
    
    # 导入CSV数据到数据库
    import_csv_to_database('books.csv')
    
    print("\n操作完成！数据已从 books.csv 成功导入到 books.db 数据库")
    

def get_titles_alphabetically():
    """
    从books表中选择title列并按字母顺序输出
    """
    try:
        # 连接到数据库
        conn = sqlite3.connect('books.db')
        cursor = conn.cursor()
        
        # SQL查询：选择title列并按字母顺序排序
        sql_query = "SELECT title FROM books ORDER BY title ASC"
        
        # 执行查询
        cursor.execute(sql_query)
        
        # 获取所有结果
        titles = cursor.fetchall()
        
        # 输出结果
        if titles:
            print("图书标题（按字母顺序排序）：")
            print("-" * 50)
            
            for i, title_tuple in enumerate(titles, 1):
                # 每个结果是一个元组，取第一个元素就是标题
                print(f"{i:2d}. {title_tuple[0]}")
            
            print(f"\n总共找到 {len(titles)} 本书")
        else:
            print("数据库中没有找到任何图书")
            
    except sqlite3.Error as e:
        print(f"数据库查询出错：{e}")
    finally:
        if conn:
            conn.close()

if __name__ == "__main__":
    print("=" * 60)
    print("从 books 表中选择 title 列并按字母顺序输出")
    print("=" * 60)
    print("\n1. 基本版本：")

get_titles_alphabetically()
print("\n" + "=" * 60)

def get_books_by_publication_year():
    """
    从books表中选择所有列并按出版年份顺序输出
    """
    try:
        # 连接到数据库
        conn = sqlite3.connect('books.db')
        cursor = conn.cursor()
        
        # SQL查询：选择所有列并按年份升序排序
        sql_query = "SELECT * FROM books ORDER BY year ASC"
        
        # 执行查询
        cursor.execute(sql_query)
        
        # 获取所有结果
        books = cursor.fetchall()
        
        # 输出结果
        if books:
            print("图书信息（按出版年份升序排序）：")
            print("=" * 90)
            print(f"{'ID':<4} | {'Title':<40} | {'Author':<20} | {'Year'}")
            print("-" * 90)
            
            for book in books:
                print(f"{book[0]:<4} | {book[1]:<40} | {book[2]:<20} | {book[3]}")
            
            print(f"\n总共找到 {len(books)} 本书")
        else:
            print("数据库中没有找到任何图书")
            
    except sqlite3.Error as e:
        print(f"数据库查询出错：{e}")
    finally:
        if conn:
            conn.close()

if __name__ == "__main__":
    print("=" * 90)
    print("从 books 表中选择所有列并按出版年份顺序输出")
    print("=" * 90)
    
    # 基本版本：按年份升序排序
    print("\n1. 基本版本（按出版年份升序）：")
    get_books_by_publication_year()