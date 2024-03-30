# Documentation de la librairie de transition python -> sql
*J'utilise la librairie Psycopg2 pour communiquer avec une base de données SQL*


## 1. get_id(database) -> *dict*
La fonction get_id renvoie un dictionnaire comprenant les moyens de communiquer avec la base de données :
```txt
    {'database':database,    -> nom de la base de données
    'user':'postgres',      -> user du serveur
    'password':'bonjour',   -> mot de passe
    'host':'localhost',     -> host
    'port':5432}            -> port (le port par défaut est 5432 mais ça peut changer)
```
- Si l'argument base de données n'est pas renseigné, la fonction renverra simplement un dictionnaire avec le couple user, password. C'est utilisé notamment dans la fonction create_database
- Si vous avez configuré votre base de données avec d'autres identifiants, il faudra modifier cette fonction


## 2. log(message) -> *bool*
Cette fonction permet d'écrire des messages dans le fichier log.txt\
Si jamais la fonction n'arrive pas à écrire, elle renvoie `False`, sinon elle renvoie `True`


## 3. format_sql(data) -> *str*
La fonction permet de formater les données pour qu'elles soient adaptées à la syntaxe SQL :
```txt
string => 'string'
int => str(int)
liste(...) => ARRAY[...]
```

## 4. GET(database, tables, variable, valeur) -> *list[tuple]*
Cette fonction extrait des données d'une table SQL\
**Arguments :** nom de la base de données (string), nom de la (des) table(s) (liste de string), variable de sélection (en string), valeur de sélection (en string), identifiants = dictionnaire d'identifiants

### Cas d'usage 1 :
get('db_1', ['group']) -> renvoie le contenu de la table group de la base de données 'db_1'

### Cas d'usage 2 :
get('db_1', ['group', 'subnet']) -> renvoie le contenu de la table group JOINTE (inner join) avec la table subnet !\
**_IMPORTANT : la jointure se fait sur la variable premieretable.deuxiemetable_id = deuxiemetable.id_**\
(ex: group.subnet_id = subnet.id)\
La jointure ne peut se faire que sur deux tables

### Cas d'usage 3 :
get('db_1', ['group'], 'name', 'Vannes') -> renvoie le contenu de la table group, avec le filtre name = 'Vannes' (ie variable = 'valeur')\
**_IMPORTANT : je n'ai prévu pour l'instant qu'un seul filtre possible mais cela peut évoluer si besoin_**


## 5. PUT(database, table, data) -> *bool*
Cette fonction insère des données dans une table SQL\
**Arguments :** nom de la base de données (string), nom de la (des) table(s) (liste de string), données de l'élément à ajouter (dict de string), identifiants = dictionnaire d'identifiants\
Renvoie un booléen indiquant le succès de l'opération\
**_IMPORTANT : Si jamais un élément existe déjà, la fonction renverra le booléen `False`_**


## 6. DELETE(database, table, id) -> *bool*
Cette fonction supprime une entrée dans une table SQL\
**Arguments :** nom de la base de données (string), nom de la table (string), clé primaire de l'élément à supprimer (integer), identifiants = dictionnaire d'identifiants\
Renvoie un booléen indiquant le succès de l'opération\


## 7. create_database(name) -> *bool*
Cette fonction crée une database\
**Arguments :** nom de la base de données (string)\
Renvoie un booléen indiquant le succès de l'opération\


## 8. create_table(database, table_name) -> *bool*
Cette fonction crée une table dans une base de données\
Arguments : nom de la base de données (string), nom de la table (string)\
Renvoie un booléen indiquant le succès de l'opération\


## 9. add_column(database, table, column_name, type) -> *bool*
Cette fonction ajoute une colonne à une table d'une base de données\
**Arguments :** nom de la base de données (string), nom de la table (string), nom de la colonne (string), type de données de la colonne (type)\
Renvoie un booléen indiquant le succès de l'opération\


## 10. """user guide"""
Exemples de fonctions permettant d'illustrer un usage type de la librairie
```py
    create_database('database_1')
    create_table('database_1', 'table_1')
    add_column('database_1','table_1','column_1',int)
    add_column('database_1','table_1','column_2',str)
    add_column('database_1','table_1','column_3',bool)
    add_column('database_1','table_1','column_4',list[int])
    add_column('database_1','table_1','column_5',list[str])
    put('database_1','table_1',{f"column_{i}":val for i,val in enumerate([4,567,'oui',False,[9,8,7,6],['i','o','a']])})
    put('database_1','table_1',{f"column_{i}":val for i,val in enumerate([6,82,'oui',False,[9,8,7,6],['i','o','a']])})
    get('database_1',['table_1'])
    get('database_1',['table_1'],'column_1',82)
    delete('database_1','table_1',6)
```