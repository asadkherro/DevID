import subprocess
import re
import csv

def RunBashScript(script_path, *args):
    try:
        # command = ["bash", script_path] + list(args)
        command = ["sudo", "bash", script_path] + list(args)
        output = subprocess.check_output(command, stderr=subprocess.STDOUT)
        output = output.decode('utf-8').strip()
        return output
        
    except subprocess.CalledProcessError as e:
        print(f"Error: {e.output.decode('utf-8').strip()}")

import re

def ParseOutput(output):
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

def WriteToCSV(Ip , Mac , DeviceType , RunningDevice, OsCpe, OsDetails, OsGuesses):
    data = zip(Ip , Mac ,DeviceType , RunningDevice, OsCpe, OsDetails, OsGuesses)
    csvFile = "Result.csv"
    with open(csvFile, 'w', newline='') as file:
        writer = csv.writer(file)
        writer.writerow(["Ip", "Mac", "RunningDevice", "OsCpe", "OsDetails", "OsGuesses"])
        writer.writerows(data)


if __name__ == "__main__":
    ip_script_path = "GetIp.sh"
    nmap_script_path = "OsScan.sh"
    subnet = RunBashScript(ip_script_path)
    output = RunBashScript(nmap_script_path, subnet)
    Ip , Mac ,DeviceType , RunningDevice, OsCpe, OsDetails, OsGuesses = ParseOutput((output))
    WriteToCSV(Ip , Mac , DeviceType , RunningDevice, OsCpe, OsDetails, OsGuesses)