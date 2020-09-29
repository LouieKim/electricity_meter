CREATE TABLE IF NOT EXISTS modbus_info (
  point_id INTEGER PRIMARY KEY AUTOINCREMENT NOT NULL,
  slave INTEGER NOT NULL,
  function_code INTEGER NOT NULL,
  map_address INTEGER NOT NULL,
  unit VARCHAR(50),
  UNIQUE(point_id)
);

CREATE TABLE IF NOT EXISTS history (
  point_id INTEGER,
  date DATE NOT NULL,
  value INTEGER NOT NULL,
  PRIMARY KEY(point_id, date),
  FOREIGN KEY(point_id) REFERENCES modbus_info(point_id) ON DELETE CASCADE
);

CREATE TABLE IF NOT EXISTS calc_history (
  point_id INTEGER,
  date DATE NOT NULL,
  value INTEGER NOT NULL,
  PRIMARY KEY(point_id, date),
  FOREIGN KEY(point_id) REFERENCES modbus_info(point_id) ON DELETE CASCADE
);