#!/bin/bash
cat<<'EOF'
  __  __      _        ____                   ____       _               
 |  \/  | ___| |_ __ _| __ )  __ _ ___  ___  / ___|  ___| |_ _   _ _ __  
 | |\/| |/ _ \ __/ _` |  _ \ / _` / __|/ _ \ \___ \ / _ \ __| | | | '_ \ 
 | |  | |  __/ || (_| | |_) | (_| \__ \  __/  ___) |  __/ |_| |_| | |_) |
 |_|  |_|\___|\__\__,_|____/ \__,_|___/\___| |____/ \___|\__|\__,_| .__/ 
                                                                  |_|    
EOF

source ../.env

if [ -z "$METABASE_DB_USER" ]; then
  echo "METABASE_DB_USER is not set"
  exit 1
fi
if [ -z "$METABASE_DB_PASSWORD" ]; then
  echo "METABASE_DB_PASSWORD is not set"
  exit 1
fi
cat<<EOF > ./sql/configure_metabase.sql
-- CREATE ROLE metabase NOSUPERUSER NOCREATEDB NOCREATEROLE NOINHERIT LOGIN NOREPLICATION NOBYPASSRLS PASSWORD '${METABASE_DB_PASSWORD}';
-- CREATE DATABASE metabase OWNER metabase ENCODING 'UTF8';

CREATE USER ${METABASE_DB_USER} WITH
    LOGIN
    NOSUPERUSER
    NOCREATEDB
    NOCREATEROLE
    NOINHERIT
    NOREPLICATION
    PASSWORD '${METABASE_DB_PASSWORD}'
;
CREATE DATABASE metabase OWNER ${METABASE_DB_USER} ENCODING 'UTF8';
GRANT ALL PRIVILEGES ON DATABASE metabase TO metabase;



--\c metabase;

EOF


## Run as 
## cat ./sql/configure_metabase.sql | podman-compose exec db psql -U postgres