import re
import sqlite3
from typing import Optional,Dict

class mobilesuit():
    def __init__(self,db_name:str="mobilesuit.db"):
        self.db_name=db_name
        self.buildup_db()

    def buildup_db(self):
        conn=sqlite3.connect(self.db_name)
        cursor=conn.cursor()
        buildup_sql='''
        CREATE TABLE IF NOT EXISTS mobile_suits (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            suit_code VARCHAR(20) UNIQUE NOT NULL,
            suit_name VARCHAR(100) NOT NULL)'''
        cursor.execute(buildup_sql)
        input_sql='''
        INSERT OR IGNORE INTO mobile_suits (
            suit_code,suit_name) VALUES (?,?)'''
        
 # 插入示例数据
        sample_data = [
            ('RX-78-2', 'GUNDAM'),
            ('MS-06S', 'ZAKU'),
            ('MSZ-006', 'ZETA GUNDAM'),
            ('RX-93', 'ν GUNDAM')
        ]

        cursor.executemany(input_sql,sample_data)
        conn.commit()
        conn.close()
    
    def get_data(self,input_code:str)->Optional[str]:
        pattern= r'[A-Z]{1,5}\d*-?\d*[A-Z]*\d*-?\d*'
        match=re.search(pattern,input_code.upper())
        if match:
            suit_code = match.group()
            print(f"提取到的机体编号: {suit_code}")
            return suit_code
        else:
            print("未找到有效的机体编号格式")
            return None

    def search_in_code(self,suit_code:str):
        conn=sqlite3.connect(self.db_name)
        cursor=conn.cursor()
        cursor.execute("SELECT suit_code,suit_name FROM \
                       mobile_suits WHERE suit_code=?",(suit_code,))#元组形式
        result=cursor.fetchone()
        if result:
            return{'code':result[0],'name':result[1]}#创建返回字典
        cursor.execute("SELECT suit_code,suit_name FROM \
                       mobile_suits WHERE suit_code LIKE ?"\
                       ,f'%{suit_code}%')#前后加%实现模糊搜索
        results=cursor.fetchall()
        if results:
            print("The similar results")
            for i,(code,name) in enumerate(results,1):
                print(f'{i}.{code}-{name}')
                # 如果有多个结果，让用户选择
            if len(results) > 1:
                choice = input("请选择编号 (直接回车选择第一个): ").strip()
                idx = int(choice) - 1 if choice.isdigit()\
                      and 0 < int(choice) <= len(results) else 0
                return {'code': results[idx][0], 'name': results[idx][1]}
            else:
                return {'code': results[0][0], 'name': results[0][1]}   
        return None
    
    def add_new(self, suit_code: str, suit_name: str)->bool:
        conn = sqlite3.connect(self.db_name)
        cursor = conn.cursor()
        try:
            cursor.execute("INSERT INTO mobile_suits (suit_code,suit_name)\
                            VALUES(?,?)",(suit_code.upper(),suit_name))
            conn.commit()
            print(f"成功添加机体: {suit_code} - {suit_name}")
            return True
        except sqlite3.IntegrityError:
            print(f"机体编号 {suit_code} 已存在")
            return False
        finally:
            conn.close()

    def del_old(self,suit_code:str):
        conn=sqlite3.connect(self.db_name)
        cursor=conn.cursor()
        cursor.execute("DELETE FROM mobile_suits WHERE suit_code=?",(suit_code,))#数据库中元组
        conn.commit()
        return None
        conn.close()

    def output_data(self):
        conn=sqlite3.connect(self.db_name)
        cursor=conn.cursor()
        cursor.execute("SELECT * FROM mobile_suits ORDER BY suit_code")
        data=cursor.fetchall()
        print("所有机体名")
        for suits in data:
            print(f"{suits[0]:<4} | {suits[1]:<40} | {suits[2]:<20}")
        conn.close()

    #删除功能
    # 编号问题    
    #根据名字搜索
    #更新数据

def main():
    db=mobilesuit()
    while True:
        print("\n=== 机体数据库搜索系统 ===")
        print("1. 搜索机体")
        print("2. 添加新机体")
        print("3. 删除已有机体")
        print("4. 显示所有机体")
        print("5. 退出")
        
        choice = input("请选择操作 (1-5): ").strip()
        
        if choice == '1':
            # 搜索机体
            user_input = input("请输入机体编号或包含编号的文本: ").strip()
            
            if user_input:
                suit_code = db.get_data(user_input)#得到字符串
                
                if suit_code:
                    result = db.search_in_code(suit_code)#得到字典
                    if result:
                        print(f"\n搜索结果: {result['code']} - {result['name']}")
                    else:
                        print(f"未找到编号为 {suit_code} 的机体")
                        add_new = input("是否添加到数据库? (y/n): ").lower()
                        if add_new == 'y':
                            name = input("请输入机体名称: ").strip()
                            if name:
                                db.add_new(suit_code, name)
        
        elif choice == '2':
            # 添加新机体
            code = input("请输入机体编号: ").strip().upper()
            name = input("请输入机体名称: ").strip()
            
            if code and name:
                db.add_new(code, name)
            else:
                print("编号和名称不能为空")
        
        elif choice=='3':
            #删除机体
            user_input = input("请输入机体编号或包含编号的文本: ").strip()
            
            if user_input:
                suit_code = db.get_data(user_input)
                
                if suit_code:
                    db.del_old(suit_code)
                    print(f"机体{suit_code}已删除")
                    db.output_data()
                else:
                    print(f"未找到编号为 {suit_code} 的机体")


        elif choice == '4':
            # 显示所有机体
            db.output_data()
        
        elif choice == '5':
            print("感谢使用，再见！")
            break
        
        else:
            print("无效选择，请重新输入")

if __name__ == "__main__":
    main()

#测试输出
#TEST=mobilesuit()


