# Import required python libraries
import os
import time
import datetime
import sys 
import boto3
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
import smtplib

# MySQL database details
dbs = ["pradan_hr", "pradan_grow", "pradan_mis", "pradan_intranet", "pradan_project", "pradan_sirf", "pradan_tds", "pradan_visitingcard", "pradan_workunit", "apcmis"]
DB_HOST = '****'
DB_USER = '****'
DB_USER_PASSWORD = '****'
BACKUP_PATH = '/opt/other/tmpdbbackup'
S3_BUCKET_NAME = 'pradandbbackup'

s3 = boto3.resource('s3')
bucket = s3.Bucket(S3_BUCKET_NAME)

# Getting current datetime
now = datetime.datetime.now()
today = now.strftime("%Y-%m-%d-%H:%M")

# Checking if backup folder exists or not. If not exists, create it.
print("Creating backup folder")
if not os.path.exists(BACKUP_PATH):
    os.makedirs(BACKUP_PATH)

for db in dbs:
    print(db)
    suffix = "/" + db + "-" + today + ".sql"
    print(suffix)
    dumpcmd = f"mysqldump -u {DB_USER} -p{DB_USER_PASSWORD} -h {DB_HOST} {db} > {BACKUP_PATH}{suffix}"
    print(f"Creating Db-backup for {db}")
    
    try:
        result = os.system(dumpcmd)
        print(result)

        if result == 0:
            backup_file = BACKUP_PATH + suffix
            zipgen = f"cat {BACKUP_PATH}{suffix} | gzip -9 > {BACKUP_PATH}{suffix}.gz"
            os.system(zipgen)
            print(f"DB-backup for {db} ..DONE.")

            file_path = BACKUP_PATH + suffix + ".gz"
            print(file_path)

            with open(file_path, 'rb') as data:
                file_name = os.path.basename(file_path)
                print(f'Uploading {file_name}')
                bucket.put_object(Key=f'{db}/{today}/{file_name}', Body=data)

            print(f"Removing DB-backup file {db}-{today}.sql.gz")
            os.remove(BACKUP_PATH + suffix)
            os.remove(BACKUP_PATH + suffix + ".gz")

        else:
            os.remove(BACKUP_PATH + suffix)
            mail = smtplib.SMTP('smtp.gmail.com', 587)
            mail.starttls()
            mail.login("serverforpradan@pradan.net", "Pradan@135790")

            msg = MIMEMultipart('alternative')
            msg['Subject'] = "CRITICAL: DB BACKUP FAILED"
            msg['TO'] = "***@pradan.net,***@pardan.net"

            body = f"DB BACKUP FAILED FOR DB: {db}"
            body = MIMEText(body, "plain")
            msg.attach(body)
            print(msg)

            mail.sendmail("***@pradan.net", "***@pradan.net", msg.as_string())
            mail.quit()

    except OSError as e:
        print(f"EXCEPTION OCCURRED: {e}")
        pass
