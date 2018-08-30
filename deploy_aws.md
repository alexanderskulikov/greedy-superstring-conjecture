# Deployment
Here we explain how to deploy the webpage on an amazon AWS server.

## Launch Instance

Go to [https://console.aws.amazon.com/ec2/](https://console.aws.amazon.com/ec2/), click **Launch Instance**, choose **Ubuntu Server 16.04 LTS (HVM)**, then **t2.micro**. Now **Edit Security Groups**, add *SSH* and *HTTP* with Source *Anywhere*. Download the provided private key. The name of our private key file is *firstkeypair.pem*. We need to change its permission:
```
chmod 400 firstkeypair.pem
```

## SSH to the server
Our Public DNS is *ec2-18-191-207-139.us-east-2.compute.amazonaws.com*. Thus, we can ssh to this machine using the command
```
ssh -i "firstkeypair.pem" ubuntu@ec2-18-191-207-139.us-east-2.compute.amazonaws.com
```

## Install Python 3, pip, and Apache
```
sudo apt-get update
sudo apt install python3
sudo apt-get install python3-pip
sudo pip3 install --upgrade pip
sudo apt-get install apache2
sudo apt-get install libapache2-mod-wsgi-py3
```

## Install the required packages

```
sudo pip3 install flask
sudo pip3 install networkx
sudo apt-get install graphviz libgraphviz-dev graphviz-dev pkg-config
sudo pip install pygraphviz
```

## Download Code
```
sudo apt install git
git clone https://github.com/alexanderskulikov/greedy-superstring-conjecture.git
```
   
## Setup Flask
sudo ln -sT ~/greedy-superstring-conjecture/web /var/www/html/web
sudo vim /etc/apache2/sites-enabled/000-default.conf
After the line `DocumentRoot /var/www/html`, add the following block:
```
WSGIDaemonProcess flaskapp threads=5
WSGIScriptAlias / /var/www/html/web/flaskapp.wsgi

<Directory flaskapp>
    WSGIProcessGroup flaskapp
    WSGIApplicationGroup %{GLOBAL}
    Order deny,allow
    Allow from all
</Directory>
```

Now run the command
```
sudo apachectl restart
```
   
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
	
	