import pyodbc 
# Some other example server values are
# server = 'localhost\sqlexpress' # for a named instance
# server = 'myserver,port' # to specify an alternate port
server = '10.149.1.195,3000' 
database = 'fqmdb' 
username = 'IBDO' 
password = 'ibdo!data' 
cnxn = pyodbc.connect('DRIVER={ODBC Driver 17 for SQL Server};SERVER='+server+';DATABASE='+database+';UID='+username+';PWD='+ password)
cursor = cnxn.cursor()
cursor.execute("SELECT @@version;")
cursor.execute('''
SELECT * FROM dbo.tb_Check_Badness
''')
row = cursor.fetchone() 
while row: 
    print(row)
    row = cursor.fetchone()
