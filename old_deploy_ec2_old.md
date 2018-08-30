# Deployment
Here we explain how to deploy the webpage on an amazon ec2 server.

## SSH to the server


Install all the required packages using yum

	chmod 400 firstkeypair.pem
    ssh -i firstkeypair.pem ec2-user@18.220.191.231
   
## Install all the required packages


	sudo yum group install "Development Tools"
    sudo yum install python-pip
    sudo yum install graphviz-devel
    sudo pip install pygraphviz
    sudo pip install python-dotenv
    sudo pip install flask
    sudo pip install networkx
    
   
## Run flask

	ssh -i firstkeypair.pem ec2-user@18.220.191.231
    cd greedy-superstring-conjecture/
    flask run
    
In order to check that flask is running, one can run the following commands:

	ssh -i firstkeypair.pem ec2-user@18.220.191.231
    links
    http://localhost:5000
    
## Install Apache

	sudo yum install httpd mod_ssl
    sudo yum install mod_wsgi

Start Apache:

	sudo systemctl start httpd

Be sure that Apache starts at boot:

	sudo systemctl enable httpd

To check the status of Apache:

	sudo systemctl status httpd

To stop Apache:

	sudo systemctl stop httpd    

To restart Apache:

	sudo apachectl restart

Apache config file:

	/etc/httpd/conf/httpd.conf

Apache log file:

	/etc/httpd/logs/error_log


## Setup Flask

	sudo mkdir /var/www/html/csc
	sudo cp -R ~/greedy-superstring-conjecture/* /var/www/html/csc/
	sudo chmod -R 755 /var/www/html/csc
	
	