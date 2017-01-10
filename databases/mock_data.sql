BEGIN TRANSACTION;

--(id, username, password, email)
INSERT INTO profiles VALUES (989898, "2-Elite-4-u", "codislife", "THEPRO@mlg.com");
INSERT INTO profiles VALUES (452246, "lolmemes", "PianoTuner", "The_Spiciest@live.com");
INSERT INTO profiles VALUES (987654, "SMARTness", "45623424252352523523525235", "yo@yahoo.com");
INSERT INTO profiles VALUES ( 92455, "James-Curran", "JamesCurran", "James_Curran@hotmail.com");
INSERT INTO profiles VALUES (123456, "Pie", "smileyface", "haha@gmail.com");
INSERT INTO profiles VALUES (747025, "ksgiwfw", "weift823r2", "f23rb82bf_@gmail.com");
INSERT INTO profiles VALUES ( 20520, "Becky", "idIfg34rer", "BeckyWilda@coles.com");


--(id, user_id, reply_to, image_id, contents, date)
INSERT INTO comments VALUES (1, 989898, NULL, NULL, "I can do better.", "2017-01-01 00:00:26");
INSERT INTO comments VALUES (2, 452246, 4, NULL, "Me like", "2017-01-01 00:01:50");
INSERT INTO comments VALUES (3, 987654, NULL, NULL, "I believe your choice of colours is incorrect. Add more warmth so you can add more life to it.", "2017-01-01 05:42:42");
INSERT INTO comments VALUES (4, 92455, NULL, NULL, "Is that a James Curran I see?", "2017-01-01 08:13:42");
INSERT INTO comments VALUES (5, 123456, NULL, NULL, "1000000000000000 upvotes for you good sir!", "2017-01-02 00:00:00");
INSERT INTO comments VALUES (6, 747025, 3, NULL, "Yeah, I agree.", "2017-01-02 01:05:58");
INSERT INTO comments VALUES (7, 20520, 5, NULL, "Plus mine :)", "2017-01-02 01:17:21");

COMMIT;