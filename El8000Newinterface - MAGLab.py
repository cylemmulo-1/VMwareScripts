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
import customtkinter
import tkinter as tk
from tkinter import ttk
import tkinter.scrolledtext as tkscrolled


customtkinter.set_appearance_mode("Dark")  # Modes: "System" (standard), "Light","Dark" 
customtkinter.set_default_color_theme("green")  # Themes: "blue" (standard), "green", "dark-blue"
root = customtkinter.CTk()
root.iconbitmap(r'mag.ico')
style = ttk.Style()
root.configure(background='gray')





root.geometry("1300x1000")
root.title("MAGAERO EL8000")
## Not sure why but I need this in here even though it is definied below. If I just use this output it gets weird too

#####

#use these to stop or start print functions for the Vsphere lookup
MBFACTOR = float(1 << 20)
#Main geometry for the window
printVM = True
printDatastore = True
printHost = True

username = "root"
pwd = "1qazXSW@"

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
    host = "10.1.110.196"
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
def Take_inputvm195():
    host = "10.1.110.195"
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
capture195 = io.StringIO()
#save,sys.stdout = sys.stdout,capture33
#Take_inputvm33()
#sys.stdout = save
############
def Take_inputvm196():
    host = "10.1.110.196"
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
capture196 = io.StringIO()
#save,sys.stdout = sys.stdout,capture7
#Take_inputvm7()
#sys.stdout = save

####################
def Take_inputvm197():
    host = "10.1.110.197"
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


capture197 = io.StringIO()
#save,sys.stdout = sys.stdout,capture6
#Take_inputvm6()
#sys.stdout = save
####################



def Take_inputvm198():
    host = "10.1.110.198"
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


capture198 = io.StringIO()
#save,sys.stdout = sys.stdout,capture34
#Take_inputvm34()
#sys.stdout = save


####################

def Take_input195():
    with redirect_stdout(capture195):
        Take_inputvm195()
    Output.insert(END, capture195.getvalue())
    Output.see("end")
    capture195.seek(0)


def Take_input196():
    with redirect_stdout(capture196):
        Take_inputvm196()
    Output.insert(END, capture196.getvalue())
    Output.see("end")
    capture196.seek(0)
      
def Take_input197():
    with redirect_stdout(capture197):
        Take_inputvm197()
    Output.insert(END, capture197.getvalue())
    Output.see("end")
    capture197.seek(0)

def Take_input198():
    with redirect_stdout(capture198):
        Take_inputvm198()
    Output.insert(END, capture198.getvalue())
    Output.see("end")
    capture198.seek(0)

#Box popups to confirm rebooting VM

def confirmkraken():
    answer = askyesno(title='confirmation',
                    message='Are you sure that you want to reset GNS3?')
    if answer:
        resetvm("Kraken")
        
def confirmlibrenms():
    answer = askyesno(title='confirmation',
                    message='Are you sure that you want to reset RHEL 9?')
    if answer:
        resetvm(librenms)

#ws = Tk()
#frame=Frame(ws)
#frame.geometry("1200x1000")

#l = Label(text = "Choose an option")
#inputtxt = Text(root, height = 10,
             #   width = 25,
            #    bg = "light yellow")

photo = PhotoImage(file = "airplanesml.png")
photoimage = photo.subsample(1, 1)

photo2 = PhotoImage(file = "el8000sml.png")
photoimage2 = photo2.subsample(1,1)

#text entry frame

frame_left = customtkinter.CTkFrame(master=root,width=180,corner_radius=10)
frame_left.grid(row=0, column=0,rowspan=1, sticky="nswe")

frame_right = customtkinter.CTkFrame(root)
frame_right.grid(row=0, column=1, sticky="nswe", rowspan=2)

frame_info = customtkinter.CTkFrame(master=frame_right)
frame_info.grid(row=0, column=1, columnspan=2, rowspan=2, pady=2, padx=2, sticky="nsew")


Output = tkscrolled.ScrolledText(master=frame_info, height=50, width=105, wrap=WORD, bg="black", fg="white")

 
Display = customtkinter.CTkButton(master=frame_left,
                 text ="Blade-1 .195",
                 text_font=("Roboto Medium", -22),
                 command = lambda:Take_input195())
Display2 = customtkinter.CTkButton(master=frame_left,
                 text ="Blade-3 .196",
                 text_font=("Roboto Medium", -22),
                 command = lambda:Take_input196())
Display3 = customtkinter.CTkButton(master=frame_left,
                 text ="Blade-5 .197",
                 text_font=("Roboto Medium", -22),
                 command = lambda:Take_input197())
Display4 = customtkinter.CTkButton(master=frame_left,
                 text ="Blade-7 .198",
                 text_font=("Roboto Medium", -22),
                 command = lambda:Take_input198())
Display5 = customtkinter.CTkButton(master=frame_left,
                 text_font=("Roboto Medium", -22),
                 text ="Reset Kraken",
                 command = lambda:confirmkraken())
Display6 = customtkinter.CTkButton(master=frame_left,
                 text_font=("Roboto Medium", -22),
                 text ="Reset librenms",
                 command = lambda:confirmlibrenms())
photobutton = customtkinter.CTkButton(master=frame_left, image = photoimage,
                 text ="",
                 command = root.destroy)

#############################
###Darkmode Switch
#def change_mode():
    #if switch_2.get() == 1:
        #customtkinter.set_appearance_mode("light")
   # else:
        #customtkinter.set_appearance_mode("dark")
#switch_2 = customtkinter.CTkSwitch(master=root,
                                        #text="Dark Mode",
                                       # command=change_mode)
#switch_2.grid(row=4, column=7, pady=10, padx=20, sticky="w")
##################################

#El8000s Image insert

el8000label = customtkinter.CTkLabel(
    root, background='white',
    text= "",image = photoimage2,
    justify = 'right')


#l.pack()
#inputtxt.pack()

el8000label.grid(row=1, column =0, columnspan=1,rowspan=1)
photobutton.grid(row=5, column=2,pady=10, padx=60, sticky="we")
Display.grid(row =1, column=2,pady=10, padx=60, sticky="we")
Display2.grid(row =2, column=2,pady=10, padx=60, sticky="we")
Display3.grid(row=3,column=2,pady=10, padx=60, sticky="we")
Display4.grid(row=4,column=2,pady=10, padx=60, sticky="we")
Display5.grid(row=6,column=2,pady=10, padx=60, sticky="we")
Display6.grid(row=7,column=2,pady=10, padx=60, sticky="we")
Output.grid(row=0,column=3, columnspan=5, rowspan=2)




root.mainloop()
