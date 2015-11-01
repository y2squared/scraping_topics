create table article ( \
    `title`  	 varchar(64) primary key, \
    `link`   	 varchar(64) not null, \
    `detail`  	 mediumtext  not null, \
    `updated_at` datetime    not null
)engine=InnoDB default charset=utf8;
