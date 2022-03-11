create table log(id bigint, date datetime, inside bool, primary key (date));






create table log2(date datetime, id_badge bigint, inside bool, primary key (date), key(id_badge));