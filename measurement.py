import os

DEBUG_MODE = True

config = {
    "init": {
        "intitializeSlaveMachines": False, 
        "slaveMachineN":5
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
REPEAT_NTIMES_PER_DATAPOINT = 3

for nProposer in [30, 50, 100]:
    dataPoint = {
                    "enable": True, 
                    "cmdParameters": f"{DEFAULT_PROPOSER_NUM} {nProposer} 1 1200 {DEFAULT_MEASUREMENT_TIMEOUT}", 
                    "repeatN": REPEAT_NTIMES_PER_DATAPOINT
                }
    config["measurement"]["dataPoints"].append(dataPoint)




def execCmd(cmd: str):
    print(f"Executing Command line: {cmd}")
    if DEBUG_MODE:
        return
    os.system(cmd)


if __name__ == "__main__":
    # spin up all the slave machines
    if config["init"]["intitializeSlaveMachines"]:
        print("Initializing slave machines")
        slaveMachineN = config["init"]["slaveMachineN"]
        execCmd(f"python3 ./da-project/init-all-instance.py {slaveMachineN}")


    # do the measurement one by one
    if config["measurement"]["enable"]:
        for dataPoint in config["measurement"]["dataPoints"]:
            if dataPoint["enable"]:
                # repeat the measurement N times
                for repeatI in range(dataPoint["repeatN"]):
                    cmdParameters = dataPoint["cmdParameters"]
                    execCmd(f"./da-project/run-manager.bash {cmdParameters}")
