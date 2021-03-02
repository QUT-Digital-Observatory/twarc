import sqlite3


init_statements = """
/* result_page table
Each page of results from the Twitter API has a row in result_page.
The 'meta' object from the result page is stored in this table (in columns corresponding
to the key names).
There is currently no way to mark pages as part of the same query result, but that is
possible if the data were to be passed in as additional metadata from twarc as the pages
are inserted.
*/
create table result_page (
    page_id integer primary key,
    newest_id text,
    oldest_id text,
    result_count integer,
    next_token text
);

/* tweet table
*/
create table tweet (
    result_page_id integer references result_page (page_id),
    tweet_id text,
    possibly_sensitive integer,
    lang text,
    source text,
    reply_settings text,
    created_at real,  -- use julianday(date_string_from_twitter) on insert
    text text,
    conversation_id text,
    author_id text,
    retweet_count integer,
    reply_count integer,
    like_count integer,
    quote_count integer,
    primary key (result_page_id, tweet_id)
);

/* media table
*/
create table media (
    media_key text primary key,
    result_page_id integer references result_page (page_id),
    height integer,
    url text,
    type text,
    width integer,
    duration_ms integer,
    preview_image_url text,
    view_count integer
)

/* tweet_media table
*/
create table tweet_media (
    result_page_id integer,
    tweet_id text,
    media_key text references media (media_key),
    
    foreign key (result_page_id, tweet_id) references tweet (result_page_id, tweet_id),
    primary key (result_page_id, tweet_id, media_key)
);

"""