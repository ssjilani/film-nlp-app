CREATE TABLE IF NOT EXISTS script_data
    (
    line_id VARCHAR(500) PRIMARY KEY NOT NULL,
    character_name VARCHAR(100),
    dialogue VARCHAR(5000),
    character_line_number INT,
    film VARCHAR(255),
    url VARCHAR(500),
	franchise VARCHAR(50)
    );
	
-- load data from CSV into script_data table at initialization
COPY script_data(line_id, character_name, dialogue, character_line_number, film, url, franchise)
FROM '/docker-entrypoint-initdb.d/script_data_processed.csv' DELIMITER ',' CSV HEADER;