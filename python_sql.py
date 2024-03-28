from typing import Union
import psycopg2 as ps

identifiants = {'database':'ipam',
                'user':'postgres',
                'password':'bonjour',
                'host':'localhost',
                'port':5432}

def log(message:str) -> bool:
    try:
        with open("log.txt","a",encoding="utf-8") as file:
            file.write(message)
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

def get(tables:list[str], variable:str="", valeur:str="", identifiants:dict[str, str]=identifiants) -> list[tuple]:
    with ps.connect(**identifiants) as connector:
        with connector.cursor() as cursor:
            if len(tables) >= 3:
                return [('Erreur')]
            commande = f'select * from public."{tables[0]}"'
            if len(tables) == 2:
                commande += f' inner join public."{tables[1]}" on public."{tables[0]}".{tables[1]}_id = public."{tables[1]}".id'
            if variable:
                commande+= f" where {variable} = '{valeur}'"
            cursor.execute(commande)
            return cursor.fetchall()

def put(table:str, data:dict[str,str], identifiants:dict[str, str]=identifiants) -> bool:
    try:
        with ps.connect(**identifiants) as connector:
            with connector.cursor() as cursor:
                cursor.execute(f"""
                                insert into public."{table}" values ({", ".join([format_sql(x) for x in data.values()])})
                                """)
                connector.commit()
                return True
    except:
        return False

def delete(table:str, id:int, identifiants:dict[str, str]=identifiants) -> bool:
    try:
        with ps.connect(**identifiants) as connector:
            with connector.cursor() as cursor:
                cursor.execute(f"""
                                delete from public."{table}" where id = {id}
                                """)
                connector.commit()
                return cursor.rowcount > 0
    except:
        return False

if __name__ == '__main__':
    """User guide de la librairie"""
    print(get(["IP_address"]))
    print(get(["group"], 'name', 'Vannes'))
    print(put(table="IP_address", data={'id':6, 'address': "10.4.2.1"}))
    print(delete("group", 1))
    print(delete("group", 3))
    print(put("subnet", {'id':5, 'first@':'10.0.0.2', 'gp_id':1}))
    print(put("group", {'id':3, 
                        'name':'Brest', 
                        'p_id':1, 
                        'c_ids':[1,4,6], 
                        'r_r':['dl','sa'], 
                        'w_r':['sa']}))