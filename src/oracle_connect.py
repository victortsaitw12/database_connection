import cx_Oracle
ip = '10.132.128.66'
port = 1521
service = 'D11'

dsn = cx_Oracle.makedsn(ip,port,service)

connection = cx_Oracle.connect("IBDO", "ibdo!data", dsn)

cursor = connection.cursor()
cursor.execute('''
    SELECT * FROM SFC.MJ_BY_DETAIL
''')

rows = cursor.fetchall()
print(rows)
