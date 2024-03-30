from typing import Union
import psycopg2 as ps
from psycopg2 import OperationalError
import traceback

def get_id(database:str='') -> dict[str,str]:
     if database :
         return {'database': database,
            'user':'postgres',
            'password':'bonjour',
            'host': 'localhost',
            'port': 5432}
     return {'user':'postgres',
             'password':'bonjour'}

def log(message:str) -> bool:
    try:
        with open("log.txt","a",encoding="utf-8") as file:
            file.write(f'\n{message}')
        return True
    except:
        return False

def format_sql(data:Union[str, int, list[str], list[int], bool]) -> str:
    if type(data) == str:
        return f"'{data}'"
    if type(data) == list:
        if len(data) == 0:
            return
        return f'ARRAY[{", ".join([format_sql(x) for x in data])}]'
    return str(data)

def get(database:str, tables:list[str], variable:str="", valeur:str="") -> list[tuple]:
    try:
        id = get_id(database)
        with ps.connect(**id) as connector:
            with connector.cursor() as cursor:
                if len(tables) >= 3:
                    return [('Erreur')]
                commande = f'select * from public."{tables[0]}"'
                if len(tables) == 2:
                    commande += f' inner join public."{tables[1]}" on public."{tables[0]}".{tables[1]}_id = public."{tables[1]}".id'
                if variable:
                    commande+= f" where {variable} = {format_sql(valeur)}"
                cursor.execute(commande)
                return cursor.fetchall()
    except:
        return [()]

def put(database:str, table:str, data:dict[str,str]) -> bool:
    try:
        id = get_id(database)
        with ps.connect(**id) as connector:
            with connector.cursor() as cursor:
                cursor.execute(f"""
                                insert into public."{table}" values ({", ".join([format_sql(x) for x in data.values()])})
                                """)
                connector.commit()
                return True
    except:
        return False

def delete(database:str, table:str, id:int) -> bool:
    try:
        identifiants = get_id(database)
        with ps.connect(**identifiants) as connector:
            with connector.cursor() as cursor:
                cursor.execute(f"""
                                delete from public."{table}" where id = {id}
                                """)
                connector.commit()
                return cursor.rowcount > 0
    except:
        traceback.print_exc()
    
def create_database(name:str='database_1') -> bool:
    try:
        id = get_id()
        conn = ps.connect(**id)
        conn.autocommit = True
        cursor = conn.cursor()
        cursor.execute(f"CREATE DATABASE {name}")
        cursor.close()
        conn.close()
        return True
    except:
        return False

def create_table(database:str, table_name:str) -> bool:
    try:
        id = get_id(database)
        with ps.connect(**id) as conn:
            conn.autocommit = True
            with conn.cursor() as cursor:
                cursor.execute(f"SELECT EXISTS (SELECT 1 FROM information_schema.tables WHERE table_name = '{table_name}');")
                table_exists = cursor.fetchone()[0]
                if not table_exists:
                    cursor.execute(f"CREATE TABLE {table_name} (id SERIAL PRIMARY KEY)")
                return not table_exists
    except:
        return False
    
def add_column(database:str, table:str, column_name:str, type:type) -> bool:
    try:
        id = get_id(database)
        conversion = {int:'integer',
                      str:'text',
                      bool:'boolean',
                      bool:'boolean',
                      list[int]:'integer[]',
                      list[str]:'text[]'}
        with ps.connect(**id) as conn:
            conn.autocommit = True
            with conn.cursor() as cursor:
                cursor.execute(f"SELECT EXISTS (select 1 from information_schema.columns where table_name = '{table}' and column_name = '{column_name}')")
                column_exists = cursor.fetchone()[0]
                if not column_exists:
                    cursor.execute(f"""
                                   ALTER TABLE {table}
                                   ADD {column_name} {conversion[type]}
                                   """)
                return not column_exists
    except:
        traceback.print_exc()

if __name__ == '__main__':
    """User guide de la librairie"""
    print(create_database('database_1'))
    print(create_table('database_1', 'table_1'))
    print(add_column('database_1','table_1','column_1',int))
    print(add_column('database_1','table_1','column_2',str))
    print(add_column('database_1','table_1','column_3',bool))
    print(add_column('database_1','table_1','column_4',list[int]))
    print(add_column('database_1','table_1','column_5',list[str]))
    print(put('database_1','table_1',{f"column_{i}":val for i,val in enumerate([4,567,'oui',False,[9,8,7,6],['i','o','a']])}))
    print(put('database_1','table_1',{f"column_{i}":val for i,val in enumerate([6,82,'oui',False,[9,8,7,6],['i','o','a']])}))
    print(get('database_1',['table_1']))
    print(get('database_1',['table_1'],'column_1',82))
    print(delete('database_1','table_1',6))
    """
    print(get(["address"]))
    print(get(["group"], 'name', 'Vannes'))
    print(put(table="address", data={'id':6, 'address': "10.4.2.1"}))
    print(delete("group", 1))
    print(delete("group", 3))
    print(put("subnet", {'id':5, 'first@':'10.0.0.2', 'gp_id':1}))
    print(put("group", {'id':3, 
                        'name':'Brest', 
                        'p_id':1, 
                        'c_ids':[1,4,6], 
                        'r_r':['dl','sa'], 
                        'w_r':['sa']}))
    """
