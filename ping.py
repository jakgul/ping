import os
import subprocess
import platform
import ipaddress

class Smartping():

    def __init__(self,ips=[],ping_count=2, subnet=""):
        self.ips=ips
        self.ping_count = ping_count
        self.subnet = subnet
        self.platform = platform.system().lower()
        self.ping_result = ""
        self.flattened_ips=[]  #IPs will be added here

    def flatten_ips(self):
        for ip in self.ips:
            if "/" in ip:  #convert network address to IPs
                self.load_ips_from_subnet(ip)
            else:
                self.flattened_ips.append(ip)

    def ping(self):
        self.flatten_ips()
        if self.platform == "windows":
            self.windows_ping()
        else:
            self.linux_ping()

    def linux_ping(self):
        for ip in self.flattened_ips:
            command = "ping -c {} {}".format(str(self.ping_count), ip)  #EX: ping -c 1 10.10.10.1  (send 1 ping)
            response = os.system(command)
            if response == 0:
                self.ping_result += ip + " is up!\n"
            else:
                self.ping_result += ip + " is down!\n"
        print(self.ping_result)

    def windows_ping(self):
        for ip in self.flattened_ips:
            command = "ping -n {} {}".format(str(self.ping_count), ip)   #EX: ping -n 1 10.10.10.1  (send 1 ping)
            response = subprocess.run(command, capture_output=True)
            output = response.stdout.decode()
            print(output)
            if "Destination host unreachable" in output:
                self.ping_result += ip + " is down! Destination host unreachable. \n"
            elif "Request timed out" in output:
                self.ping_result += ip + " is down! Request timed out.\n"
            else:
                self.ping_result += ip + " is up!\n"
        print(self.ping_result)

    def load_ips(self,filename):
        with open(filename) as file:  #load IPs from a spesific file
            ip_text_file = file.read()
            self.ips = ip_text_file.split("\n")


    def load_ips_from_subnet(self,subnet):
        for addr in ipaddress.ip_network(subnet):  #find all the IPs in network, add it to list
            self.flattened_ips.append(str(addr))

    def save_output(self,filename="pingresult.txt"):  #write the ping result to a file
        file = open(filename, "w")
        file.write(self.ping_result)
        file.close()


############################################
#Run the script by editing below
############################################

#Step 1, call the class object and create a smartping object
a = Smartping()

#Step 2, load IPs.
a.load_ips("ips.txt")    #load IPs from file
#a.ips = ["10.70.69.0/30","10.70.70.2","10.70.70.3"] #load IPs as a list

# Step 3 Specify the ping count(default is 2)
a.ping_count = 1
#Step 4, call the ping function
a.ping()

#Step 5, save the ping results to a file. Default file name is pingresult.txt or specify the name
a.save_output("writehere.txt")


