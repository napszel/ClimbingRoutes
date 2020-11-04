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
       , vlid INT
       , name TEXT
       , full_name TEXT
       , grade TEXT
       , setter TEXT
       , color TEXT
       , color_codes TEXT
       , toprope BOOLEAN
       , toppas BOOLEAN
       , lead BOOLEAN
       , sector TEXT
       , vlsector TEXT
       , new_ BOOLEAN
       , lastcall BOOLEAN
       , retired BOOLEAN
       , kids BOOLEAN
       , imgurl TEXT
       , sectorimg TEXT
       , sector1 TEXT
       , sector2 TEXT
       , sector3 TEXT
       , polygoon TEXT
       , PRIMARY KEY (dat, typ, place, rid)
       );

