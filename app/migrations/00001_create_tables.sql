CREATE TABLE IF NOT EXISTS wswe_metadata {
    db_version INT
}

CREATE TABLE IF NOT EXISTS restaurants (
    id  UUID PRIMARY KEY,
    name TEXT NOT NULL,
    price INT
);