Ceci est la documentation de la librairie de transition python -> sql :<br>
J'utilise la librairie Psycopg2 pour communiquer avec une database sql


# 1. get_id(database) -> dictionnaire :
La fonction get_id renvoie un dictionnaire comprenant les moyens de communiquer avec la database :
    {'database':database,    -> nom de la database <br>
    'user':'postgres',      -> user du serveur <br>
    'password':'bonjour',   -> mot de passe <br>
    'host':'localhost',     -> host <br>
    'port':5432}            -> port (le port par défaut est 5432 mais ça peut changer) <br>

- Si l'argument database n'est pas renseigné, la fonction renverra simplement un dictionnaire avec le couple user, password <br>
  C'est utilisé nottament dans la fonction create_database
- Si vous avez configuré votre database avec d'autres identifiants, il faudra modifier cette fonction


# 2. log(message) -> bool :
Cette fonction permet d'écrire des messages dans le fichier log.txt <br>
Si jamais la fonction n'arrive pas à écrire, elle renvoie False, sinon elle renvoie True


# 3. format_sql(data) -> str :
La fonction permet de formatter les données pour qu'elles soient adaptées à la syntaxe SQL : <br>
string => 'string' <br>
int => str(int) <br>
liste(...) => ARRAY[...]


# 4. GET(database, tables, variable, valeur) -> list[tuple]
Cette fonction extrait des données d'une table SQL <br>
Arguments : nom de la database (string), nom de la (des) table(s) (liste de string), variable de sélection (en string), valeur de sélection (en string), identifiants = dictionnaire d'identifiants

Cas d'usage 1 :
get('db_1', ['group']) -> renvoie le contenu de la table group de la database 'db_1'

Cas d'usage 2 :
get('db_1', ['group', 'subnet']) -> renvoie le contenu de la table group JOINTE (inner join) avec la table subnet !
IMPORTANT : la jointure se fait sur la variable premieretable.deuxiemetable_id = deuxiemetable.id  <br>
(ex: group.subnet_id = subnet.id) <br>
La jointure ne peut se faire que sur deux tables

Cas d'usage 3 :
get('db_1', ['group'], 'name', 'Vannes') -> renvoie le contenu de la table group, avec le filtre name = 'Vannes' (ie variable = 'valeur') <br>
IMPORTANT : je n'ai prévu pour l'instant qu'un seul filtre possible mais cela peut évoluer si besoin


# 5. PUT(database, table, data) -> bool:
Cette fonction insère des données dans une table SQL <br>
Arguments : nom de la database (string), nom de la (des) table(s) (liste de string), données de l'élément à ajouter (dict de string), identifiants = dictionnaire d'identifiants <br>
Renvoie un booléen indiquant le succès de l'opération <br>
IMPORTANT Si jamais un élément existe déjà, la fonction renverra le booléen False


# 6. DELETE(database, table, id) -> bool:
Cette fonction supprime une entrée dans une table SQL <br>
Arguments : nom de la database (string), nom de la table (string), clé primaire de l'élément à supprimer (integer), identifiants = dictionnaire d'identifiants <br>
Renvoie un booléen indiquant le succès de l'opération


# 7. create_database(name) -> bool:
Cette fonction crée une database <br>
Arguments : nom de la database (string) <br>
Renvoie un booléen indiquant le succès de l'opération


# 8. create_table(database, table_name) -> bool:
Cette fonction crée une table dans une database <br>
Arguments : nom de la database (string), nom de la table (string) <br>
Renvoie un booléen indiquant le succès de l'opération


# 9. add_column(database, table, column_name, type) -> bool:
Cette fonction ajoute une column à une table d'une database <br>
Arguments : nom de la database (string), nom de la table (string), nom de la colomne (string), type de données de la colomne (type) <br>
Renvoie un booléen indiquant le succès de l'opération


# 10. """user guide"""
Exemples de fonctions permettant d'illustrer un usage type de la librairie <br>
    create_database('database_1') <br>
    create_table('database_1', 'table_1') <br>
    add_column('database_1','table_1','column_1',int) <br>
    add_column('database_1','table_1','column_2',str) <br>
    add_column('database_1','table_1','column_3',bool) <br>
    add_column('database_1','table_1','column_4',list[int]) <br>
    add_column('database_1','table_1','column_5',list[str]) <br>
    put('database_1','table_1',{f"column_{i}":val for i,val in enumerate([4,567,'oui',False,[9,8,7,6],['i','o','a']])}) <br>
    put('database_1','table_1',{f"column_{i}":val for i,val in enumerate([6,82,'oui',False,[9,8,7,6],['i','o','a']])}) <br>
    get('database_1',['table_1']) <br>
    get('database_1',['table_1'],'column_1',82) <br>
    delete('database_1','table_1',6)
