import os
import time
import subprocess

DEBUG_MODE = False


# ------------------------------- Config -------------------------------
config = {
    "init": {
        "intitializeSlaveMachines": True, 
        "slaveMachineN":1
    },

    # a list of measurement parameters
    "measurement": {
        "enable": True,
        "dataPoints": [
            # # for example: 
            # {
            #   "enable": True, 
            #     "cmdParameters": f"10 100 1 600 600", 
            #     "repeatN":3
            # },

            # {
            #   "enable": True, 
            #     "cmdParameters": f"10 200 1 600 600", 
            #     "repeatN":3
            # },

        ]
    }


}


# add more data points that need to be measured
DEFAULT_PROPOSER_NUM = 10
DEFAULT_MEASUREMENT_TIMEOUT = 600
REPEAT_NTIMES_PER_DATAPOINT = 1

for nProposer in [30, 60]:
    dataPoint = {
                    "enable": True, 
                    "cmdParameters": f"{DEFAULT_PROPOSER_NUM} {nProposer} 1 1200 {DEFAULT_MEASUREMENT_TIMEOUT}", 
                    "repeatN": REPEAT_NTIMES_PER_DATAPOINT
                }
    config["measurement"]["dataPoints"].append(dataPoint)


# ------------------------------- Measure -------------------------------

def execCmd(cmd: str):
    print(f"----------------- Executing Command line: {cmd}")
    if DEBUG_MODE:
        return
    proc = subprocess.Popen(cmd, shell=True, stdout=subprocess.PIPE)
    proc.wait()
    print(proc.returncode)


if __name__ == "__main__":
    # spin up all the slave machines
    if config["init"]["intitializeSlaveMachines"]:
        print("Initializing slave machines")
        slaveMachineN = config["init"]["slaveMachineN"]
        execCmd(f"python3 /home/ec2-user/da-project/init-all-instance.py {slaveMachineN}")
        waitingTime = 120
        print(f"Waiting {waitingTime} seconds for the slave machines initialization")
        time.sleep(waitingTime)


    # do the measurement one by one
    if config["measurement"]["enable"]:
        for dataPoint in config["measurement"]["dataPoints"]:
            if dataPoint["enable"]:
                # repeat the measurement N times
                for repeatI in range(dataPoint["repeatN"]):
                    cmdParameters = dataPoint["cmdParameters"]
                    execCmd(f"python3 -m da -f -n ManagerNode --message-buffer-size 4096000 -i /home/ec2-user/da-project/myCode.da {cmdParameters}")
