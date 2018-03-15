-- route id:
--   date date
--   typ text
--   place text
--   rid int

-- always has one line, the last seen post from disqus
CREATE TABLE lastseenpost
       ( postid TEXT );

CREATE TABLE postcount
       ( dat TEXT
       , typ TEXT
       , place TEXT
       , rid INT
       , threadid TEXT
       , posts INT
       , latest TEXT
       , commenter TEXT
       , PRIMARY KEY (dat, typ, place, rid)
       );

CREATE TABLE routes
       ( dat TEXT
       , typ TEXT
       , place TEXT
       , rid INT
       , name TEXT
       , subname TEXT
       , grade TEXT
       , setter TEXT
       , color TEXT
       , toprope BOOLEAN
       , toppas BOOLEAN
       , lead BOOLEAN
       , sector TEXT
       , new_ BOOLEAN
       , lastcall BOOLEAN
       , retired BOOLEAN
       , kids BOOLEAN
       , imgurl TEXT
       , PRIMARY KEY (dat, typ, place, rid)
       );
