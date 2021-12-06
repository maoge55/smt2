import pymssql
from pymssql import _mssql
from pymssql import _pymssql
import uuid
import decimal

#增
def insert(datas,table):
    conn = pymssql.connect('.', 'sa','123456', 'smt')
    with conn:
        with conn.cursor() as cursor:
            success=0;fail=0
            for data in datas:
                zdstr=','.join(data.keys())
                vals=tuple(data.values())
                sstr=''
                for j in range(len(vals)):
                    sstr+=r'%s'+','
                    if j==len(vals)-1:
                        sstr=sstr[:-1]
                sqlstr=f'insert into {table}({zdstr}) values({sstr})'
                try:
                    cursor.execute(sqlstr,vals)
                    success+=1
                except Exception as e:
                    #print(f"insert 出现错误 => {e}")
                    fail+=1
            conn.commit()
            return {'success':success,'fail':fail}
    
#删
def delete(where,table):
    conn = pymssql.connect('.', 'sa','123456', 'smt')
    with conn:
        with conn.cursor() as cursor:

            sqlstr=f'delete from {table} where {where}'
            try:
                cursor.execute(sqlstr)
                conn.commit()
                print(f"{table},删除成功")
            except Exception as e:
                print(f"{table},删除失败=>{e}")
            

#改

def update(set,where,table):
    conn = pymssql.connect('.', 'sa','123456', 'smt')
    with conn:
        with conn.cursor() as cursor:

            sqlstr=f'update {table} set {set} where {where}'
            try:
                cursor.execute(sqlstr)
                conn.commit()
                #print(f"{table},更新成功")
            except Exception as e:
                print(f"{table},更新失败=>{e}")
#查
def select(where,table):
    conn = pymssql.connect('.', 'sa','123456', 'smt')
    with conn:
        with conn.cursor(as_dict=True) as cursor:
            sql=f'select * from {table} where {where}'
            try:                    
                cursor.execute(sql)
                #print(f"{table},查询成功")
                res=cursor.fetchall()
                return res
            except Exception as e:
                print(f'{table}查询失败=> {e}')
                return []

#通用查询

def exe_sql(sql):
    try:
        conn = pymssql.connect('.', 'sa','123456', 'smt')
        with conn:
            with conn.cursor() as cursor:

                    cursor.execute(sql)
                    res=cursor.fetchall()
                    conn.commit()  #提交
                    return res
    except Exception as e:
        print(f'{sql}执行失败 => {e}')

# 通用查询2

def exe_sql2(sql,vals):
    try:
        conn = pymssql.connect('.', 'sa','123456', 'smt')
        with conn:
            with conn.cursor(as_dict=True) as cursor:

                    cursor.execute(sql,vals)
                    res=cursor.fetchall()
                    conn.commit()  #提交
                    return res
    except Exception as e:
        print(f'{sql}执行失败 => {e}')

