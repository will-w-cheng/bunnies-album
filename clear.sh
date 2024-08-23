#!/bin/bash

mysql -u newjeans_user -ppassword -e "USE newjeans_albums; SET FOREIGN_KEY_CHECKS = 0; DROP TABLE IF EXISTS album; SET FOREIGN_KEY_CHECKS = 1;"


flask db init
flask db migrate -m "Initial migration"
flask db upgrade
