import subprocess
import re
import csv

def run_bash_script(script_path, *args):
    try:
        command = ["sudo", "bash", script_path] + list(args)
        output = subprocess.check_output(command, stderr=subprocess.STDOUT)
        output = output.decode('utf-8').strip()
        return output
        
    except subprocess.CalledProcessError as e:
        print(f"Error: {e.output.decode('utf-8').strip()}")

def parse_output_normal(output):
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
    
def writeToCSV_Normal(ips, macs, names):
    data = zip(ips, macs, names)
    csvFile = "apps/scan/csv/NormalResults.csv"
    with open(csvFile, 'w', newline='') as file:
        writer = csv.writer(file)
        writer.writerow(["Ip", "Mac", "Device names"])
        writer.writerows(data)
    

def parse_output_os(output):
    Ip = []
    Mac = []
    DeviceType = []
    RunningDevice = []
    OsCpe = []
    OsDetails = []
    OsGuesses = []

    mainPattern = re.compile(r'Nmap scan report(?:.|\n)*?Network Distance')
    ipPattern = r'Nmap scan report for (\d+\.\d+\.\d+\.\d+)'
    macPattern = r'MAC Address: ([\w:]+) \((.*?)\)'
    deviceTypePattern = r"Device type:\s*(.*)"
    runningPattern = r"Running\s*(.*)"
    osCpepattern = r"OS CPE:\s*(.*)"
    osDetailsPattern = r"OS details:\s*(.*)"
    osGuessesPattern = r"Aggressive OS guesses:\s*(.*)"
    allMatches = mainPattern.findall(output)

    for match in allMatches:
        ipMatch = re.search(ipPattern, match)
        macMatch = re.search(macPattern, match)
        deviceTypeMatch = re.search(deviceTypePattern, match)
        runningMatch = re.search(runningPattern, match)
        osCpeMatch = re.search(osCpepattern, match)
        osDetailsMatch = re.search(osDetailsPattern, match)
        osGuessesMatch = re.search(osGuessesPattern, match)

        ipMatch = ipMatch.group(1) if ipMatch else 'Unmatched'
        macMatch = macMatch.group(1) if macMatch else 'Unmatched'
        deviceTypeMatch = deviceTypeMatch.group(1) if deviceTypeMatch else 'Unmatched'
        runningMatch = runningMatch.group(1) if runningMatch else 'Unmatched'
        osCpeMatch = osCpeMatch.group(1) if osCpeMatch else 'Unmatched'
        osDetailsMatch = osDetailsMatch.group(1) if osDetailsMatch else 'Unmatched'
        osGuessesMatch = osGuessesMatch.group(1) if osGuessesMatch else 'Unmatched'
        
        Ip.append(ipMatch)
        Mac.append(macMatch)
        DeviceType.append(deviceTypeMatch)
        RunningDevice.append(runningMatch)
        OsCpe.append(osCpeMatch)
        OsDetails.append(osDetailsMatch)
        OsGuesses.append(osGuessesMatch)
        
    return Ip , Mac, DeviceType , RunningDevice, OsCpe, OsDetails, OsGuesses

def WriteToCSV_OS(Ip , Mac , DeviceType , RunningDevice, OsCpe, OsDetails, OsGuesses):
    data = zip(Ip , Mac ,DeviceType , RunningDevice, OsCpe, OsDetails, OsGuesses)
    csvFile = "apps/scan/csv/OSResults.csv"
    with open(csvFile, 'w', newline='') as file:
        writer = csv.writer(file)
        writer.writerow(["Ip", "Mac", "RunningDevice", "OsCpe", "OsDetails", "OsGuesses"])
        writer.writerows(data)

    
