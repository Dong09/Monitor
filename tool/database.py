import pymysql
import datetime

# NpoZ82>-gW>u

#打开数据库连接
def db_operate(table,data):
    
    db = pymysql.connect(host='localhost',
                        user='root',
                        password='123456',
                        db='project2')
    #获取操作游标
    cursor = db.cursor()

    try:
        cursor.execute(f"insert into {table} values{data}")
        db.commit()
    except:
        db.rollback()

    #查询操作
    cursor.execute(f'SELECT * from {table}')
    data = cursor.fetchall()
    print(data)
    #关闭数据库连接
    db.close()


if __name__ == '__main__':
    data = (1,'classroom','front')
    db_operate('areainfo',data)