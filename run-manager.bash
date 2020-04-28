#!/bin/bash
cd ~
[ -d "./da-project" ] && rm -rf ./da-project 
git clone https://github.com/loading99pct/da-project.git  
chmod 777 ./da-project/run-manager.bash
export PYTHONPATH="/home/ec2-user/da/distalgo":${PYTHONPATH}
cd ~/da-project
python3 -m da -f -n ManagerNode --message-buffer-size 4096000 -i ./myCode.da "$@"
