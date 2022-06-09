# Connecting to a remote server

ssh ip_address

# copy files from local to EC2 instance

scp -r folder_path_to_be_copied user_name@IP:destination_path

# open a file

cat file_name_with_path

# Setting up a cronjob

systemctl status cron # Check if the cron job is set up

crontab -e

0 10 17 * * command >> path_/a_file.log 2>&1

# Working with Screens - Will mitigate the risk of loosing connection to the server

screen -ls # list all the screens

screen # create a new screen

## Once you are inside the screen you can run your command

# Checking the jobs run on the machine

ps aux | grep "any_keywords"

top # will return a live vew of all the jobs that are being run

sudo pkill -u 'user_name' # will kill all the jobs run by the user

# Check the folder constituents in S3

aws s3 ls s3_path

# working with jupyter

jupyter notebook stop port_number # by default the port is 8888

