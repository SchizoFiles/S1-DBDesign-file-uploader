-- SCHEMA: public

-- DROP SCHEMA IF EXISTS public ;

CREATE SCHEMA IF NOT EXISTS public
    AUTHORIZATION postgres;

COMMENT ON SCHEMA public
    IS 'standard public schema';

GRANT ALL ON SCHEMA public TO PUBLIC;

GRANT ALL ON SCHEMA public TO postgres;

/* 
 Stores file information about the files
 ----------------------------------------
 fileId is a unique id given to each file 
 fileDir is for the file location
 fileName is the filename with extension, the column is limited to the windows file path limit
 fileType is for the files MIME type
 dateAdded is to sort of log when the entry was added
*/
CREATE TABLE fileData(
    fileId INTEGER NOT NULL PRIMARY KEY,
    filerDir TEXT,
    fileName VARCHAR(256),
    fileType TEXT,
    dateAdded INTEGER
	);

/*
  for keeping tags and assighning id's
  general idea, save data by assigning a number to each tag in the tags table instead of the whole tag string,
  then just pull the tag string from the number when grabbing data
  this one works the same way as fileData but lesser
  also this standardises tags across the 2 whole tabes that use tags
  ----------------------------------------
  tagId is the unique id of the tag
  tag is the string for the tag or the actuall tag ("videos", "movies", "music", etc)

*/
CREATE TABLE tags(
    tagId INTEGER NOT NULL PRIMARY KEY,
    tag TEXT NOT NULL
  );

/*
 Assighns tags to a file through a tagId and file Id
 through some spooky sql magic and other tomfoolery you are able to grab the tags of a file
 there can be multipe tags to a file by just having a line per tag
 you can also nest tags by assighning them a parent tag with 0 being no parent
 ----------------------------------------
 fileId is the file's id from the fileData table
 tagId is the tag's id from the tags table
 parentTag is the parent of a tag, used for nesting tags and creating sub categories, with 0 being none (still iffy on this one)

*/
CREATE TABLE fileTag(
    fileId INTEGER NOT NULL,
    tagId INTEGER NOT NULL,
    parentTag INTEGER NOT NULL DEFAULT 0
  );

/*
  Sources files were pulled from
  more for record keeping than anything, gives a source for were a file comes from,
  a file can have multiple sources
  ----------------------------------------
  fileId the file's id from fileData
  source a string for where it came from, NOTE: I'll have to standardise it somehow later (probably do what I did with tags)

*/
CREATE TABLE fileSource(
    fileId INTEGER NOT NULL,
    source TEXT NOT NULL
  );
