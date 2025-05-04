
# Projet Flask : API REST Utilisateurs et Rôles

Ce projet Flask permet de lancer une application qui expose une API REST pour :

- **Créer des utilisateurs**
- **Se connecter (login)**
- **Assigner des rôles aux utilisateurs**
- **Contrôler l’accès à certaines routes en fonction des rôles**
- **Accéder et manipuler des données simples**  
  *(via SQLAlchemy, avec une base comme SQLite ou PostgreSQL)*

---

## Architecture du Projet

```
├── app
│   ├── database.py
│   ├── __init__.py
│   ├── models
│   │   ├── __init__.py
│   │   ├── table.py
│   │   └── user.py
│   └── routes
│       ├── allowed.py
│       ├── __init__.py
│       ├── table.py
│       └── user.py
├── config.py
├── docker-compose.yml
├── Dockerfile
├── instance
│   └── test.db
├── readme.txt
├── requirements.txt
├── run.py
└── tests
    ├── test_docker.py
    ├── test_get_data.py
    └── test_user.py
```

---

## Configuration et Tests

### 1. Créer un environnement virtuel et installer les dépendances

```bash
python -m venv env
pip install -r requirements.txt
```

### 2. Lancer les tests

```bash
export PYTHONPATH=$(pwd)
pytest tests/test_user.py tests/test_get_data.py -v
```

### 3. Lancer l’application avec Docker

```bash
docker compose up db
docker compose up web
```

### 4. Nettoyer la base de données

Pour réinitialiser la base de données, utilisez cette commande SQL dans Docker :

```bash
docker exec -it usermanagerapp-db-1 psql -U myuser -d mydb
```

Puis exécutez le code SQL suivant pour vider les tables :

```sql
DO $$ DECLARE
    r RECORD;
BEGIN
    FOR r IN (SELECT tablename FROM pg_tables WHERE schemaname = 'public') LOOP
        EXECUTE 'TRUNCATE TABLE public.' || r.tablename || ' RESTART IDENTITY CASCADE';
    END LOOP;
END $$;
```

---

## Tests de la Base de Données avec Docker

Les tests pour Docker sont disponibles dans le fichier `test_docker.py`.