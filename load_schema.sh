#!/bin/bash
psql -h localhost -p $PGPORT -d ${USER}_finalproj_DB -f create_tables.sql
psql -h localhost -p $PGPORT -d ${USER}_finalproj_DB -f backend/data/import_data.sql
echo "Loaded schema"