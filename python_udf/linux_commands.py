# Connecting to a remote server

ssh ip_address

# copy files from local to EC2 instance

scp -r folder_path_to_be_copied user_name@IP:destination_path

# open a file

cat file_name_with_path

# Setting up a cronjob

crontab -e

0 10 17 * * command >> path_/a_file.log 2>&1
