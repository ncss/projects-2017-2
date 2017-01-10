CREATE TABLE profiles (
	id INT PRIMARY KEY,
	username TEXT UNIQUE,
	password TEXT,
	email TEXT
);

--STATEMENT-DELIM

CREATE TABLE images (
	id INT PRIMARY KEY,
	user_id INT,
	date DATETIME  DEFAULT (DATETIME('NOW')),
	FOREIGN KEY(user_id) REFERENCES profiles(id)
);

--STATEMENT-DELIM

CREATE TABLE comments (
	id INT PRIMARY KEY,
	user_id INT,
	reply_id INT,
	image_id INT DEFAULT NULL,
	contents TEXT,
	date DATETIME DEFAULT (DATETIME('NOW')),
	FOREIGN KEY(user_id) REFERENCES profiles(id),
	FOREIGN KEY(reply_id) REFERENCES comments(id),
	FOREIGN KEY(image_id) REFERENCES images(id)
);

--STATEMENT-DELIM

CREATE TABLE categories (
	id INT PRIMARY KEY,
	name TEXT -- category name
);

--STATEMENT-DELIM

CREATE TABLE imagecategories (
	id INT PRIMARY KEY,
	category_id INT,
	image_id INT,
	FOREIGN KEY(category_id) REFERENCES categories(id),
	FOREIGN KEY(image_id) REFERENCES images(id)
);

--STATEMENT-DELIM

CREATE TABLE votes (
	id INT PRIMARY KEY,
	user_id INT,
	comment_id INT,
	is_upvote INT, -- SQLite does not technically have a bool
	FOREIGN KEY(user_id) REFERENCES profiles(id),
	FOREIGN KEY(comment_id) REFERENCES comments(id)
);