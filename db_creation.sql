create table quotes
(
    quote_id          SERIAL PRIMARY KEY,
    message_id        integer UNSIGNED NOT NULL,
    from_username     varchar(30),
    from_name         varchar(30),
    from_lastname     varchar(30),
    message_date_time timestamp,
    message_text      char(250)
);

