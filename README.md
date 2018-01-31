## Installation Guide

### Aliyun ECS (public)
+ hardware: at least 8 cores, 16 gb memo, 200 gb cloud ssd and 10 Mbps network bandwith
+ image: choose customized image 'prod-03_2017-11-15' to initialize
+ login www.xinnet.com, add A type record
+ apply SSL certificate and download SSL cert files
+ login as aqiuser / Moonp1ess
  + ~/env-setup/git-github/client.sh -a update
  + cd ~/git-projects/devops/
  + ./scripts/build.sh
  + update hostname of ECS and SSL cert files into devops
  + ./scripts/get-sqldump.sh production-02
  + ./scripts/ops.sh -a up -ph 'finix_01 finix_02 ...' -s true -h `hostname`
+ access https://FQDN


### Customer Environment (private)

#### Hardware
+ 8 Core, 16 GB memory, 200 GB Cloud SSD, at least 10Mbps Network bandwidth

#### Software
+ ubuntu: 16.04.3
+ kernel: >= 4.14
+ git: >= 2.7
+ docker: >= 17.09.0-ce (overlay2 storage)
+ docker-compose: >= 1.17.1
+ python3: >= 3.5.2 (pip3: 9.0.1)
  + 3rd modules: docker colorama
  + python3 bin available from /usr/local/bin

#### clone guidance project
+ git clone git@github.com:aqitrade/guidance.git && cd guidance

#### setup example
we use docker-compose to organize dockerized environment (skip mysql if not using container)
+ docker pull deepstream rabbitmq:3-management mysql
+ make .env file used by docker-compose
```
docker_ip="`ifconfig | grep docker0 -A 1 | grep inet | awk '{print $2}' | awk -F\: '{print $2}'`"
echo "COMPOSE_PROJECT_NAME=projectName" > .env
echo "DEVOPS_PATH=/somewhere/devops" >> .env
echo "ENV_USER=`id -u`:`id -g`" >> .env
echo "USER_NAME=`echo $USER`" >> .env
echo "USER_HOME=`echo $HOME`" >> .env
echo "DOCKER0_IP=${docker_ip}" >> .env
echo "HOST=`hostname`" >> .env
```
+ pull iFam related docker images
```
registry='registry.cn-beijing.aliyuncs.com/aqitrade'
images='algo mdserv panda phoenix raduga'
for image in $images; do
  image_name="${registry}/${image}"
  docker pull $image_name && \
  docker tag $image_name $image && \
  docker rmi $image_name
done
```
+ see docker-compose.yml for containers need to run
+ see conf file of separate component folder under config folder
+ orcinus.py
  + called from inside raduga container to control algo container
+ startup procedure:
  + docker-compose up -d rabbitmq deepstream
  + docker-compose up -d mysql
  + docker-compose up -d mdserv
  + docker-compose up -d phoenix_a phoenix_b ...
  + docker-compose up -d raduga
  + docker-compose up -d panda
+ try to access http://FQND or https://FQND
