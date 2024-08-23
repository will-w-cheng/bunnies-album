# bunnies-album



sudo apt-get update                                                                                                ─╯
sudo apt-get install python3-dev default-libmysqlclient-dev build-essential


mysql -u root -p
CREATE DATABASE newjeans_albums;
CREATE USER 'newjeans_user'@'localhost' IDENTIFIED BY 'password';
GRANT ALL PRIVILEGES ON newjeans_albums.* TO 'newjeans_user'@'localhost';
FLUSH PRIVILEGES;
EXIT;
