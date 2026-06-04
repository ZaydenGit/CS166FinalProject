#! /bin/bash
echo "Starting CS166 postgresql"
cs166_initdb
cs166_db_start
cs166_db_status

echo "Creating db named "$USER"_finalproj_DB"
cs166_createdb $USER'_finalproj_DB'
cs166_db_status


