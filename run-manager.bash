#!/bin/bash
cd ~
[ -d "./da-project" ] && rm -rf ./da-project 
git clone https://github.com/loading99pct/da-project.git  
chmod 777 ./da-project/run-manager.bash
PYTHONPATH="/home/ec2-user/da/distalgo":${PYTHONPATH}
cd ~/da-project
python3 -m da -f -n ManagerNode -i ./myCode.da "$@"
