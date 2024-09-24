CREATE TABLE IF NOT EXISTS telemetry (
    id SERIAL PRIMARY KEY,
    timestamp INTEGER,
    value REAL,
    status SMALLINT
);