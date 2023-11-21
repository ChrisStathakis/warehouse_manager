@ECHO OFF
start cmd.exe /C "python -Xutf8 manage.py dumpdata > db_backup.json"