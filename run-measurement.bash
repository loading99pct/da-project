#!/bin/bash
cd ~
[ -d "./da-project" ] && rm -rf ./da-project
git clone https://github.com/loading99pct/da-project.git
export PYTHONPATH="/home/ec2-user/da/distalgo":${PYTHONPATH}
chmod 777 ./da-project/run-measurement.bash
# cd ./da-project
python3 /home/ec2-user/da-project/measurement.py
