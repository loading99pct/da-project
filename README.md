# da-project

 

On the Manager machine:  
  1. init-manager.bash   
  This script is used to install python, distalgo, github and test code in the manager machine.   

  2. run-measurement.bash and measurement.py   
  This script is used to run the manager node to measure the total time. The script will call measurement.py. The measurement.py will execute codes in init-manager.py to launch slave machines before doing any measurement.

  3. myCode.da  
  This is the algorithm to be measured.
    
    
On the Slave Machines:
  1. run-node.bash   
  This script is called when the slave machine is launched.

  2. myCode.da   
  This is the algorithm to be measured.
