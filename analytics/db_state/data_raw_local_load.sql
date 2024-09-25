--
-- PostgreSQL database dump
--

-- Dumped from database version 16.4 (Debian 16.4-1.pgdg120+1)
-- Dumped by pg_dump version 16.4 (Debian 16.4-1.pgdg120+1)

SET statement_timeout = 0;
SET lock_timeout = 0;
SET idle_in_transaction_session_timeout = 0;
SET client_encoding = 'UTF8';
SET standard_conforming_strings = on;
SELECT pg_catalog.set_config('search_path', '', false);
SET check_function_bodies = false;
SET xmloption = content;
SET client_min_messages = warning;
SET row_security = off;

--
-- Data for Name: books; Type: TABLE DATA; Schema: public; Owner: postgres
--

INSERT INTO public.books (book_id, unique_hash, gr_id, title, author, isbn, date_added, date_last_displayed) OVERRIDING SYSTEM VALUE VALUES (51, '2bb9ec8c66bf9f4dc8e9b9b92c648f4ff3ad065efbe5825447054e87a6336b54', 54120, 'The Double', 'José Saramago', '0151010404', '2024-09-05 02:11:30.036162', '2024-09-05 02:11:30.036162');
INSERT INTO public.books (book_id, unique_hash, gr_id, title, author, isbn, date_added, date_last_displayed) OVERRIDING SYSTEM VALUE VALUES (42, 'd7792ca487ae88a0108773f89afd4ee717460891d0e337b2fdd72c23260c09df', 68428, 'The Final Empire (Mistborn, #1)', 'Brandon Sanderson', '', '2024-09-05 02:08:56.93004', '2024-09-05 02:08:56.93004');
INSERT INTO public.books (book_id, unique_hash, gr_id, title, author, isbn, date_added, date_last_displayed) OVERRIDING SYSTEM VALUE VALUES (19, '3d33756ff016f47d6c577133c24ee8a9cb91a2085b3ac8ab550195a9240a6c98', 23168817, 'The Dark Forest (Remembrance of Earth’s Past, #2)', 'Liu Cixin', '', '2024-09-03 04:39:16.877058', '2024-09-03 04:39:16.877058');
INSERT INTO public.books (book_id, unique_hash, gr_id, title, author, isbn, date_added, date_last_displayed) OVERRIDING SYSTEM VALUE VALUES (13, 'a17ae520d90e32c2d72266f3fd34dc7793bd601869597db5c185e1c3fcab5570', 40376072, 'Children of Ruin (Children of Time, #2)', 'Adrian Tchaikovsky', '', '2024-09-03 04:25:27.736715', '2024-09-03 04:25:27.736715');
INSERT INTO public.books (book_id, unique_hash, gr_id, title, author, isbn, date_added, date_last_displayed) OVERRIDING SYSTEM VALUE VALUES (12, '2e4908bc3eee2617a20beef863ad301702ddc3bdef0bf13b9e91c152a30efc2c', 33600, 'Shantaram', 'Gregory David Roberts', '192076920X', '2024-09-03 04:25:27.736715', '2024-09-03 04:25:27.736715');
INSERT INTO public.books (book_id, unique_hash, gr_id, title, author, isbn, date_added, date_last_displayed) OVERRIDING SYSTEM VALUE VALUES (24, '90ab6599e9950d5373c8e1756b06009005187f762b65ab54a7477695fbf2ec76', 40604658, 'Jurassic Park (Jurassic Park, #1)', 'Michael Crichton', '', '2024-09-03 18:26:08.26731', '2024-09-03 18:26:08.26731');
INSERT INTO public.books (book_id, unique_hash, gr_id, title, author, isbn, date_added, date_last_displayed) OVERRIDING SYSTEM VALUE VALUES (49, '0f906ffc960727ac9f517d0f3956fd24d1610d20e4f543248a46df38b850821b', 24800, 'House of Leaves', 'Mark Z. Danielewski', '', '2024-09-05 02:11:25.101794', '2024-09-05 02:11:25.101794');
INSERT INTO public.books (book_id, unique_hash, gr_id, title, author, isbn, date_added, date_last_displayed) OVERRIDING SYSTEM VALUE VALUES (6, '272c36a3b4c8519dcadca2d8836780557a70994f8ba9c0b9642412ac2b96a288', 24885533, 'The Paper Menagerie and Other Stories', 'Ken Liu', '1481442546', '2024-09-02 23:03:45.622513', '2024-09-02 23:03:45.622513');
INSERT INTO public.books (book_id, unique_hash, gr_id, title, author, isbn, date_added, date_last_displayed) OVERRIDING SYSTEM VALUE VALUES (52, 'a10c07ed9b7edef19a61b925fd7e68a7f7e9a3a3f4ccd35d532b97f2dbd02730', 6063554, 'Columbine: A True Crime Story', 'Jeff Kass', '0981652565', '2024-09-05 02:11:30.036162', '2024-09-05 02:11:30.036162');
INSERT INTO public.books (book_id, unique_hash, gr_id, title, author, isbn, date_added, date_last_displayed) OVERRIDING SYSTEM VALUE VALUES (11, 'ae330ce0285eb74847ee51013795b0a9cf440ae48a9c3edf7f54864ad693a854', 35631386, 'The Undoing Project: A Friendship That Changed Our Minds', 'Michael Lewis', '0393354776', '2024-09-03 04:25:27.736715', '2024-09-04 22:33:44.123466');
INSERT INTO public.books (book_id, unique_hash, gr_id, title, author, isbn, date_added, date_last_displayed) OVERRIDING SYSTEM VALUE VALUES (9, '2cb5d38a1cec27a269c84623ae4113fe22f4952fac7b630471875cc97f9735c3', 12497, 'No Country for Old Men', 'Cormac McCarthy', '', '2024-09-02 23:03:45.622513', '2024-09-05 02:08:56.93004');
INSERT INTO public.books (book_id, unique_hash, gr_id, title, author, isbn, date_added, date_last_displayed) OVERRIDING SYSTEM VALUE VALUES (22, 'b99ab890a4aa8bddd04a3065d89c78ea08ac9fb868e3e5548f8f1fe9d9d924db', 60165391, 'Survival of the Richest: Escape Fantasies of the Tech Billionaires', 'Douglas Rushkoff', '0393881067', '2024-09-03 18:26:08.26731', '2024-09-03 18:26:08.26731');
INSERT INTO public.books (book_id, unique_hash, gr_id, title, author, isbn, date_added, date_last_displayed) OVERRIDING SYSTEM VALUE VALUES (18, '327d53026dc9ef78e42bfc6fa400e4158cd5036e9b742f69b3ddf77edf0cf998', 170505, 'American Ground: Unbuilding the World Trade Center', 'William Langewiesche', '0865476756', '2024-09-03 04:39:16.877058', '2024-09-03 04:39:16.877058');
INSERT INTO public.books (book_id, unique_hash, gr_id, title, author, isbn, date_added, date_last_displayed) OVERRIDING SYSTEM VALUE VALUES (27, 'd84ed2525c2c76c9f78acfef81c13c927c6cfeb3b7200d44b4b3180730c2325d', 40864030, 'A Prayer for the Crown-Shy (Monk & Robot, #2)', 'Becky Chambers', '', '2024-09-04 01:42:59.489135', '2024-09-04 01:52:59.240974');
INSERT INTO public.books (book_id, unique_hash, gr_id, title, author, isbn, date_added, date_last_displayed) OVERRIDING SYSTEM VALUE VALUES (48, '47a0e31420225eb5267f53b85654d7f42ef8c67494aabacdc584696d4ab58821', 123471, 'I Am a Strange Loop', 'Douglas R. Hofstadter', '0465030785', '2024-09-05 02:11:25.101794', '2024-09-05 02:11:25.101794');
INSERT INTO public.books (book_id, unique_hash, gr_id, title, author, isbn, date_added, date_last_displayed) OVERRIDING SYSTEM VALUE VALUES (8, 'dff74765ca235b8cf8fc7b94bb073556e7debe82ed17e3b3d8036d9a44634404', 170945, 'Five Were Missing', 'Lois Duncan', '0451086783', '2024-09-02 23:03:45.622513', '2024-09-02 23:03:45.622513');
INSERT INTO public.books (book_id, unique_hash, gr_id, title, author, isbn, date_added, date_last_displayed) OVERRIDING SYSTEM VALUE VALUES (26, 'fc5cc30cfee2023e0768e6f642f7c31beb8d6b5a733993a5a13ef10e48cda014', 57701764, 'Wish You Were Here', 'Jodi Picoult', '1984818414', '2024-09-04 01:42:59.489135', '2024-09-04 01:52:59.240974');
INSERT INTO public.books (book_id, unique_hash, gr_id, title, author, isbn, date_added, date_last_displayed) OVERRIDING SYSTEM VALUE VALUES (37, '5b7a8cbc2b33f879cd821ecfd1b20120dbedaa4785452968fea37514ce3e4532', 16902, 'Walden', 'Henry David Thoreau', '', '2024-09-04 22:33:44.123466', '2024-09-04 22:33:44.123466');
INSERT INTO public.books (book_id, unique_hash, gr_id, title, author, isbn, date_added, date_last_displayed) OVERRIDING SYSTEM VALUE VALUES (36, '926478eb5a94a72a582605031bd80ffa323e3cbad7563fb4814384a574b8bd14', 164154, 'A Canticle for Leibowitz (St. Leibowitz, #1)', 'Walter M. Miller Jr.', '0060892994', '2024-09-04 22:33:44.123466', '2024-09-04 22:33:44.123466');
INSERT INTO public.books (book_id, unique_hash, gr_id, title, author, isbn, date_added, date_last_displayed) OVERRIDING SYSTEM VALUE VALUES (21, 'acfe145990bf99997b634a41df26a6839fd75481e9f84de7f6fb43273805619e', 57850265, 'How High We Go in the Dark', 'Sequoia Nagamatsu', '0063072645', '2024-09-03 18:26:08.26731', '2024-09-05 02:11:25.101794');
INSERT INTO public.books (book_id, unique_hash, gr_id, title, author, isbn, date_added, date_last_displayed) OVERRIDING SYSTEM VALUE VALUES (53, 'dad143321c6c18322eb8fb83e88516caa7343606a98ad1e166ce8921583fd5a3', 61286907, 'The Trees Grew Because I Bled There: Collected Stories', 'Eric LaRocca', '1803363002', '2024-09-05 02:11:30.036162', '2024-09-05 02:11:30.036162');
INSERT INTO public.books (book_id, unique_hash, gr_id, title, author, isbn, date_added, date_last_displayed) OVERRIDING SYSTEM VALUE VALUES (23, '40fe9faa76e608b6cb8a27c62e645b2e1a0151241e16d8c885508698bf7785a4', 531989, 'Drown', 'Junot Díaz', '1573226068', '2024-09-03 18:26:08.26731', '2024-09-05 02:11:30.036162');
INSERT INTO public.books (book_id, unique_hash, gr_id, title, author, isbn, date_added, date_last_displayed) OVERRIDING SYSTEM VALUE VALUES (17, '457849fc4dd8c5bac371b94b14b84a4e982d915ca09e9e129625258ea7b171ce', 203164421, 'William', 'Mason Coile', '0593719603', '2024-09-03 04:39:16.877058', '2024-09-03 04:39:16.877058');
INSERT INTO public.books (book_id, unique_hash, gr_id, title, author, isbn, date_added, date_last_displayed) OVERRIDING SYSTEM VALUE VALUES (41, '4111be00c761c2a7c9c33382d81b22d6717a0f8a101bdf93eb3b89b11732e2c3', 199698485, 'The God of the Woods', 'Liz Moore', '', '2024-09-05 02:08:56.93004', '2024-09-07 20:20:52.81133');
INSERT INTO public.books (book_id, unique_hash, gr_id, title, author, isbn, date_added, date_last_displayed) OVERRIDING SYSTEM VALUE VALUES (14, '9bc88918e6a2d50933f36cf308c122842a15fc698f63f08be79b99910351ce7a', 41128, 'The Wild Shore (Three Californias Triptych, #1)', 'Kim Stanley Robinson', '0312890362', '2024-09-03 04:25:27.736715', '2024-09-03 04:25:27.736715');
INSERT INTO public.books (book_id, unique_hash, gr_id, title, author, isbn, date_added, date_last_displayed) OVERRIDING SYSTEM VALUE VALUES (7, 'd9fe03330b69e819335f78e9c4278320d247f53a7e3e275ae0334069ec8bc972', 25451264, 'Death''s End (Remembrance of Earth’s Past, #3)', 'Liu Cixin', '0765377101', '2024-09-02 23:03:45.622513', '2024-09-02 23:03:45.622513');
INSERT INTO public.books (book_id, unique_hash, gr_id, title, author, isbn, date_added, date_last_displayed) OVERRIDING SYSTEM VALUE VALUES (16, 'ba1460c45d9c0347cf58297d626aa69a398babbae6eeaabf3657f976ac5ac218', 31548, 'Of Human Bondage', 'W. Somerset Maugham', '0451530179', '2024-09-03 04:39:16.877058', '2024-09-03 04:39:16.877058');
INSERT INTO public.books (book_id, unique_hash, gr_id, title, author, isbn, date_added, date_last_displayed) OVERRIDING SYSTEM VALUE VALUES (54, 'e430404398d9549ae3b112a58872b233356122a87087f9cfb2b09f1daa03f55a', 31176818, 'The Shadow of What Was Lost (The Licanius Trilogy, #1)', 'James Islington', '', '2024-09-07 15:53:06.456185', '2024-09-07 15:53:06.456185');
INSERT INTO public.books (book_id, unique_hash, gr_id, title, author, isbn, date_added, date_last_displayed) OVERRIDING SYSTEM VALUE VALUES (55, 'd8bee2696652b63f72d7efd1d379eb8defa730c47412ad9de722486e3528e75e', 56474282, 'Heartless Sky (Zodiac Academy, #7)', 'Caroline Peckham', '', '2024-09-07 15:53:06.456185', '2024-09-07 15:53:06.456185');
INSERT INTO public.books (book_id, unique_hash, gr_id, title, author, isbn, date_added, date_last_displayed) OVERRIDING SYSTEM VALUE VALUES (76, '2269cad4b8a754e8b722108338745420eadf3a62636c82a705c0c386a803d3b6', 58897384, 'Radiate: 90 Devotions to Reflect the Heart of Jesus', 'Cleere Cherry', '1648708137', '2024-09-07 15:57:54.961436', '2024-09-07 15:57:54.961436');
INSERT INTO public.books (book_id, unique_hash, gr_id, title, author, isbn, date_added, date_last_displayed) OVERRIDING SYSTEM VALUE VALUES (78, '89b2e5bd48ff428a239350dbff5f8cb5e8e15ea1d8e4c0b4a2cf6a4ee1eb0b80', 57861689, 'Witch King (The Rising World, #1)', 'Martha Wells', '', '2024-09-07 15:57:54.961436', '2024-09-07 15:57:54.961436');
INSERT INTO public.books (book_id, unique_hash, gr_id, title, author, isbn, date_added, date_last_displayed) OVERRIDING SYSTEM VALUE VALUES (79, 'feb4b93071d16b7013db6e34ed58785d410e8993ddc8c23f93de25e15e31b713', 58997182, 'Good Enough: 40ish Devotionals for a Life of Imperfection', 'Kate Bowler', '', '2024-09-07 15:57:54.961436', '2024-09-07 15:57:54.961436');
INSERT INTO public.books (book_id, unique_hash, gr_id, title, author, isbn, date_added, date_last_displayed) OVERRIDING SYSTEM VALUE VALUES (80, 'ca7e7482f2e1ccf8cc16e200f10ead00e5613d08ada8990301b26542d12c335f', 26856502, 'Vengeful (Villains, #2)', 'Victoria Schwab', '', '2024-09-07 15:58:02.314147', '2024-09-07 15:58:02.314147');
INSERT INTO public.books (book_id, unique_hash, gr_id, title, author, isbn, date_added, date_last_displayed) OVERRIDING SYSTEM VALUE VALUES (56, 'db7efbc47f91214bb31ee91ccd8cfb43d2a8b7e7509052bfbd2e625ed0b0813d', 150249463, 'The Tainted Cup (Shadow of the Leviathan, #1)', 'Robert Jackson Bennett', '1984820729', '2024-09-07 15:53:06.456185', '2024-09-07 15:58:02.314147');
INSERT INTO public.books (book_id, unique_hash, gr_id, title, author, isbn, date_added, date_last_displayed) OVERRIDING SYSTEM VALUE VALUES (57, '51eb35ea7b2c28ee9f0548197d3a8af7d72fb16a19063191bfb8373cba10bdaf', 123249278, 'The Hurricane Wars (The Hurricane Wars #1)', 'Thea Guanzon', '', '2024-09-07 15:53:06.456185', '2024-09-07 15:58:09.69231');
INSERT INTO public.books (book_id, unique_hash, gr_id, title, author, isbn, date_added, date_last_displayed) OVERRIDING SYSTEM VALUE VALUES (77, 'c77165284b78576c5ee5cd40c8ba500e4840c2097897f3dbe6c067272a031c97', 58678549, 'The No-Show', 'Beth O''Leary', '0593438442', '2024-09-07 15:57:54.961436', '2024-09-07 15:58:09.69231');
INSERT INTO public.books (book_id, unique_hash, gr_id, title, author, isbn, date_added, date_last_displayed) OVERRIDING SYSTEM VALUE VALUES (81, '7b766778ea4b396e18b7f8e4ec3a037a13c690c22304ae9165c7305015372e35', 201899944, 'The Marriage Portrait', 'Maggie O''Farrell', '', '2024-09-07 15:58:02.314147', '2024-09-07 15:58:09.69231');
INSERT INTO public.books (book_id, unique_hash, gr_id, title, author, isbn, date_added, date_last_displayed) OVERRIDING SYSTEM VALUE VALUES (87, '70063ab116b6f745c64fc5c3ed700b112c3478c4e1d75e99a3836f9e3896f018', 75265531, 'The Secret History', 'Donna Tartt', '', '2024-09-07 15:58:09.69231', '2024-09-07 15:58:09.69231');
INSERT INTO public.books (book_id, unique_hash, gr_id, title, author, isbn, date_added, date_last_displayed) OVERRIDING SYSTEM VALUE VALUES (88, 'b285780317998861adc39f183f5cc3bdd3164a0d70a7000a97df52b7878c1e92', 53906012, 'The Billiard Ball', 'Isaac Asimov', '', '2024-09-07 20:20:52.81133', '2024-09-07 20:20:52.81133');
INSERT INTO public.books (book_id, unique_hash, gr_id, title, author, isbn, date_added, date_last_displayed) OVERRIDING SYSTEM VALUE VALUES (89, 'b5493bc26f3b8563da8c4d6242e75116fc70ede69bb4901f70ed41e035ea837d', 20906644, 'The MAXX: Maxximized Volume 1', 'Sam Kieth', '1613779593', '2024-09-07 20:20:52.81133', '2024-09-07 20:20:52.81133');
INSERT INTO public.books (book_id, unique_hash, gr_id, title, author, isbn, date_added, date_last_displayed) OVERRIDING SYSTEM VALUE VALUES (90, '2d0db2a7b8a7209eb2e09d21743e8a5ac5ad93fda3c1249b2129125478681a92', 62919902, 'The Handyman Method', 'Nick Cutter', '1982196718', '2024-09-07 20:20:52.81133', '2024-09-07 20:20:52.81133');
INSERT INTO public.books (book_id, unique_hash, gr_id, title, author, isbn, date_added, date_last_displayed) OVERRIDING SYSTEM VALUE VALUES (1, '45fe47cba7e94651749d00ef4768a0a8b554995e305dfd5ba60aca38979685b1', 1898, 'Into Thin Air: A Personal Account of the Mt. Everest Disaster', 'Jon Krakauer', '', '2024-09-02 09:46:54.835456', '2024-09-02 09:46:54.835456');
INSERT INTO public.books (book_id, unique_hash, gr_id, title, author, isbn, date_added, date_last_displayed) OVERRIDING SYSTEM VALUE VALUES (2, '4304f0a833cf3a4c3855c2f59133449756992052654e32201746794bad30ef23', 49552, 'The Stranger', 'Albert Camus', '', '2024-09-02 09:46:54.835456', '2024-09-02 09:46:54.835456');
INSERT INTO public.books (book_id, unique_hash, gr_id, title, author, isbn, date_added, date_last_displayed) OVERRIDING SYSTEM VALUE VALUES (3, '40b301fe09ffbd1569f03877787a7caccc4c3868d610b46c972a12e853098a40', 36529, 'Narrative of the Life of Frederick Douglass', 'Frederick Douglass', '1580495761', '2024-09-02 09:46:54.835456', '2024-09-02 09:46:54.835456');
INSERT INTO public.books (book_id, unique_hash, gr_id, title, author, isbn, date_added, date_last_displayed) OVERRIDING SYSTEM VALUE VALUES (4, 'e65bb2dd37b7be4eb893f71f22c4fb006ac4324851a36617656ba4b8a8d8083e', 36064445, 'Skin in the Game: The Hidden Asymmetries in Daily Life', 'Nassim Nicholas Taleb', '0241300657', '2024-09-02 09:46:54.835456', '2024-09-02 09:46:54.835456');


--
-- Data for Name: library_searches; Type: TABLE DATA; Schema: public; Owner: postgres
--

INSERT INTO public.library_searches (library_search_id, library_id, is_libby, time_start, time_complete, book_id, available, availability_message) OVERRIDING SYSTEM VALUE VALUES (1, 'nashville', true, '2024-09-02 09:47:02.582256', '2024-09-02 09:47:02.878562', 1, true, 'AVAILABLE: Check link for more');
INSERT INTO public.library_searches (library_search_id, library_id, is_libby, time_start, time_complete, book_id, available, availability_message) OVERRIDING SYSTEM VALUE VALUES (2, 'nashville', true, '2024-09-02 23:07:49.741199', '2024-09-02 23:07:50.053383', 6, false, 'UNAVAILABLE: Check to see hold');
INSERT INTO public.library_searches (library_search_id, library_id, is_libby, time_start, time_complete, book_id, available, availability_message) OVERRIDING SYSTEM VALUE VALUES (3, 'nashville', true, '2024-09-03 04:26:57.939362', '2024-09-03 04:26:58.555782', 12, true, 'AVAILABLE: Check link for more');
INSERT INTO public.library_searches (library_search_id, library_id, is_libby, time_start, time_complete, book_id, available, availability_message) OVERRIDING SYSTEM VALUE VALUES (4, 'nashville', false, '2024-09-03 04:39:58.763122', '2024-09-03 04:39:59.72605', 17, false, 'UNKNOWN STATUS: Check link for more details');
INSERT INTO public.library_searches (library_search_id, library_id, is_libby, time_start, time_complete, book_id, available, availability_message) OVERRIDING SYSTEM VALUE VALUES (5, 'nashville', true, '2024-09-03 18:26:36.647791', '2024-09-03 18:26:37.325325', 21, false, 'UNAVAILABLE: Check to see hold');
INSERT INTO public.library_searches (library_search_id, library_id, is_libby, time_start, time_complete, book_id, available, availability_message) OVERRIDING SYSTEM VALUE VALUES (6, 'nashville', true, '2024-09-04 01:43:14.133614', '2024-09-04 01:43:14.851427', 26, false, 'UNAVAILABLE: Check to see hold');
INSERT INTO public.library_searches (library_search_id, library_id, is_libby, time_start, time_complete, book_id, available, availability_message) OVERRIDING SYSTEM VALUE VALUES (7, 'nashville', true, '2024-09-04 01:43:20.529208', '2024-09-04 01:43:21.109342', 27, false, 'UNAVAILABLE: Check to see hold');
INSERT INTO public.library_searches (library_search_id, library_id, is_libby, time_start, time_complete, book_id, available, availability_message) OVERRIDING SYSTEM VALUE VALUES (8, 'nashville', false, '2024-09-04 01:43:42.385244', '2024-09-04 01:43:43.430699', 26, true, 'AVAILABLE: [''Bellevue'', ''Bordeaux'', ''Donelson'']');
INSERT INTO public.library_searches (library_search_id, library_id, is_libby, time_start, time_complete, book_id, available, availability_message) OVERRIDING SYSTEM VALUE VALUES (9, 'nashville', false, '2024-09-04 01:43:51.052204', '2024-09-04 01:43:52.123213', 27, true, 'AVAILABLE: [''Donelson'', ''Edmondson Pike'', ''Green Hills'']');
INSERT INTO public.library_searches (library_search_id, library_id, is_libby, time_start, time_complete, book_id, available, availability_message) OVERRIDING SYSTEM VALUE VALUES (10, 'nashville', true, '2024-09-05 02:09:18.861377', '2024-09-05 02:09:19.546215', 9, true, 'AVAILABLE: Check link for more');
INSERT INTO public.library_searches (library_search_id, library_id, is_libby, time_start, time_complete, book_id, available, availability_message) OVERRIDING SYSTEM VALUE VALUES (11, 'nashville', false, '2024-09-05 02:09:29.561177', '2024-09-05 02:09:30.920112', 9, true, 'AVAILABLE: [''Green Hills'']');
INSERT INTO public.library_searches (library_search_id, library_id, is_libby, time_start, time_complete, book_id, available, availability_message) OVERRIDING SYSTEM VALUE VALUES (12, 'nashville', true, '2024-09-07 15:53:24.153619', '2024-09-07 15:53:24.883579', 54, false, 'UNAVAILABLE: Check to see hold');
INSERT INTO public.library_searches (library_search_id, library_id, is_libby, time_start, time_complete, book_id, available, availability_message) OVERRIDING SYSTEM VALUE VALUES (13, 'nashville', true, '2024-09-07 15:53:29.162594', '2024-09-07 15:53:29.757917', 54, false, 'UNAVAILABLE: Check to see hold');
INSERT INTO public.library_searches (library_search_id, library_id, is_libby, time_start, time_complete, book_id, available, availability_message) OVERRIDING SYSTEM VALUE VALUES (14, 'nashville', true, '2024-09-07 15:53:56.901352', '2024-09-07 15:53:57.521257', 54, false, 'UNAVAILABLE: Check to see hold');
INSERT INTO public.library_searches (library_search_id, library_id, is_libby, time_start, time_complete, book_id, available, availability_message) OVERRIDING SYSTEM VALUE VALUES (15, 'nashville', true, '2024-09-07 15:57:30.688287', '2024-09-07 15:57:31.202818', 54, false, 'UNAVAILABLE: Check to see hold');
INSERT INTO public.library_searches (library_search_id, library_id, is_libby, time_start, time_complete, book_id, available, availability_message) OVERRIDING SYSTEM VALUE VALUES (16, 'nashville', true, '2024-09-07 15:57:37.697895', '2024-09-07 15:57:38.220637', 55, false, 'Item Not Found: Link to search results');
INSERT INTO public.library_searches (library_search_id, library_id, is_libby, time_start, time_complete, book_id, available, availability_message) OVERRIDING SYSTEM VALUE VALUES (17, 'nashville', true, '2024-09-07 15:57:41.969641', '2024-09-07 15:57:42.591917', 56, false, 'UNAVAILABLE: Check to see hold');
INSERT INTO public.library_searches (library_search_id, library_id, is_libby, time_start, time_complete, book_id, available, availability_message) OVERRIDING SYSTEM VALUE VALUES (18, 'nashville', true, '2024-09-07 15:57:46.146086', '2024-09-07 15:57:46.647002', 57, true, 'AVAILABLE: Check link for more');
INSERT INTO public.library_searches (library_search_id, library_id, is_libby, time_start, time_complete, book_id, available, availability_message) OVERRIDING SYSTEM VALUE VALUES (19, 'nashville', true, '2024-09-07 15:53:24.153619', '2024-09-07 15:53:24.883579', 54, false, 'UNAVAILABLE: Check to see hold');
INSERT INTO public.library_searches (library_search_id, library_id, is_libby, time_start, time_complete, book_id, available, availability_message) OVERRIDING SYSTEM VALUE VALUES (20, 'nashville', true, '2024-09-07 15:53:29.162594', '2024-09-07 15:53:29.757917', 54, false, 'UNAVAILABLE: Check to see hold');
INSERT INTO public.library_searches (library_search_id, library_id, is_libby, time_start, time_complete, book_id, available, availability_message) OVERRIDING SYSTEM VALUE VALUES (21, 'nashville', true, '2024-09-07 15:53:56.901352', '2024-09-07 15:53:57.521257', 54, false, 'UNAVAILABLE: Check to see hold');
INSERT INTO public.library_searches (library_search_id, library_id, is_libby, time_start, time_complete, book_id, available, availability_message) OVERRIDING SYSTEM VALUE VALUES (22, 'nashville', true, '2024-09-07 15:57:30.688287', '2024-09-07 15:57:31.202818', 54, false, 'UNAVAILABLE: Check to see hold');
INSERT INTO public.library_searches (library_search_id, library_id, is_libby, time_start, time_complete, book_id, available, availability_message) OVERRIDING SYSTEM VALUE VALUES (23, 'nashville', true, '2024-09-07 15:57:37.697895', '2024-09-07 15:57:38.220637', 55, false, 'Item Not Found: Link to search results');
INSERT INTO public.library_searches (library_search_id, library_id, is_libby, time_start, time_complete, book_id, available, availability_message) OVERRIDING SYSTEM VALUE VALUES (24, 'nashville', true, '2024-09-07 15:57:41.969641', '2024-09-07 15:57:42.591917', 56, false, 'UNAVAILABLE: Check to see hold');
INSERT INTO public.library_searches (library_search_id, library_id, is_libby, time_start, time_complete, book_id, available, availability_message) OVERRIDING SYSTEM VALUE VALUES (25, 'nashville', true, '2024-09-07 15:57:46.146086', '2024-09-07 15:57:46.647002', 57, true, 'AVAILABLE: Check link for more');
INSERT INTO public.library_searches (library_search_id, library_id, is_libby, time_start, time_complete, book_id, available, availability_message) OVERRIDING SYSTEM VALUE VALUES (26, 'nashville', true, '2024-09-07 20:27:00.485207', '2024-09-07 20:27:01.199723', 90, false, 'UNAVAILABLE: Check to see hold');
INSERT INTO public.library_searches (library_search_id, library_id, is_libby, time_start, time_complete, book_id, available, availability_message) OVERRIDING SYSTEM VALUE VALUES (27, 'nashville', true, '2024-09-07 20:31:06.219267', '2024-09-07 20:31:06.895772', 41, false, 'UNAVAILABLE: Check to see hold');
INSERT INTO public.library_searches (library_search_id, library_id, is_libby, time_start, time_complete, book_id, available, availability_message) OVERRIDING SYSTEM VALUE VALUES (28, 'nashville', true, '2024-09-02 09:47:02.582256', '2024-09-02 09:47:02.878562', 1, true, 'AVAILABLE: Check link for more');


--
-- Data for Name: shelves; Type: TABLE DATA; Schema: public; Owner: postgres
--

INSERT INTO public.shelves (shelf_id, shelf_url, date_added, date_last_searched) OVERRIDING SYSTEM VALUE VALUES (6, 'https://www.goodreads.com/review/list/161795839?shelf=to-read&sort=position&order=a', '2024-09-04 01:42:59.489135', '2024-09-04 01:52:59.240974');
INSERT INTO public.shelves (shelf_id, shelf_url, date_added, date_last_searched) OVERRIDING SYSTEM VALUE VALUES (13, 'https://www.goodreads.com/review/list/10001241?shelf=currently-reading&sort=position&order=d', '2024-09-07 15:53:06.456185', '2024-09-07 15:58:09.69231');
INSERT INTO public.shelves (shelf_id, shelf_url, date_added, date_last_searched) OVERRIDING SYSTEM VALUE VALUES (4, 'https://www.goodreads.com/review/list/158747789?shelf=to-read&sort=position&order=d', '2024-09-03 04:39:16.877058', '2024-09-07 20:20:52.81133');
INSERT INTO public.shelves (shelf_id, shelf_url, date_added, date_last_searched) OVERRIDING SYSTEM VALUE VALUES (1, 'https://www.goodreads.com/review/list/158747789-michael-chapman?shelf=to-read', '2024-09-02 09:46:54.835456', '2024-09-02 09:46:54.835456');


--
-- Data for Name: shelf_searches; Type: TABLE DATA; Schema: public; Owner: postgres
--

INSERT INTO public.shelf_searches (shelf_search_id, shelf_id, num_books, time_start, time_complete, total_book_count, books_returned, search_type) OVERRIDING SYSTEM VALUE VALUES (1, 1, 4, '2024-09-02 09:46:54.835456', '2024-09-02 09:46:58.51341', 127, '{1,2,3,4}', 'Shuffle');
INSERT INTO public.shelf_searches (shelf_search_id, shelf_id, num_books, time_start, time_complete, total_book_count, books_returned, search_type) OVERRIDING SYSTEM VALUE VALUES (2, 1, 4, '2024-09-02 23:03:45.622513', '2024-09-02 23:03:45.626169', 128, '{6,7,8,9}', 'Shuffle');
INSERT INTO public.shelf_searches (shelf_search_id, shelf_id, num_books, time_start, time_complete, total_book_count, books_returned, search_type) OVERRIDING SYSTEM VALUE VALUES (3, 1, 4, '2024-09-03 04:25:27.736715', '2024-09-03 04:25:37.06636', 128, '{11,12,13,14}', 'Shuffle');
INSERT INTO public.shelf_searches (shelf_search_id, shelf_id, num_books, time_start, time_complete, total_book_count, books_returned, search_type) OVERRIDING SYSTEM VALUE VALUES (4, 4, 4, '2024-09-03 04:39:16.877058', '2024-09-03 04:39:24.836954', 128, '{16,17,18,19}', 'Shuffle');
INSERT INTO public.shelf_searches (shelf_search_id, shelf_id, num_books, time_start, time_complete, total_book_count, books_returned, search_type) OVERRIDING SYSTEM VALUE VALUES (5, 4, 4, '2024-09-03 18:26:08.26731', '2024-09-03 18:26:17.246519', 128, '{21,22,23,24}', 'Shuffle');
INSERT INTO public.shelf_searches (shelf_search_id, shelf_id, num_books, time_start, time_complete, total_book_count, books_returned, search_type) OVERRIDING SYSTEM VALUE VALUES (6, 6, 2, '2024-09-04 01:42:59.489135', '2024-09-04 01:43:02.575516', 2, '{26,27}', 'Shuffle');
INSERT INTO public.shelf_searches (shelf_search_id, shelf_id, num_books, time_start, time_complete, total_book_count, books_returned, search_type) OVERRIDING SYSTEM VALUE VALUES (7, 6, 2, '2024-09-04 01:52:55.270739', '2024-09-04 01:52:55.271589', 2, '{26,27}', 'Shuffle');
INSERT INTO public.shelf_searches (shelf_search_id, shelf_id, num_books, time_start, time_complete, total_book_count, books_returned, search_type) OVERRIDING SYSTEM VALUE VALUES (8, 6, 2, '2024-09-04 01:52:59.240974', '2024-09-04 01:52:59.241595', 2, '{26,27}', 'Shuffle');
INSERT INTO public.shelf_searches (shelf_search_id, shelf_id, num_books, time_start, time_complete, total_book_count, books_returned, search_type) OVERRIDING SYSTEM VALUE VALUES (9, 4, 4, '2024-09-04 22:33:44.123466', '2024-09-04 22:33:54.186585', 129, '{36,37,4,11}', 'Shuffle');
INSERT INTO public.shelf_searches (shelf_search_id, shelf_id, num_books, time_start, time_complete, total_book_count, books_returned, search_type) OVERRIDING SYSTEM VALUE VALUES (10, 4, 4, '2024-09-05 02:08:56.93004', '2024-09-05 02:09:05.946273', 129, '{9,41,42,3}', 'Shuffle');
INSERT INTO public.shelf_searches (shelf_search_id, shelf_id, num_books, time_start, time_complete, total_book_count, books_returned, search_type) OVERRIDING SYSTEM VALUE VALUES (11, 4, 4, '2024-09-05 02:11:25.101794', '2024-09-05 02:11:25.106478', 129, '{21,2,48,49}', 'Shuffle');
INSERT INTO public.shelf_searches (shelf_search_id, shelf_id, num_books, time_start, time_complete, total_book_count, books_returned, search_type) OVERRIDING SYSTEM VALUE VALUES (12, 4, 4, '2024-09-05 02:11:30.036162', '2024-09-05 02:11:30.037503', 129, '{23,51,52,53}', 'Shuffle');
INSERT INTO public.shelf_searches (shelf_search_id, shelf_id, num_books, time_start, time_complete, total_book_count, books_returned, search_type) OVERRIDING SYSTEM VALUE VALUES (13, 13, 4, '2024-09-07 15:53:06.456185', '2024-09-07 15:53:11.286964', 22, '{54,55,56,57}', 'Shuffle');
INSERT INTO public.shelf_searches (shelf_search_id, shelf_id, num_books, time_start, time_complete, total_book_count, books_returned, search_type) OVERRIDING SYSTEM VALUE VALUES (14, 13, 4, '2024-09-07 15:53:06.456185', '2024-09-07 15:53:11.286964', 22, '{54,55,56,57}', 'Shuffle');
INSERT INTO public.shelf_searches (shelf_search_id, shelf_id, num_books, time_start, time_complete, total_book_count, books_returned, search_type) OVERRIDING SYSTEM VALUE VALUES (15, 13, 4, '2024-09-07 15:57:54.961436', '2024-09-07 15:57:54.962409', 22, '{76,77,78,79}', 'Shuffle');
INSERT INTO public.shelf_searches (shelf_search_id, shelf_id, num_books, time_start, time_complete, total_book_count, books_returned, search_type) OVERRIDING SYSTEM VALUE VALUES (16, 13, 4, '2024-09-07 15:58:02.314147', '2024-09-07 15:58:02.315018', 22, '{80,81,56,77}', 'Shuffle');
INSERT INTO public.shelf_searches (shelf_search_id, shelf_id, num_books, time_start, time_complete, total_book_count, books_returned, search_type) OVERRIDING SYSTEM VALUE VALUES (17, 13, 4, '2024-09-07 15:58:09.69231', '2024-09-07 15:58:09.693273', 22, '{57,77,81,87}', 'Shuffle');
INSERT INTO public.shelf_searches (shelf_search_id, shelf_id, num_books, time_start, time_complete, total_book_count, books_returned, search_type) OVERRIDING SYSTEM VALUE VALUES (18, 4, 4, '2024-09-07 20:20:52.81133', '2024-09-07 20:21:02.862943', 129, '{88,89,90,41}', 'Shuffle');
INSERT INTO public.shelf_searches (shelf_search_id, shelf_id, num_books, time_start, time_complete, total_book_count, books_returned, search_type) OVERRIDING SYSTEM VALUE VALUES (19, 1, 4, '2024-09-02 09:46:54.835456', '2024-09-02 09:46:58.51341', 127, '{1,2,3,4}', 'Shuffle');


--
-- Name: books_book_id_seq; Type: SEQUENCE SET; Schema: public; Owner: postgres
--

SELECT pg_catalog.setval('public.books_book_id_seq', 98, true);


--
-- Name: library_searches_library_search_id_seq; Type: SEQUENCE SET; Schema: public; Owner: postgres
--

SELECT pg_catalog.setval('public.library_searches_library_search_id_seq', 28, true);


--
-- Name: shelf_searches_shelf_search_id_seq; Type: SEQUENCE SET; Schema: public; Owner: postgres
--

SELECT pg_catalog.setval('public.shelf_searches_shelf_search_id_seq', 19, true);


--
-- Name: shelves_shelf_id_seq; Type: SEQUENCE SET; Schema: public; Owner: postgres
--

SELECT pg_catalog.setval('public.shelves_shelf_id_seq', 19, true);


--
-- PostgreSQL database dump complete
--

