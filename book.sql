
create table if not exists user (
  user_id integer primary key autoincrement,
  username text not null,
  pwd text not null
);



