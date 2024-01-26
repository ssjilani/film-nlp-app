CREATE TABLE IF NOT EXISTS script_data
    (
    line_id VARCHAR(255) PRIMARY KEY NOT NULL,
    character_name VARCHAR(100),
    dialogue VARCHAR(5000),
    character_line_number INT,
    film VARCHAR(100)
    );