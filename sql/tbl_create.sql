DROP TABLE IF EXISTS AlbumAccess;
DROP TABLE IF EXISTS Contain;
DROP TABLE IF EXISTS Photo;
DROP TABLE IF EXISTS Album;
DROP TABLE IF EXISTS User;

CREATE TABLE User
(
	username varchar(20),
	firstname varchar(20) NOT NULL,
	lastname varchar(20) NOT NULL,
	password varchar(256) NOT NULL,
	email varchar(40) NOT NULL,
	-- Keys
	PRIMARY KEY (username)
);

CREATE TABLE Album
(
	albumid int AUTO_INCREMENT,
	title varchar(50),
	created DATE NOT NULL,
	lastupdated DATE NOT NULL,
	username varchar(20),
	access ENUM('private', 'public') NOT NULL,
	-- Keys
	PRIMARY KEY (albumid),
	FOREIGN KEY (username) REFERENCES User(username)
);

CREATE TABLE Photo
(
	picid varchar(40),
	format varchar(3),
	date DATE NOT NULL,
	-- Keys
	PRIMARY KEY (picid)
);

CREATE TABLE Contain
(
	albumid int,
	picid varchar(40),
	caption varchar(255),
	sequencenum int NOT NULL,
	-- Keys
	PRIMARY KEY (albumid, picid),
	FOREIGN KEY (albumid) REFERENCES Album(albumid) ON DELETE CASCADE,
	FOREIGN KEY (picid) REFERENCES Photo(picid) ON DELETE CASCADE
);

CREATE TABLE AlbumAccess
(
	albumid int,
	username varchar(20),
	-- Keys
	FOREIGN KEY (albumid) REFERENCES Album(albumid),
	FOREIGN KEY (username) REFERENCES User(username)
);
