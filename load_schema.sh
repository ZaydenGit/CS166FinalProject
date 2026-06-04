#!/bin/bash
psql -h localhost -p $PGPORT -d ${USER}_finalproj_DB -f cs166_phase2_schema.sql
echo "Loaded schema"