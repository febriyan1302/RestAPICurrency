#!/usr/bin/env bash
docker exec restapicurrency_mysql_1 sh -c 'exec mysqldump --all-databases -uroot -p"$MYSQL_ROOT_PASSWORD"' < databases.sql