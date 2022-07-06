#!/usr/bin/env python

import pyVmomi
import argparse
import atexit
import itertools
import getpass
from pyVmomi import vim, vmodl
from pyVim.connect import SmartConnect, Disconnect, SmartConnectNoSSL
import humanize
from vmutils import vmutils

select = input("""1 for vm reboot 
2 for vm status """)

if select == "1":
    si = None

    serverinput = input("""1 for .6 
2 for .7 
3 for .33 
4 for .34 """)
        
    vminput = input("""1 for GNS3
2 for RHEL-9""")

    if serverinput == "1":
        server = "172.16.0.6"
    elif serverinput == "2":
        server = "172.16.0.7"
    elif serverinput == "3":
        server = "172.16.0.33"
    elif serverinput == "4":
        server = "172.16.0.34"
    else:
        print("entr the right number entry!")
        
    if vminput == "1":
        vmname = "GNS3"
    elif vminput == "2":
        vmname = "RHEL-9"
    else:
        print("enter the right number entry!")
        
    username = "root"
    password = getpass.getpass('Password:')
    
    try:
        si = SmartConnectNoSSL(host=server, user=username, pwd=password, port=443)
    except:
        print("error")
        pass

    # Finding source VM
    vm = vmutils.get_vm_by_name(si, vmname)

    # does the actual vm reboot
    try:
        vm.RebootGuest()
    except:
        # forceably shutoff/on
        # need to do if vmware guestadditions isn't running
        vm.ResetVM_Task()

    Disconnect(si)

else :
    
    MBFACTOR = float(1 << 20)
    host = input("ip address- ")
    username = input("username- ")
    pwd = getpass.getpass('Password:')
    port = int(443)

    printVM = True
    printDatastore = True
    printHost = True


    def dump(obj):
        for attr in dir(obj):
            print("obj.%s = %s" % (attr, getattr(obj, attr)))



    def printHostInformation(host):
        try:
            summary = host.summary
            stats = summary.quickStats
            hardware = host.hardware
            cpuUsage = stats.overallCpuUsage
            uptime = stats.uptime
            memoryCapacity = hardware.memorySize
            memoryCapacityInMB = hardware.memorySize/MBFACTOR
            memoryUsage = stats.overallMemoryUsage
            freeMemoryPercentage = 100 - (
                (float(memoryUsage) / memoryCapacityInMB) * 100
            )
            print("--------------------------------------------------")
            print("Host name: ", host.name)
            # dump(host)
            print("Host CPU usage: ", cpuUsage)
            print("Host Uptime: ", uptime)
            print("Host memory capacity: ", humanize.naturalsize(memoryCapacity,
                                                                 binary=True))
            print("Host memory usage: ", memoryUsage / 1024, "GiB")
            print("Free memory percentage: " + str(freeMemoryPercentage) + "%")
            print("--------------------------------------------------")
        except Exception as error:
            print("Unable to access information for host: ", host.name)
            print(error)
            pass


    def printComputeResourceInformation(computeResource):
        try:
            hostList = computeResource.host
            print("##################################################")
            print("Compute resource name: ", computeResource.name)
            print("##################################################")
            for host in hostList:
                printHostInformation(host)
        except Exception as error:
            print("Unable to access information for compute resource: ",
                  computeResource.name)
            print(error)
            pass


    def printDatastoreInformation(datastore):
        try:
            summary = datastore.summary
            capacity = summary.capacity
            freeSpace = summary.freeSpace
            uncommittedSpace = summary.uncommitted
            freeSpacePercentage = (float(freeSpace) / capacity) * 100
            print("##################################################")
            print("Datastore name: ", summary.name)
            print("Capacity: ", humanize.naturalsize(capacity, binary=True))
            if uncommittedSpace is not None:
                provisionedSpace = (capacity - freeSpace) + uncommittedSpace
                print("Provisioned space: ", humanize.naturalsize(provisionedSpace,
                                                                  binary=True))
            print("Free space: ", humanize.naturalsize(freeSpace, binary=True))
            print("Free space percentage: " + str(freeSpacePercentage) + "%")
            print("##################################################")
        except Exception as error:
            print("Unable to access summary for datastore: ", datastore.name)
            print(error)
            pass

    def printVmInformation(virtual_machine):
        summary = virtual_machine.summary
        stats = summary.quickStats
        print("Name       : ", summary.config.name)
        print("Template   : ", summary.config.template)
        print("Path       : ", summary.config.vmPathName)
        print("Guest      : ", summary.config.guestFullName)
        print("Memory Size : ", summary.config.memorySizeMB)
        print("Memory Usage : ", stats.hostMemoryUsage)
        print("CPU Usage : ", stats.overallCpuUsage)
        annotation = summary.config.annotation
        if annotation:
            print("Annotation : ", annotation)
        print("State      : ", summary.runtime.powerState)
        if summary.guest is not None:
            ip_address = summary.guest.ipAddress
            tools_version = summary.guest.toolsStatus
            if tools_version is not None:
                print("VMware-tools: ", tools_version)
            else:
                print("Vmware-tools: None")
            if ip_address:
                print("IP         : ", ip_address)
            else:
                print("IP         : None")
        if summary.runtime.question is not None:
            print("Question  : ", summary.runtime.question.text)
        print("")
        pass

    def main():
        # try:
        si = SmartConnectNoSSL(host=host,
                                   user=username,
                                   pwd=pwd,
                                   port=int(port))

        atexit.register(Disconnect, si)

        content = si.RetrieveContent()

        for datacenter in content.rootFolder.childEntity:
            print("##################################################")
            print("##################################################")
            print("### datacenter : " + datacenter.name)
            print("##################################################")

            if printVM:
                if hasattr(datacenter.vmFolder, 'childEntity'):
                    vmFolder = datacenter.vmFolder
                    vmList = vmFolder.childEntity
                    for vm in vmList:
                        printVmInformation(vm)

            if printDatastore:
                datastores = datacenter.datastore
                for ds in datastores:
                    printDatastoreInformation(ds)

            if printHost:
                if hasattr(datacenter.hostFolder, 'childEntity'):
                    hostFolder = datacenter.hostFolder
                    computeResourceList = hostFolder.childEntity
                    for computeResource in computeResourceList:
                        printComputeResourceInformation(computeResource)

        # except Exception as error:
        #     print("Caught vmodl fault : " + error.msg)
        #     return -1
        return 0

    if __name__ == "__main__":
        main()

k=input("press any key to exit")
