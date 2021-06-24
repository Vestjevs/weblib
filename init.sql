CREATE TABLE users (
    id INTEGER NOT NULL, 
    username VARCHAR(50), 
    pw_hash VARCHAR(100), 
    PRIMARY KEY (id), 
    UNIQUE (username)
);

CREATE TABLE books (
    id INTEGER NOT NULL, 
    title VARCHAR(50), 
    abstract TEXT, 
    PRIMARY KEY (id), 
    UNIQUE (title), 
    UNIQUE (abstract)
);

CREATE TABLE authors (
    id INTEGER NOT NULL, 
    name VARCHAR(50), 
    biography TEXT, 
    PRIMARY KEY (id), 
    UNIQUE (name), 
    UNIQUE (biography)
);

CREATE TABLE association (
    books_id INTEGER, 
    authors_id INTEGER, 
    FOREIGN KEY(books_id) REFERENCES books (id), 
    FOREIGN KEY(authors_id) REFERENCES authors (id)
);