CREATE TABLE IF NOT EXISTS modbus_info (
  point_id numeric NOT NULL, 
  slave numeric NOT NULL,
  function_code numeric NOT NULL,
  map_address numeric NOT NULL,
  description TEXT,
  PRIMARY KEY(point_id)
);

CREATE TABLE IF NOT EXISTS history (
  point_id numeric NOT NULL,
  date TEXT NOT NULL,
  value numeric NOT NULL, 
  PRIMARY KEY(point_id, date)
);

CREATE TABLE IF NOT EXISTS graph_history (
  point_id numeric NOT NULL,
  date TEXT NOT NULL,
  value numeric NOT NULL, 
  PRIMARY KEY(point_id, date)
);
