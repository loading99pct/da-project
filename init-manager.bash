#!/bin/bash
sudo yum install python3 -y
sudo yum install git -y
mkdir da
cd da        
git clone https://github.com/DistAlgo/distalgo.git 
export PYTHONPATH="/home/ec2-user/da/distalgo":${PYTHONPATH} 
cd ~
[ -d "./da-project" ] && rm -rf ./da-project 
git clone https://github.com/loading99pct/da-project.git  
mkdir ~/inst-bash
mkdir ~/.aws
