create table if not exists users (
        user_id integer primary key autoincrement,
	user_name text not null,
	pwd text not null,
	college text,
	num text,
	email text
);

 create table if not exists  books(
       book_id text primary key,
       book_name text not null,
       author text not null,
       publish_com text not null,
       publish_date text not null
);

drop table if exists borrows;
create table  borrows(
       user_name text not null,
       book_id text not null,
       date_borrow text not null,
       date_return text not null,
       primary key (user_name, book_id)
);

drop table if exists histroys;
create table histroys(
       histroy_id integer primary key autoincrement,
       book_id text not null,
       user_name text not null,
       date_borrow text not null,
       date_return text,
       status text not null default 'not return'
);
