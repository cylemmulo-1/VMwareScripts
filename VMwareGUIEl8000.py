import tkinter
from tkinter import *
from tkinter.ttk import *
import tkinter.messagebox
from tkinter.messagebox import askyesno
import atexit
import getpass
from pyVmomi import vim, vmodl
from pyVim.connect import SmartConnect, Disconnect, SmartConnectNoSSL
import humanize
from vmutils import vmutils
import io
from contextlib import redirect_stdout

MBFACTOR = float(1 << 20)
#Main geometry for the window
root = Tk()
root.geometry("1200x1000")
root.configure(background='White')
root.title("MAGAERO EL8000 ")
root.iconbitmap(r'mag.ico')
## Not sure why but I need this in here even though it is definied below. If I just use this output it gets weird too
Output = Text(root, height = 40,
              width = 45,
              bg = "red")
#####

#use these to stop or start print functions for the Vsphere lookup

printVM = True
printDatastore = True
printHost = True

username = "pythonadmin"
pwd = "r@TsVXN808MT"

#Moved the functions for defining what to lookup in vmware to the top so it can be used by all vsphere lookups

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

###########################################################################
#####RESET VM FUNCTION
def resetvm(namevm):
    host = "172.16.0.33"
    vmname = namevm


    try:
        si = SmartConnectNoSSL(host=host, user=username, pwd=pwd, port=443)
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
    tkinter.messagebox.showinfo("MAG Aerospace",  "Action Completed")
    Disconnect(si)


#################################################
#GET VMWARE INFORMATION FUNCTIONS. These use the definitions up top
def Take_inputvm33():
    host = "172.16.0.33"
    port = int(443)

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

############# 
##this captures the output of Take_inputvm() function and saves it to call later
capture33 = io.StringIO()
#save,sys.stdout = sys.stdout,capture33
#Take_inputvm33()
#sys.stdout = save
############
def Take_inputvm7():
    host = "172.16.0.7"
    port = int(443)

 
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

#############

#this captures the output of Take_inputvm2() function and saves it to call later
capture7 = io.StringIO()
#save,sys.stdout = sys.stdout,capture7
#Take_inputvm7()
#sys.stdout = save

####################
def Take_inputvm6():
    host = "172.16.0.6"
    port = int(443)


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


capture6 = io.StringIO()
#save,sys.stdout = sys.stdout,capture6
#Take_inputvm6()
#sys.stdout = save
####################



def Take_inputvm34():
    host = "172.16.0.34"
    port = int(443)

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


capture34 = io.StringIO()
#save,sys.stdout = sys.stdout,capture34
#Take_inputvm34()
#sys.stdout = save


####################

def Take_input6():
    with redirect_stdout(capture6):
        Take_inputvm6()
    Output.insert(END, capture6.getvalue())
    Output.see("end")
    capture6.seek(0)

def Take_input7():
    with redirect_stdout(capture7):
        Take_inputvm7()
    Output.insert(END, capture7.getvalue())
    Output.see("end")
    capture7.seek(0)
        
def Take_input33():
    with redirect_stdout(capture33):
        Take_inputvm33()
    Output.insert(END, capture33.getvalue())
    Output.see("end")
    capture33.seek(0)

def Take_input34():
    with redirect_stdout(capture34):
        Take_inputvm34()
    Output.insert(END, capture34.getvalue())
    Output.see("end")
    capture34.seek(0)

#Box popups to confirm rebooting VM

def confirmgns3():
    answer = askyesno(title='confirmation',
                    message='Are you sure that you want to reset GNS3?')
    if answer:
        resetvm("GNS3")
        
def confirmgrhel9():
    answer = askyesno(title='confirmation',
                    message='Are you sure that you want to reset RHEL 9?')
    if answer:
        resetvm("RHEL-9")

style = Style()
 
style.configure('TButton', font =
               ('calibri', 20, 'bold'),
                    borderwidth = '42')
 

style.map('TButton', foreground = [('active', '!disabled', 'green')],
                     background = [('active', 'black')])
#ws = Tk()
#frame=Frame(ws)
#frame.geometry("1200x1000")

l = Label(text = "Choose an option")
#inputtxt = Text(root, height = 10,
             #   width = 25,
            #    bg = "light yellow")

photo = PhotoImage(file = "airplanesml.png")
photoimage = photo.subsample(1, 1)

photo2 = PhotoImage(file = "el8000.png")
photoimage2 = photo2.subsample(1,1)

Output = Text(root, height = 45,
              width = 85,
              bg = "light green")
 
Display = Button(root,
                 text ="172.16.0.6 Vmware",
                 command = lambda:Take_input6())
Display2 = Button(root,
                 text ="172.16.0.7 VMware",
                 command = lambda:Take_input7())
Display3 = Button(root,
                 text ="172.16.0.33 VMware",
                 command = lambda:Take_input33())
Display4 = Button(root,
                 text ="172.16.0.34 VMware",
                 command = lambda:Take_input34())
photobutton = Button(root, image = photoimage,
                 text ="Airplane",
                 command = root.destroy)
Display5 = Button(root,
                 text ="Reset GNS3",
                 command = lambda:confirmgns3())
Display6 = Button(root,
                 text ="Reset Rhel9",
                 command = lambda:confirmgrhel9())

#El8000s label that sits to th eleft
el8000label = Label(
    root, background='white', font=("Courier", 14),
    text= "",image = photoimage2,
    justify = 'right')


#l.pack()
#inputtxt.pack()

el8000label.grid(row=3, column =6, columnspan=1, sticky="ns")
Display.grid(row =0, column=2 )
Display2.grid(row =0, column=3)
Display3.grid(row=1,column=2)
Display4.grid(row=1,column=3)
photobutton.grid(row=4, column=6, columnspan=1)
Display5.grid(row=2,column=2, sticky="nsew")
Display6.grid(row=2,column=3, sticky="nsew")
Output.grid(row=3,column=1, columnspan=5, rowspan=2)




mainloop()
