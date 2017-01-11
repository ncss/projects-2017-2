BEGIN TRANSACTION;

CREATE TABLE profiles (
	id INTEGER PRIMARY KEY AUTOINCREMENT,
	username TEXT UNIQUE,
	password TEXT,
	email TEXT
);

/*
CREATE TABLE images (
	id INTEGER PRIMARY KEY AUTOINCREMENT,
	user_id INT,
	date DATETIME DEFAULT (DATETIME('NOW')),
	FOREIGN KEY(user_id) REFERENCES profiles(id)
);
*/

CREATE TABLE comments (
	id INTEGER PRIMARY KEY AUTOINCREMENT,
	user_id INT,
	reply_id INT DEFAULT NULL,
	--image_id INT DEFAULT NULL,
	contents TEXT,
	date DATETIME DEFAULT (DATETIME('NOW')),
	FOREIGN KEY(user_id) REFERENCES profiles(id),
	FOREIGN KEY(reply_id) REFERENCES comments(id),
	FOREIGN KEY(image_id) REFERENCES images(id)
);

CREATE TABLE categories (
	id INTEGER PRIMARY KEY AUTOINCREMENT,
	name TEXT -- category name
);

CREATE TABLE imagecategories (
	id INTEGER PRIMARY KEY AUTOINCREMENT,
	category_id INT,
	image_id INT,
	FOREIGN KEY(category_id) REFERENCES categories(id),
	FOREIGN KEY(image_id) REFERENCES images(id)
);

CREATE TABLE votes (
	id INTEGER PRIMARY KEY AUTOINCREMENT,
	user_id INT,
	comment_id INT,
	is_upvote INT, -- SQLite does not technically have a bool
	FOREIGN KEY(user_id) REFERENCES profiles(id),
	FOREIGN KEY(comment_id) REFERENCES comments(id)
);

COMMIT;