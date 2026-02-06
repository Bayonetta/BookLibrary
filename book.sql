create table if not exists users (
        user_id integer primary key autoincrement,
	user_name text not null,
	pwd text not null,
	college text,
	num text,
	email text
);

create table if not exists books(
       book_id text primary key,
       book_name text not null,
       author text not null,
       publish_com text not null,
       publish_date text not null
);

-- 借阅相关表不再在初始化时强制 drop，避免每次 init_db() 清空运行数据
create table if not exists borrows(
       user_name text not null,
       book_id text not null,
       date_borrow text not null,
       date_return text not null,
       primary key (user_name, book_id)
);

create table if not exists histroys(
       histroy_id integer primary key autoincrement,
       book_id text not null,
       user_name text not null,
       date_borrow text not null,
       date_return text,
       status text not null default 'not return'
);
