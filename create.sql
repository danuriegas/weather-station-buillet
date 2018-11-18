CREATE TABLE WEATHER_MEASUREMENT(
   ID BIGINT NOT NULL AUTO_INCREMENT,
   REMOTE_ID BIGINT,
   AMBIENT_TEMPERATURE DECIMAL(6,2) NOT NULL,
   BAROMETRIC_PRESSURE DECIMAL(6,2) NOT NULL,
   HUMIDITY DECIMAL(6,2) NOT NULL,
   GROUND_TEMPERATURE DECIMAL(6,2) NOT NULL,
   VIS_LIGHT DECIMAL(6,2) NOT NULL,
   IR_LIGHT DECIMAL(6,2) NOT NULL,
   UV_INDEX DECIMAL(6,2) NOT NULL,
   WIND_DIRECTION DECIMAL(6,2) NULL,
   WIND_SPEED DECIMAL(6,2) NOT NULL,
   WIND_GUST_SPEED DECIMAL(6,2) NOT NULL,
   RAINFALL DECIMAL (6,2) NOT NULL,
   CREATED TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
   PRIMARY KEY ( ID )
);