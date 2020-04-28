#!/bin/bash
[ -d "./da-project" ] && rm -rf ./da-project 
git clone https://github.com/loading99pct/da-project.git  
export PYTHONPATH="/home/ec2-user/da/distalgo":${PYTHONPATH}
chmod 777 /home/ec2-user/da-project/run-node.da
sh ./da-project/run-node.bash "$@"
