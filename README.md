# duplicity-remover

duplicity-remover is a simple script written in Python that keeps N full backups and removes all backups that are older than that. You can use it to clean up duplicity backup files without having the PGP secret key.

*Why do I not use the built-in function of duplicity?* I download the encrypted backup to a Raspberry PI and `duplicity remove-all-but-n-full` requires the PGP secret key. For security reasons I don't want to have the key on the Raspberry so that's why I wrote this script.

Testet on Python 2.7.11 

##Example

```
./duplicity-remover.py --remove-all-but-n-full 3 --force /backups/files
```
will keep 3 full backups and removes all older full and incremental backups. 
The '--force' option will delete the files. To try this script, you can leave it out. 

