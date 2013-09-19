drop table if exists users;
create table users (
        user_id integer primary key autoincrement,
	user_name text not null,
	pwd text not null
);


drop table if exists books;
 create table books(
       book_id text primary key,
       book_name text not null,
       author text not null,
       publish_com text not null,
       publish_date text not null
);


