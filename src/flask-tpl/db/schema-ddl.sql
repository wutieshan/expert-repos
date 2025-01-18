drop table if exists t_user;
create table t_user (
    id integer primary key autoincrement,
    username text unique not null,
    password text not null
);