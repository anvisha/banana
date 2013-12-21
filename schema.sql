drop table if exists entries;
create table users(
    phone integer primary key,
    name text not null,
    email text not null
);
