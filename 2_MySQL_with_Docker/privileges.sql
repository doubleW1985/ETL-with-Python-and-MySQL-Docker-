use mysql;
select host, user from user;

create user ###your username### identified by '###your password###';

grant all on ###your database name###.* to ###your username###@'%' identified by '###your password###' with grant option;

flush privileges;

