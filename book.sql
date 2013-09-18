
create table if not exists user (
        user_id integer primary key autoincrement,
	user_name text not null,
	pwd text not null
);


create table if not exists book (
       book_id integer primary key,
       book_name text not null,
       author text not null,
       publish_com text not null,
       publish_date text not null
);


