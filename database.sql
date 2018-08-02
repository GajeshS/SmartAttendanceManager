drop table subject_timings;
drop table attendance;
drop table student;
drop table teacher;
drop Table login;

create table login(
	ID int primary key,
	Pass varchar(20) NOT NULL,
	acces char(10),
	CHECK(acces in ('student','teacher','admin'))
);

create table student(
	Name varchar(20) NOT NULL,
	RollNo int references login(ID),
	PRIMARY KEY(RollNo)
	);
create table teacher(
	Name varchar(20) NOT NULL,
	RollNo int references login(ID),
	Subject varchar(20),
	PRIMARY KEY(RollNo)
);
create table attendance(
	Today date,
	c_hour int,
	RollNo int,
	PRIMARY KEY (Today,c_hour,RollNo),
	FOREIGN KEY(RollNo) REFERENCES Student(RollNo)
);
create table subject_timings(
Today date,
c_hour int,
TeacherID int,
strength int,
FOREIGN KEY(TeacherID) REFERENCES Teacher(RollNo)
);

insert into login values(1729,'root','admin');
