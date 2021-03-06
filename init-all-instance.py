import sys
import subprocess
import json

DEBUG_MODE = False


def writeAwsRunInstFile(nodeName: str, fileName: str):
	with open(fileName, "w") as f:
		headPart = """Content-Type: multipart/mixed; boundary="//"
MIME-Version: 1.0

--//
Content-Type: text/cloud-config; charset="us-ascii"
MIME-Version: 1.0
Content-Transfer-Encoding: 7bit
Content-Disposition: attachment; filename="cloud-config.txt"

#cloud-config
cloud_final_modules:
- [scripts-user, always]

--//
Content-Type: text/x-shellscript; charset="us-ascii"
MIME-Version: 1.0
Content-Transfer-Encoding: 7bit
Content-Disposition: attachment; filename="userdata.txt"
\n"""
		if DEBUG_MODE:
			bashOnRun = "\n".join(["#!/bin/bash",
				"""echo "running" | tee logfile.txt"""])
		else:
# 			bashOnRun = "\n".join(["#!/bin/bash",
# 				"git clone https://github.com/loading99pct/da-project.git",
# 				"chmod 777 /home/ec2-user/da-project/run-node.bash", 
# 				"sh /home/ec2-user/da-project/run-node.bash {}".format(nodeName)])
			bashOnRun = "\n".join(["#!/bin/bash",
				"sudo yum -y install python3", 
				"sudo yum -y install git", 
				"cd /home/ec2-user", 
				"mkdir da", 
				"cd da",
				"git clone https://github.com/DistAlgo/distalgo.git ", 
				"cd /home/ec2-user", 
				"git clone https://github.com/loading99pct/da-project.git",
				"chmod 777 /home/ec2-user/da-project/run-node.bash", 
				"sh /home/ec2-user/da-project/run-node.bash {}".format(nodeName)])
	
		f.write(headPart + bashOnRun)

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
	
	AWS_IMAGE_ID = "ami-0892815748fd033a2" if DEBUG_MODE else "ami-0323c3dd2da7fb37d"
	# AWS_IMAGE_ID = "ami-0892815748fd033a2"
	
	daAddrL = []
	for i in range(beginIndex, beginIndex + instanceToInitN):
		bashFileName = f"/home/ec2-user/inst-bash/NodeBash-{i}.bash"
		nodeName = f"Node-{i}"
		writeAwsRunInstFile(nodeName, bashFileName)

		# bashCommand = f"chmod 777 {bashFileName}"
		# process = subprocess.Popen(bashCommand.split(), stdout=subprocess.PIPE)
		# output, error = process.communicate()

		bashCommand = " ".join([
			"aws ec2 run-instances", 
			f"--image-id {AWS_IMAGE_ID}",
			"--count 1",
			"--instance-type t2.2xlarge",
			"--key-name testKey",
			"--subnet-id subnet-650cb66b",
			"--security-group-ids sg-0fa58bcb1ed782b66",
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
			with open("/home/ec2-user/newDaAddr.config", "w") as f:
				f.writelines("\n".join(daAddrL) + "\n")
		else:
			with open("/home/ec2-user/newDaAddr.config", "a") as f:
				f.write(daAddr + "\n")
		
		# print("output: \n")
		# print(outputMsg)
		# print("error message: \n")
		# print(errorMsg)
