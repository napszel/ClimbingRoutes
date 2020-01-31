ALTER TABLE routes ADD COLUMN vlid INT; 

ALTER TABLE routes ADD COLUMN full_name TEXT; 

ALTER TABLE routes ADD COLUMN vlsector TEXT; 

ALTER TABLE routes ADD COLUMN color_codes TEXT; 

CREATE UNIQUE INDEX vlid_unique ON routes(vlid);
 
