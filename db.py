import psycopg2

conn = psycopg2.connect(
    dbname='terminal_cw18',
    user='postgres',
    password='12345678',
    host='localhost',
    port='4060'
)
cur = conn.cursor()
table1 = """
create table users (user_id serial primary key,
name varchar(300) not null,last_name varchar(300) not null,
username varchar(300) unique not null,
password varchar (300) not null,
wallet_balance int);
"""
table2 = """
create table trip(
trip_id serial primary key,
origin varchar(300)  not null,
destination varchar(300) not null,
trip_date date not null,
price int not null);
"""
table3 = """
create table ticket(
ticket_id serial primary key,
user_id int not null,
trip_id int not null,
type varchar(300) not null,
foreign key (user_id) references users(user_id) 
,foreign key (trip_id) references trip(trip_id) 
 );
"""
cur.execute(table3)
conn.commit()


