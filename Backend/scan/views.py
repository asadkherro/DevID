import subprocess
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status, permissions


from .utils import *

class SubnetScanView(APIView):
    permission_classes = [permissions.AllowAny]

    def get(self, request):
        # Command to run the Bash script with the 'eth0' argument
        command = ["bash", 'scan/InitialNetwork.sh', 'eth0']
        
        # Run the command and capture the output
        process = subprocess.Popen(command, stdout=subprocess.PIPE, stderr=subprocess.PIPE)

        # Read and print the output line by line
        while True:
            output = process.stdout.readline()
            if output == b'' and process.poll() is not None:
                break
            if output:
                print(output.strip().decode())
        
        # Decode the output from bytes to string
        stdout, stderr = process.communicate()
        output = stdout.decode()
        error = stderr.decode()

        # Check for any errors
        if error:
            print("Error occurred:", error)
            return Response({"error": error}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
        else:
            print(output)
            return Response({"output": output}, status=status.HTTP_200_OK)


class PythonScanView(APIView):
    permission_classes = [permissions.AllowAny]


    def get(self, request):
        try:
            script_path = "scan/scripts/InitialNetwork.sh"  
            arguments = ["eth0"]
            command = ["sudo", "bash", script_path] + arguments
            process = subprocess.Popen(command, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
            stdout, stderr = process.communicate()
            if stderr:
                error_message = stderr.decode().strip()
                return Response({'error': error_message}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
            output = stdout.decode().strip()
            ips, macs, names = parse_output_normal(output)
            output_objects = []
            for index , ip in enumerate(ips):
                output_objects.append({
                    "id" : index+1,
                    "ip" : ip,
                    "mac" : macs[index],
                    "name" : names[index]
                })
            writeToCSV_Normal(ips, macs, names)
            return Response({"output":  output_objects}, status=status.HTTP_200_OK)
        except Exception as e:
            return Response({'error': f"Error Occurred: {e}"}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

class OsScanView(APIView):
    permission_classes = [permissions.AllowAny]

    def get(self , request):
        try:
            print("===== GOT HIT ======")
            ip_script_path = "scan/scripts/get_Ip.sh"
            nmap_script_path = "scan/scripts/script3.sh"
            subnet = run_bash_script(ip_script_path)
            print("===== GET IP DONE =====")
            print(subnet)
            output = run_bash_script(nmap_script_path, subnet)
            print("===== OUTPUT DONE ======")
            print(output)
            Ip , Mac ,DeviceType , RunningDevice, OsCpe, OsDetails, OsGuesses = parse_output_os((output))
            output_objects = []
            for index , ip in enumerate(Ip):
                output_objects.append({
                    'id' : index+1,
                    'ip' : ip,
                    'mac':Mac[index],
                    'device_type' : DeviceType[index],
                    'running_device' : RunningDevice[index],
                    'oscpe' : OsCpe[index],
                    'os_details' : OsDetails[index],
                    "os_guess" : OsGuesses[index],
                })
            WriteToCSV_OS(Ip , Mac , DeviceType , RunningDevice, OsCpe, OsDetails, OsGuesses)
            return Response({'output':output_objects} , status=status.HTTP_200_OK)
        except Exception as e:
            return Response({'error' : f"Error Occured: {e}"} , status=status.HTTP_500_INTERNAL_SERVER_ERROR)