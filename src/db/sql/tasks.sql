CREATE TABLE tasks (
	id SERIAL PRIMARY KEY,
	description VARCHAR(30) NOT NULL,
	priority SMALLINT,
	is_completed BOOLEAN NOT NULL
);
