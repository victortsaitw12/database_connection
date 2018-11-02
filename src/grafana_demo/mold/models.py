from django.db import models
import pyodbc 
# Create your models here.
server = '10.149.1.195,3000' 
database = 'fqmdb' 
username = 'IBDO' 
password = 'ibdo!data' 
cnxn = pyodbc.connect('DRIVER={ODBC Driver 17 for SQL Server};SERVER='+server+';DATABASE='+database+';UID='+username+';PWD='+ password)

def badMaterials():
    result = {}
    with cnxn.cursor() as cursor:
        cursor.execute('''
            SELECT f_MaterialNumber, count(*) FROM dbo.tb_Check_Badness GROUP BY f_MaterialNumber
        ''')
        row = cursor.fetchone() 
        while row: 
            meterial_no = row[0]
            count = row[1]
            result[meterial_no] = count
            row = cursor.fetchone()

    return result
