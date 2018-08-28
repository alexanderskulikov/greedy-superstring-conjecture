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
    sudo /usr/sbin/apachectl start
    sudo yum install mod_wsgi
    sudo ln -sT ~/greedy-superstring-conjecture/ /var/www/html/csc
    

