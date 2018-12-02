CREATE DATABASE IF NOT EXISTS novel CHARACTER SET utf8 COLLATE utf8_general_ci;
USE novel;
DROP TABLE IF EXISTS post;
DROP TABLE IF EXISTS user;
CREATE TABLE user (
  id INT PRIMARY KEY AUTO_INCREMENT,
  username varchar(10) UNIQUE NOT NULL,
  password varchar(20) NOT NULL
);
CREATE TABLE post (
  id INT PRIMARY KEY AUTO_INCREMENT,
  author_id INT NOT NULL,
  created TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
  title varchar(30) unique NOT NULL,
  body TEXT NOT NULL,
  FOREIGN KEY (author_id) REFERENCES user (id)
);
