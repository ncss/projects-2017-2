CREATE TABLE profiles (
	id INT PRIMARY KEY,
	username TEXT,
	password TEXT,
	email TEXT
);

CREATE TABLE images (
	id INT PRIMARY KEY,
	user_id INT FOREIGN KEY REFERENCES profiles(id),
	date TEXT
);

CREATE TABLE comments (
	id INT PRIMARY KEY,
	user_id INT FOREIGN KEY REFERENCES profiles(id),
	reply_id INT FOREIGN KEY REFERENCES comments(id),
	image_id INT FOREIGN KEY REFERENCES images(id),
	contents TEXT,
	date TEXT
);

CREATE TABLE imagecategories (
	id INT PRIMARY KEY,
	category_id INT FOREIGN KEY REFERENCES categories(id),
	image_id INT FOREIGN KEY REFERENCES images(id)
);