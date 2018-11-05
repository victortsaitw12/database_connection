# -*- coding: utf-8 -*-
import sys
import pymysql
import pyodbc 
import cx_Oracle
import json
from elasticsearch import Elasticsearch


class Connection(object):
    def __init__(self, conn_name, db):
        self.conn = None
        self.conn_name = conn_name
        self.db = db

        if conn_name == 'mysql':
            return self.connectMySQL()
        elif conn_name == 'mssql':
            return self.connectMSSQL()
        elif conn_name == 'oracle':
            return self.connectOracle()
        elif conn_name == 'elasticsearch':
            return self.connectElasticsearch()

    def getName(self):
        return self.conn_name

    def getDB(self):
        return self.db.lower()

    def connectMySQL(self):
        self.conn = pymysql.connect(host='10.149.7.20', 
                                    port=3306, 
                                    user='ibdo', 
                                    passwd='ibdo1234', 
                                    db='mes_db')
        return
 
    def connectMSSQL(self):
        server = '10.149.1.195,3000' 
        database = 'fqmdb' 
        username = 'IBDO' 
        password = 'ibdo!data' 
        self.conn = pyodbc.connect('DRIVER={ODBC Driver 17 for SQL Server};SERVER='+server+';DATABASE='+database+';UID='+username+';PWD='+ password)
        return

    def connectOracle(self):
        dsn = cx_Oracle.makedsn('10.132.128.66', 1521, 'D11')
        self.conn = cx_Oracle.connect("IBDO", "ibdo!data", dsn, encoding="UTF-8", nencoding="UTF-8")
        return

    def connectElasticsearch(self):
        self.conn = Elasticsearch([{'host':'elasticsearch','port':9200}])
        return

    def getCursor(self):
        return self.conn.cursor()

    def getConnection(self):
        return self.conn


class SQL2ELK(object):

    def __init__(self):
        self.oracle = Connection('oracle', 'D11')
        self.mysql = Connection('mysql', 'mes_db')
        self.mssql = Connection('mssql', 'fqmdb')
        self.es = Connection('elasticsearch', '')
        return 
    
    def getConnection(self, conn_name):
        if conn_name == self.mysql.getName():
            return self.mysql
        elif conn_name == self.oracle.getName():
            return self.oracle
        elif conn_name == self.mssql.getName():
            return self.mssql
        elif conn_name == self.es.getName():
            return self.es

    def getCursor(self, conn_name):
        return self.getConnection(conn_name).getCursor()

    def getAllTables(self, conn_name):
        if conn_name == self.mysql.getName():
            query = 'SHOW TABLES'
        elif conn_name == self.oracle.getName():
            query = 'SELECT table_name FROM all_tables'
        elif conn_name == self.mssql.getName():
            query = "SELECT name FROM sysobjects WHERE xtype='u'"

        with self.getCursor(conn_name) as cur:
            cur.execute(query)
            result = cur.fetchall()
        for row in result:
            yield row[0]


    def getAllRows(self, conn_name, table):
        if conn_name == 'oracle':
            table = 'SFC.' + table
        cols = []
        with self.getCursor(conn_name) as cur:
            try:
                cur.execute("SELECT * FROM %s" % table)
                result = cur.fetchall()
            except Exception as ex:
                print(ex)
                return

            # Prepare the column names
            for desc in cur.description:
                cols.append(desc[0])

        for row in result:
            yield zip(cols, row)

    def saveToElasticsearch(self, conn_name):
        conn = self.getConnection(conn_name)
        es = self.getConnection('elasticsearch').getConnection()
        for table in self.getAllTables(conn_name):
            if not table in ['MJ_BY', 'MJ_BY_DETAIL', 'MJ_BY_INFO', 'MJ_DAYLIHIT', 'MJ_MAT', 'MJ_PRODMS',
                             'tb_Check_EntityDetail', 'tb_Check_SizeDetail1', 'tb_CHeck_Function_Detail',
                             'tb_ZJCheck_Detail', 'tb_ZJCHeck_Detail_item']:
                continue
            for row in self.getAllRows(conn_name, table):
                print('=============' + table + '=================')
                data = dict()
                for col, value in row:
                    print('col:%s, value:%s' %(col, value))
                    data[col] = "'" + str(value) + "'"

                es.index(index=conn.getDB(), 
                         doc_type=table, 
                         body=data)

    def deleteIndices(self, conn_name):
        es = self.getConnection('elasticsearch').getConnection()
        if conn_name == self.oracle.getName():
            return es.indices.delete(index=self.oracle.getDB())

        if conn_name == self.mysql.getName():
            return es.indices.delete(index=self.mysql.getDB())

        if conn_name == self.mssql.getName():
            return es.indices.delete(index=self.mssql.getDB())

    def getSchema(self, table):
        if self.conn_name == 'mysql':
            query = 'desc ' + table 
        elif self.conn_name == 'oracle':
            query = 'desc all_tab_columns'

        print(query)
        schema = []
        with self.conn.cursor() as cur:
            cur.execute(query)
            result = cur.fetchall()
        for row in result:
            schema.append(row[0])
        return schema
    
    def parseSchema(self, schema):
        schema_str = ''
        for col in schema:
            schema_str = schema_str + col + ','
        return schema_str.strip(',')

    def getRows(self, schema, table):
        schema_str = self.parseSchema(schema)
        with self.conn.cursor() as cur:
            cur.execute("SELECT %s FROM %s" % (schema_str, table))
            result = cur.fetchall()
        for row in result:
            yield zip(schema, row)

if __name__ == '__main__':
    sql_2_elk = SQL2ELK()
    for db in sys.argv[1:]:
        print(db)
        try:
            sql_2_elk.deleteIndices(db)
        except:
            pass
        sql_2_elk.saveToElasticsearch(db)
