### 备份还原
1. 使用mysqldump进行备份， mysql命令进行还原，生成.sql文件进行备份

    ```bash
    mysqldump --column-statistics=0 --set-gtid-purged=off --user=dev --password=123213 --host=localhost --port=3306 database_name > /localpath/home/Downloads/backup.sql 

    mysql --user=dev --password=123213 --host=localhost --port=3306 database_name < /localpath/home/Downloads/backup.sql 
    ```