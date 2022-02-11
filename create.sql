create table if not exists album(
	id serial primary key,
	title varchar(40),
	year_issue integer check (year_issue > 0)
);
create table if not exists collection(
	id serial primary key,
	title varchar(40),
	year_issue integer check (year_issue > 0)
);
create table if not exists singer (
	id serial primary key,
	singer_name varchar(40),
	singer_surname varchar(40),
	alias varchar(40)
);
create table if not exists singer-album (
	id serial primary key,
	id_album integer not null references album(id),
	id_singer integer not null references singer(id)
);
create table if not exists track(
	id serial primary key,
	id_album integer not null references album(id),
	title varchar(40),
	duration real check (duration > 0),
	year_issue integer
);
create table if not exists collection-track (
	id serial primary key,
	id_collection integer not null references collection(id),
	id_track integer not null references track(id)
);
create table if not exists genre (
	id serial primary key,
	title varchar(40)
);
create table if not exists genre-singer (
	id serial primary key,
	id_genre integer not null references genre(id),
	id_singer integer not null references singer(id)
);