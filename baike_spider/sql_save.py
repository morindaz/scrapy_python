import pymysql
db = pymysql.connect(host='127.0.0.1',user = 'root',passwd='maoshunyi888',db='sql_test',port=3306,charset='utf8')
cursor = db.cursor()
data = cursor.execute('SELECT * FROM `Persons`')
one = cursor.fetchone()
print(data)
print(one)