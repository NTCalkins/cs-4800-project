CREATE TABLE user_info(
	id BIGSERIAL NOT NULL PRIMARY KEY,
	first_name VARCHAR(50) NOT NULL,
	last_name VARCHAR(50) NOT NULL,
	email VARCHAR(50) NOT NULL,
	phone VARCHAR(10) NOT NULL,
	address_id BIGINT NOT NULL REFERENCES address_info(id) --relationship with address_info
)

CREATE TABLE driver_info(
	id BIGSERIAL NOT NULL PRIMARY KEY,
	first_name VARCHAR(50) NOT NULL,
	last_name VARCHAR(50) NOT NULL,
	email VARCHAR(50) NOT NULL,
	phone VARCHAR(10) NOT NULL
)

CREATE TABLE restaurant_info(
	id BIGSERIAL NOT NULL PRIMARY KEY,
	restaurant_name VARCHAR(50) NOT NULL,
	address_id BIGINT NOT NULL REFERENCES address_info(id), --relationship with address-info
	email VARCHAR(50), --can be null because restaurants might not have an email
	phone VARCHAR(10) NOT NULL,
	opening_time TIME NOT NULL,
	closing_time TIME NOT NULL
)

CREATE TABLE address_info( --relationship with user_info and restaurant_info
	id BIGSERIAL NOT NULL PRIMARY KEY,
	street_address VARCHAR(50) NOT NULL,
  city_id BIGINT NOT NULL REFERENCES city_info(id), --relationship with city_info
  state_id BIGINT NOT NULL REFERENCES state_info(id), --relationship with state_info
  country_id BIGINT NOT NULL REFERENCES country_info(id), --relationship with country_info
	zipcode VARCHAR(5) NOT NULL
)

CREATE TABLE city_info( --relationship with address-info
   id BIGSERIAL NOT NULL PRIMARY KEY,
   city_name VARCHAR(50) NOT NULL,
)

CREATE TABLE state_info( --relationship with address-info
   id BIGSERIAL NOT NULL PRIMARY KEY,
   state_name VARCHAR(50) NOT NULL,
)

CREATE TABLE country_info( --relationship with address-info
   id BIGSERIAL NOT NULL PRIMARY KEY,
   country_name VARCHAR(50) NOT NULL,
)
