# da-project

1. init-manager.bash   
This script is used to install python, distalgo, github and test code in the manager machine.

2. init-node.bash
This script is used to set up the machine where the proposers and acceptors are running. This script is set to be run automatically whenever the machine restart.

3. run-manager.bash
This script is used to run the manager node to measure the total time.

4. run-node.bash
This script is called by the init-node.bash to run the nodes in that machine on idle mode.
