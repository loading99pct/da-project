#!/bin/bash
export PYTHONPATH="/home/ec2-user/da/distalgo":${PYTHONPATH}
chmod 777 /home/ec2-user/da-project/myCode.da
python3 -m da -f --message-buffer-size 4096000 -n $1 -D /home/ec2-user/da-project/myCode.da
