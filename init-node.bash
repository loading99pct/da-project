#!/bin/bash
cd ~
[ -d "./da-project" ] && rm -rf ./da-project
git clone https://github.com/loading99pct/da-project.git
chmod 777 ./da-project/run-node.bash
sh ./da-project/run-node.bash "$@"
