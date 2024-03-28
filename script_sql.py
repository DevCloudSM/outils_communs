import psycopg2
from psycopg2 import OperationalError

def create_database(database_name):
    try:
        # Paramètres de connexion
        db_params = {
            'user': 'postgres',
            'password': 'bonjour',
            'host': 'localhost',
            'port': 5432
        }

        # Connexion au serveur PostgreSQL pour créer la base de données
        conn = psycopg2.connect(**db_params)

        # Création d'un nouveau curseur
        conn.autocommit = True
        cursor = conn.cursor()

        # Création de la base de données
        cursor.execute(f"CREATE DATABASE {database_name};")
        print(f"Base de données '{database_name}' créée avec succès!")

    except OperationalError as e:
        print(f"Erreur: {e}")


def create_table(database_name, table_name):
    try:
        # Paramètres de connexion pour se connecter à la base de données
        db_params = {
            'database': database_name,
            'user': 'postgres',
            'password': 'bonjour',
            'host': 'localhost',
            'port': 5432
        }

        # Connexion à la base de données
        conn = psycopg2.connect(**db_params)

        # Création d'un nouveau curseur pour la base de données
        conn.autocommit = True
        cursor = conn.cursor()

        # Vérifier si la table existe déjà
        cursor.execute(f"SELECT EXISTS (SELECT 1 FROM information_schema.tables WHERE table_name = '{table_name}');")
        table_exists = cursor.fetchone()[0]

        if not table_exists:
            # Création de la table
            cursor.execute(f"CREATE TABLE {table_name} (id SERIAL PRIMARY KEY, licence VARCHAR(50));")
            print(f"Table '{table_name}' créée avec succès dans la base de données '{database_name}'!")
        else:
            print(f"La table '{table_name}' existe déjà dans la base de données '{database_name}'.")

    except OperationalError as e:
        print(f"Erreur: {e}")

if __name__ == "__main__":
    # Créer une base de données
    create_database("database_licences")

    # Créer une table dans la base de données
    create_table("database_licences", "matable_sql")
