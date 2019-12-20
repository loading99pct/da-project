import sys
import subprocess
import json


def writeAwsRunInstFile(nodeName: str, fileName: str):
	with open(fileName, "w") as f:
		bashOnRun = "\n".join(["#!/bin/bash",
			"git clone https://github.com/loading99pct/da-project.git",
			"chmod 777 ./da-project/run-node.bash", 
			"sh ./da-project/run-node.bash {}".format(nodeName)])
		f.write(bashOnRun)

def parseNewInstFeedbackToIp(outputMsg: str):
    jsonObj = json.loads(outputMsg)
    networkPart = jsonObj["Instances"][0]
    ipAddr = networkPart["NetworkInterfaces"][0]["PrivateIpAddresses"][0]["PrivateIpAddress"]
    return ipAddr


if __name__ == "__main__":
	instanceToInitN = int(sys.argv[1]) if len(sys.argv) > 1 else 1
	beginIndex = int(sys.argv[2]) if len(sys.argv) > 2 else 1
	appendQ = sys.argv[3] if len(sys.argv) > 3 else "n"
	appendQ = appendQ == "y"

	daAddrL = []
	for i in range(beginIndex, beginIndex + instanceToInitN):
		bashFileName = f"./inst-bash/NodeBash-{i}.bash"
		nodeName = f"Node-{i}"
		writeAwsRunInstFile(nodeName, bashFileName)

		# bashCommand = f"chmod 777 {bashFileName}"
		# process = subprocess.Popen(bashCommand.split(), stdout=subprocess.PIPE)
		# output, error = process.communicate()

		bashCommand = " ".join([
			"aws ec2 run-instances", 
			"--image-id ami-034d4e9d666df39fc",
			"--count 1",
			"--instance-type t2.micro",
			"--key-name testKey",
			"--subnet-id subnet-dbe62bd5",
			"--security-group-ids sg-0179f1922c04fe31d",
			"--region us-east-1",
			# "--tag-specifications 'ResourceType=instance,Tags=[{Key=Name,Value=" + nodeName + "},{Key=type,Value=BatchGen}]'", 
			# "--tag-specifications 'ResourceType=instance,Tags=[{Key=Name,Value=" + nodeName + "}]'", 
			f"--user-data file://{bashFileName}"])
		# print(bashCommand)
		process = subprocess.Popen(bashCommand.split(), stdout=subprocess.PIPE)
		outputMsg, errorMsg = process.communicate()		
		# assert errorMsg == None
		if errorMsg is not None:
			print(errorMsg)

		ipAddr = parseNewInstFeedbackToIp(outputMsg)
		daAddr = f"{nodeName}@{ipAddr}"
		print(daAddr)
		daAddrL.append(daAddr)

		if not appendQ:
			with open("./newDaAddr.config", "w") as f:
				f.writelines(daAddrL + "\n")
		else:
			with open("./newDaAddr.config", "a") as f:
				f.writeline(daAddr + "\n")
		
		# print("output: \n")
		# print(outputMsg)
		# print("error message: \n")
		# print(errorMsg)
