CREATE TABLE profiles (
	id INT PRIMARY KEY,
	username TEXT UNIQUE,
	password TEXT, 
	email TEXT
);

CREATE TABLE images (
	id INT PRIMARY KEY,
	user_id INT FOREIGN KEY REFERENCES profiles(id),
	date DATETIME DEFAULT (DATETIME('NOW'))
);

CREATE TABLE comments (
	id INT PRIMARY KEY,
	user_id INT FOREIGN KEY REFERENCES profiles(id),
	reply_id INT FOREIGN KEY REFERENCES comments(id),
	image_id INT FOREIGN KEY REFERENCES images(id),
	contents TEXT,
	date DATETIME DEFAULT (DATETIME('NOW'))
);

CREATE TABLE categories (
	id INT PRIMARY KEY,
	name TEXT -- category name
);

CREATE TABLE imagecategories (
	id INT PRIMARY KEY,
	category_id INT FOREIGN KEY REFERENCES categories(id),
	image_id INT FOREIGN KEY REFERENCES images(id)
);

CREATE TABLE votes (
	id INT PRIMARY KEY,
	user_id INT FOREIGN KEY REFERENCES profiles(id),
	comment_id INT FOREIGN KEY REFERENCES comments(id),
	is_upvote INT -- SQLite does not technically have a bool
);