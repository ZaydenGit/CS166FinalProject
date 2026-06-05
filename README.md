# CS166FinalProject

Final Project for CS166 @ UCR

# Setup

CD into root directory, then run

```sh
source ./start_db.sh
source ./load_schema.sh
source ./stop_db.sh
```

## Import data from csvs

Run the following comamand to import data from the CSVs into the database

```sh
cs166_psql ${USER}_finalproj_DB < ./backend/data/import_data.sql
```

## Running

```sh
python3 frontend/main.py
```

see also: `python3 db_test.py`

# References

https://www.psycopg.org/docs/module.html#module-psycopg2
https://docs.python.org/3/library/os.html#os.environ

# Credits

Sample Data CSVs: Hyrum Catanzaro  
<small style="color: lightgrey">(data generated was distinct from that used in his program, he made a script to generate it)</small>

# Contributions
