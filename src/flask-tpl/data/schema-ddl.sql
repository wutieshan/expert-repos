drop table if exists t_sys_user;
create table t_sys_user (
    id integer primary key autoincrement,
    username text unique not null, --'用户名'
    password text not null, --'密码'
    email text default null, --'邮箱'
    phone text default null, --'手机号'
    role_id integer default null, --'角色id'
    status integer default 0, --'用户状态 0-正常, 1-锁定, 2-注销'
    avater text default null, --'头像路径'
    created_at datetime not null default current_timestamp, --'创建时间'
    updated_at datetime not null default current_timestamp --'更新时间'
);


-- drop table if exists t_sys_role;