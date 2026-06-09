# CS166FinalProject

Final Project for CS166 @ UCR

# Overview

This program is an implementation of a Database Management System (DBMS) in Python, using a terminal-based interface.
Because the implementation phase of this project was deliberately open-ended, I made a lot of deliberate design choices to help create a functioning product.
To make the code clean, readable, and extensible, I took inspiration from web development and seperated most of the files into frontend and backend folders. More on this later, first the program needs to actually be ran.

# Setup

CD into root directory, then run

```sh
source ./start_db.sh
source ./load_schema.sh
source ./stop_db.sh
```

## Import data from csvs

Run the following comamand to populate the database with data from the CSVs.

```sh
cs166_psql ${USER}_finalproj_DB < ./backend/data/import_data.sql
```

Then, run the following command to create indexes.

```sh
cs166_psql ${USER}_finalproj_DB < ./backend/data/create_index.sql
```

## Running

```sh
python3 frontend/main.py
```

see also: `python3 db_test.py`

# Usage

On first time use, you must register an account. To do this, just follow the on-screen menu.

... (screenshot here... etc) ...

From there, you can log in to the program and perform actions as a Buyer (by default).

Since this is supposed to be emulating an actual platform for sales, there is no way in the application to change yourself from a Buyer to a Seller or an Admin, if you only have access to a Buyer account.  
In order to change your role (since we have console access), type the following in the terminal:

```sh
cs166_psql ${USER}_finalproj_DB < UPDATE users SET role = 'Admin' WHERE login = '<username>';
```

Obviously, replacing "\<username>" with whichever username you chose.

The rest of the program is self-explanatory on how to interface with. Each role has a different view of the program as they have different permissions and actions that they can take.

# Justifications

Obviously, I can't cover every single design decision that I made while developing, so I will focus on the main ones (that I remember).

The frontend utilizes an approach similar to a state machine. Once a user logs in, their `session["role"]` acts as a token that directs them into a respective dashboard loop until they explicitly log out of the system. As mentioned above, there is no way to change your role inside of the client UNLESS you are an Admin.

Data displayed in the larger views (such as large lists of items, users) are managed by using pagination, that is, the `LIMIT` and `OFFSET` operators in SQL, to ensure that the ui remains clean enough in this environment. Because I have so much data to work with (see credits), it is not an option to just print everything out.

Pretty much everything in this was designed to be scalable. There are a few exceptions, such as there being static limits on some lengths of strings / numbers when displaying them. But if you don't consider that, as they are relatively trival fixes, the client easily works well with data in the thousands of rows. I cannot necessarily guarantee great performance since that, but I did take a few steps towards optimizing that in the form of indexes.

1. Foreign key indexes for JOIN operator optimizations. These indexes help massively in larger queries such as viewing an auction's bid history or pulling from a cart.
2. Partial indexes for browsing. The most heavily executed query in the entire system is Buyers searching the platform. Since buyers only really care about 'Active' status items, this index cuts down the size of the operations as it gets rid of the closed auctions that we don't really care about.
3. Sorting indexes. The seller dashboard queries multiple columns at once, so indexing these values accelerates the lookup. The `bid_timestamp DESC` index, for example, pre-sorts the bid history on the disk, which makes it so that this expensive operation doesn't have to be done every single time a user clicks in an auction view and views the previous bids.

Some other optimizations were done. I tried to implement limits in a few places, for example when getting the highest value for an auction (in the context of ending it), the bid history is sorted in descending order (which is already indexed) and we only take the first entry using `LIMIT 1`.

# References & Credits

https://www.psycopg.org/docs/module.html#module-psycopg2  
https://docs.python.org/3/library/os.html#os.environ

Sample Data CSVs: Hyrum Catanzaro  
<small style="color: lightgrey">(data generated was distinct from that used in his program, he made a script to generate it)</small>

Lecture slides and lab files

# Contributions

Zayden Middleton: Planned, designed, coded, and created writeup.
Neha Lloyd:
