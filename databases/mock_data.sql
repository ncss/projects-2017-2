

#PROFILES

users = [
    {"id": "989898", "username": "2-Elite-4-u", "password": "codislife", "email": "THEPRO@mlg.com"},
    {"id": "452246", "username": "lolmemes", "password": "PianoTuner", "email": "The_Spiciest@live.com"},
    {"id": "987654", "username": "SMARTness", "password": "45623424252352523523525235", "email": "yo@yahoo.com"},
    {"id": "092455", "username": "James-Curran", "password": "JamesCurran", "email": "James_Curran@hotmail.com"},
    {"id": "123456", "username": "Pie", "password": "smileyface", "email": "haha@gmail.com"},
    {"id": "747025", "username": "ksgiwfw", "password": "weift823r2", "email": "f23rb82bf_@gmail.com"},
    {"id": "020520", "username": "Becky", "password": "idIfg34rer", "email": "BeckyWilda@coles.com"}
    ]

#COMMENTS

comments = [
    {"id": "1", "poster_id": "989898", "reply_to": None, "contents": "I can do better.", "Dates": "1/1/2017", "image_id": None},
    {"id": "2", "poster_id": "452246", "reply_to": "4", "contents": "Me like", "Dates": "1/1/2017", "image_id": None},
    {"id": "3", "poster_id": "987654", "reply_to": None, "contents": "I believe your choice of colours is incorrect. Add more warmth so you can add more life to it.", "Dates": "1/1/2017", "image_id": None},
    {"id": "4", "poster_id": "092455", "reply_to": None, "contents": "Is that a James Curran I see?", "Dates": "1/1/2017", "image_id": None},
    {"id": "5", "poster_id": "123456", "reply_to": None, "contents": "1000000000000000 upvotes for you good sir!", "Dates": "1/1/2017", "image_id": None},
    {"id": "6", "poster_id": "747025", "reply_to": "3", "contents": "Yeah, I agree.", "Dates": "2/1/2017", "image_id": None},
    {"id": "7", "poster_id": "020520", "reply_to": "5", "contents": "Plus mine :)", "Dates": "2/1/2017", "image_id": None}
    ]

--STATEMENT-DELIM
(Id, Username, Password, Email)

INSERT INTO users VALUES (      "989898", "2-Elite-4-u", "codislife", "THEPRO@mlg.com");






--STATEMENT-DELIM
(id, poster_id, reply_to, contents, dates, image_id)
--STATEMENT-DELIM
INSERT INTO comments VALUES ( "1", "989898", None, "I can do better.", "1/1/2017", None);
--STATEMENT-DELIM
INSERT INTO comments VALUES ( "2", "452246", "4", "Me like", "1/1/2017", None);
--STATEMENT-DELIM
INSERT INTO comments VALUES ( "3", "987654", None, "I believe your choice of colours is incorrect. Add more warmth so you can add more life to it.", "1/1/2017", None);
--STATEMENT-DELIM
INSERT INTO comments VALUES ("4", "092455", None, "Is that a James Curran I see?", "1/1/2017", None);
--STATEMENT-DELIM
INSERT INTO comments VALUES ("5", "123456", None,: "1000000000000000 upvotes for you good sir!", "1/1/2017", : None);
--STATEMENT-DELIM
INSERT INTO comments VALUES ("6", "747025", "3", "Yeah, I agree.", "2/1/2017",  None);
--STATEMENT-DELIM
INSERT INTO comments VALUES ("7", "020520", "5", "Plus mine :)", "2/1/2017", None);
--STATEMENT-DELIM
