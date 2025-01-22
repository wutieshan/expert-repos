drop table if exists t_user;
create table t_user (
    id integer primary key autoincrement,
    username text unique not null,
    password text not null,
    email text default null,
    phone text default null,
    created_at datetime default current_timestamp,
    updated_at datetime default current_timestamp
);