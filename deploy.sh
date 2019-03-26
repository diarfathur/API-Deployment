#!/bin/bash

eval "$(ssh-agent -s)" &&
ssh-add -k ~/.ssh/id_rsa &&
cd /home/ubuntu/API-Deployment
git pull

source ~/.profile
echo "$DOCKERHUB_PASS" | sudo docker login --username $DOCKERHUB_USER --password-stdin
sudo docker stop ecommerceApi
sudo docker rm ecommerceApi
sudo docker rmi diarfathur/ecommerce
sudo docker run -d --name ecommerceApi -p 5000:5000 diarfathur/ecommerce:latest
