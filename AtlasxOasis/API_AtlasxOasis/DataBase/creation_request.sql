CREATE TABLE AUTHENTICATION (
  PRIMARY KEY (type_auth, id_user),
  type_auth      text NOT NULL,
  id_user        bigint NOT NULL,
  token          text
);

CREATE TABLE TICKET (
  PRIMARY KEY (id_ticket),
  id_ticket bigint NOT NULL,
  id_ticket_type bigint NOT NULL,
  status_ticket  text
);

CREATE TABLE TICKET_TYPE_EVENT (
  PRIMARY KEY (id_ticket_type),
  id_ticket_type bigint GENERATED ALWAYS AS IDENTITY,
  id_event       bigint NOT NULL,
  price          decimal(10,2),
  label          text,
  description    text,
  quantity       integer
);

CREATE TABLE CATEGORY (
  PRIMARY KEY (id_category),
  id_category bigint GENERATED ALWAYS AS IDENTITY,
  label        text
);

CREATE TABLE CUSTOMER (
  PRIMARY KEY (id_customer),
  id_customer bigint NOT NULL,
  firstname text,
  lastname text
);

CREATE TABLE EVENT (
  PRIMARY KEY (id_event),
  id_event          bigint GENERATED ALWAYS AS IDENTITY,
  id_organizer      bigint NOT NULL,
  name              text,
  start_date        timestamp,
  end_date          timestamp,
  creation_date     timestamp,
  event_status      text,
  max_capacity      integer,
  description       text,
  metadata          text
);

CREATE TABLE LOCATION (
  PRIMARY KEY (id_location),
  id_location      bigint GENERATED ALWAYS AS IDENTITY,
  max_capacity     integer,
  name             text,
  address          text,
  city             text,
  postal_code      text,
  longitude        decimal(10,6),
  latitude         decimal(10,6),
  accessibility    boolean,
  nearby_transport text
);

CREATE TABLE Waiting_list (
  PRIMARY KEY (id_customer, id_event),
  id_customer    bigint NOT NULL,
  id_event       bigint NOT NULL,
  added_date     timestamp,
  status_waiting text,
  type_priority  text
);

CREATE TABLE MEDIA (
  PRIMARY KEY (id_media),
  id_media        bigint GENERATED ALWAYS AS IDENTITY,
  label           text,
  description     text,
  format_media    text,
  url             text,
  usage_media     text,
  upload_date     timestamp,
  sharing_status  text NOT NULL,
  id_user         bigint NOT NULL,
  id_event        bigint,
  id_location     bigint
);

CREATE TABLE PROMOTION (
  PRIMARY KEY (id_promotion),
  id_promotion      bigint NOT NULL,
  id_promotion_type bigint NOT NULL,
  start_date        timestamp,
  end_date          timestamp,
  status_promotion  text,
  type_promotion    text,
  description       text
);

CREATE TABLE PROMOTION_TYPE (
  PRIMARY KEY (id_promotion_type),
  id_promotion_type     bigint GENERATED ALWAYS AS IDENTITY,
  name                  text,
  description           text,
  price                 decimal(10,2)
);

CREATE TABLE Promotion_Event (
  PRIMARY KEY (id_promotion, id_event),
  id_promotion  bigint NOT NULL,
  id_event        bigint NOT NULL
);

CREATE TABLE SALE_OBJECT (
  PRIMARY KEY (id_sale_object),
  id_sale_object bigint GENERATED ALWAYS AS IDENTITY,
  id_payment    bigint NULL,
  type_object     text
);

CREATE TABLE ORGANIZER (
  PRIMARY KEY (id_organizer),
  id_organizer   bigint NOT NULL,
  siret          text
);

CREATE TABLE Organizer_Event (
  PRIMARY KEY (id_event, id_organizer),
  id_event       bigint NOT NULL,
  id_organizer   bigint NOT NULL,
  role           text
);

CREATE TABLE PAYMENT (
  PRIMARY KEY (id_payment),
  id_payment        bigint GENERATED ALWAYS AS IDENTITY,
  id_user           bigint NOT NULL,
  price             decimal(10,2),
  status_amount    text,
  status_payment    text,
  date_payment      timestamp,
  methode_payment   text
);

CREATE TABLE Event_Location (
  PRIMARY KEY (id_location, id_event),
  id_location      bigint NOT NULL,
  id_event         bigint NOT NULL
);

CREATE TABLE Event_Category (
  PRIMARY KEY (id_event, id_category),
  id_event    bigint NOT NULL,
  id_category bigint NOT NULL
);

CREATE TABLE Follow (
  PRIMARY KEY (id_follower_customer, id_followed_user),
  id_follower_customer bigint NOT NULL,
  id_followed_user bigint NOT NULL,
  date_follow      timestamp,
  status_follow    text
);

CREATE TABLE APP_USER (
  PRIMARY KEY (id_user),
  id_user   bigint GENERATED ALWAYS AS IDENTITY,
  type_user text,
  username         text,
  email            text UNIQUE,
  description      text
);

CREATE TABLE LIKE_CUSTOMER (
  PRIMARY KEY (id_customer, id_event),
  id_customer bigint NOT NULL,
  id_event bigint NOT NULL,
  date_like timestamp
);

ALTER TABLE AUTHENTICATION ADD FOREIGN KEY (id_user) REFERENCES APP_USER (id_user) ON DELETE CASCADE;

ALTER TABLE TICKET ADD FOREIGN KEY (id_ticket_type) REFERENCES TICKET_TYPE_EVENT (id_ticket_type);
ALTER TABLE TICKET ADD FOREIGN KEY (id_ticket) REFERENCES SALE_OBJECT (id_sale_object);

ALTER TABLE TICKET_TYPE_EVENT ADD FOREIGN KEY (id_event) REFERENCES EVENT (id_event);

ALTER TABLE CUSTOMER ADD FOREIGN KEY (id_customer) REFERENCES APP_USER (id_user);

ALTER TABLE EVENT ADD FOREIGN KEY (id_organizer) REFERENCES ORGANIZER (id_organizer) ON DELETE CASCADE;

ALTER TABLE Waiting_list ADD FOREIGN KEY (id_event) REFERENCES EVENT (id_event);
ALTER TABLE Waiting_list ADD FOREIGN KEY (id_customer) REFERENCES CUSTOMER (id_customer);

ALTER TABLE MEDIA ADD FOREIGN KEY (id_user) REFERENCES APP_USER (id_user) ON DELETE CASCADE;
ALTER TABLE MEDIA ADD FOREIGN KEY (id_event) REFERENCES EVENT (id_event);
ALTER TABLE MEDIA ADD FOREIGN KEY (id_location) REFERENCES LOCATION (id_location);

ALTER TABLE PROMOTION ADD FOREIGN KEY (id_promotion) REFERENCES SALE_OBJECT (id_sale_object);
ALTER TABLE PROMOTION ADD FOREIGN KEY (id_promotion_type) REFERENCES PROMOTION_TYPE (id_promotion_type);

ALTER TABLE SALE_OBJECT ADD FOREIGN KEY (id_payment) REFERENCES PAYMENT (id_payment);

ALTER TABLE ORGANIZER ADD FOREIGN KEY (id_organizer) REFERENCES APP_USER (id_user);

ALTER TABLE Organizer_Event ADD FOREIGN KEY (id_organizer) REFERENCES ORGANIZER (id_organizer);
ALTER TABLE Organizer_Event ADD FOREIGN KEY (id_event) REFERENCES EVENT (id_event);

ALTER TABLE PAYMENT ADD FOREIGN KEY (id_user) REFERENCES APP_USER (id_user);

ALTER TABLE Event_Location ADD FOREIGN KEY (id_event) REFERENCES EVENT (id_event);
ALTER TABLE Event_Location ADD FOREIGN KEY (id_location) REFERENCES LOCATION (id_location);

ALTER TABLE Event_Category ADD FOREIGN KEY (id_category) REFERENCES CATEGORY (id_category);
ALTER TABLE Event_Category ADD FOREIGN KEY (id_event) REFERENCES EVENT (id_event);

ALTER TABLE Follow ADD FOREIGN KEY (id_follower_customer) REFERENCES CUSTOMER (id_customer) ON DELETE CASCADE;
ALTER TABLE Follow ADD FOREIGN KEY (id_followed_user) REFERENCES APP_USER (id_user) ON DELETE CASCADE;

ALTER TABLE LIKE_CUSTOMER ADD FOREIGN KEY (id_customer) REFERENCES CUSTOMER (id_customer) ON DELETE CASCADE;
ALTER TABLE LIKE_CUSTOMER ADD FOREIGN KEY (id_event) REFERENCES EVENT (id_event) ON DELETE CASCADE;
