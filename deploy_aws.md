# Deployment
Here we explain how to deploy the webpage on an amazon AWS server.

## Launch Instance

Go to [https://console.aws.amazon.com/ec2/](https://console.aws.amazon.com/ec2/), click **Launch Instance**, choose **Ubuntu Server 16.04 LTS (HVM)**, then **t2.micro**. Now **Edit Security Groups**, add *SSH* and *HTTP* with Source *Anywhere*. Download the provided private key. The name of our private key file is *firstkeypair.pem*. We need to change its permission:
```
chmod 400 firstkeypair.pem
```

## SSH to the server
Our Public DNS is *ec2-52-15-239-252.us-east-2.compute.amazonaws.com*. Thus, we can ssh to this machine using the command
```
ssh -i "firstkeypair.pem" ubuntu@ec2-52-15-239-252.us-east-2.compute.amazonaws.com
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
sudo pip3 install pygraphviz --install-option="--include-path=/usr/include/graphviz" --install-option="--library-path=/usr/lib/graphviz/"
```

## Download Code
```
sudo apt install git
git clone https://github.com/alexanderskulikov/greedy-superstring-conjecture.git
```
   
## Setup Flask
```
sudo ln -sT ~/greedy-superstring-conjecture/web /var/www/html/web
sudo vim /etc/apache2/sites-enabled/000-default.conf
```
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

## Write Permissions
```
sudo chmod -R a+w greedy-superstring-conjecture/web/static/logs/
sudo chmod -R a+w greedy-superstring-conjecture/web/static/output/
```

## Testing

Open in your browser the page `http://ec2-52-15-239-252.us-east-2.compute.amazonaws.com/scs`

You can find Apache's logs here:
```
/var/log/apache2/error.log
```

In order to restart Apache, run:
```
sudo apachectl restart
```

## Logs, History and Exceptions

```
ssh -i "firstkeypair.pem" ubuntu@ec2-52-15-239-252.us-east-2.compute.amazonaws.com
```

Here are the outputs: `greedy-superstring-conjecture/web/static/output/`

Here is the history: `greedy-superstring-conjecture/web/static/logs/history/`

Here is the list of exceptions: `greedy-superstring-conjecture/web/static/logs/exceptions.txt`

Here is the list of counter-examples: `greedy-superstring-conjecture/web/static/logs/counter-examples.txt`