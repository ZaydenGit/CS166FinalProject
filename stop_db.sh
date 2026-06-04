#! /bin/bash
echo "Stopping CS166 postgresql and db"
cs166_db_stop 
cs166_db_status
#pg_ctl -o "-c unix_socket_directories=$PGSOCKETS -p $PGPORT" -D $PGDATA -l $folder/logfile stop
