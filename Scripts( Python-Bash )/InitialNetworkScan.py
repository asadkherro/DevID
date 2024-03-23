import subprocess
import re
import csv

def run_bash_script(script_path, *args):
    try:
        # Build the command to run the Bash script with arguments
        # For normal command = ["bash", script_path] + list(args)
        command = ["sudo", "bash", script_path] + list(args)

        # Run the command and capture the output
        output = subprocess.check_output(command, stderr=subprocess.STDOUT)
        
        # Decode the output from bytes to string
        output = output.decode('utf-8').strip()
        
        # Print the output
        return output
        
    except subprocess.CalledProcessError as e:
        # If the subprocess returns a non-zero exit status, handle the error
        print(f"Error: {e.output.decode('utf-8').strip()}")

def parse_output(output):
    ip_pattern = r'Nmap scan report for (\d+\.\d+\.\d+\.\d+)'
    mac_pattern = r'MAC Address: ([\w:]+) \((.*?)\)'

    # Compile regular expression patterns
    ip_regex = re.compile(ip_pattern)
    mac_regex = re.compile(mac_pattern)

    # Find all matches in the output
    ips = ip_regex.findall(output)
    matches = mac_regex.findall(output)

    # Extract MAC addresses and device names separately
    macs = [match[0] for match in matches]
    names = [match[1] for match in matches]

    return ips, macs, names
    # for i in range(len(ips)):
        # print("Ip Address : ", ips[i], "\nMac Address : ", macs[i], "\nDevice :", names[i], "\n\n")
    
def writeToCSV(ips, macs, names):
    data = zip(ips, macs, names)
    csvFile = "Result.csv"
    with open(csvFile, 'w', newline='') as file:
        writer = csv.writer(file)
        writer.writerow(["Ip", "Mac", "Device names"])
        writer.writerows(data)

if __name__ == "__main__":
    script_path = "InitialNetwork.sh"
    arguments = ["eth0"]
    ips, macs, names = parse_output(run_bash_script(script_path, *arguments))
    writeToCSV(ips, macs, names)


    
