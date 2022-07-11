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

focusBorderImageData = '''
    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
    Ry/99NIz//oGrZpUUEAAOw==
'''

borderImageData = '''
    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
'''

customtkinter.set_appearance_mode("Light")  # Modes: "System" (standard), "Light","Dark" 
customtkinter.set_default_color_theme("green")  # Themes: "blue" (standard), "green", "dark-blue"
root = customtkinter.CTk()
style = ttk.Style()
root.configure(background='White')


borderImage = tk.PhotoImage("borderImage", data=borderImageData)
focusBorderImage = tk.PhotoImage("focusBorderImage", data=focusBorderImageData)

style.element_create("RoundedFrame",
                     "image", borderImage,
                     ("focus", focusBorderImage),
                     border=16, sticky="nsew")
style.layout("RoundedFrame",
             [("RoundedFrame", {"sticky": "nsew"})])


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


#ws = Tk()
#frame=Frame(ws)
#frame.geometry("1200x1000")

#l = Label(text = "Choose an option")
#inputtxt = Text(root, height = 10,
             #   width = 25,
            #    bg = "light yellow")

photo = PhotoImage(file = "airplanesml.png")
photoimage = photo.subsample(1, 1)

photo2 = PhotoImage(file = "el8000.png")
photoimage2 = photo2.subsample(1,1)

#text entry frame
frame_top = Frame(master=root,
                                                 width=180,
                                                  style="RoundedFrame")
frame_top.grid(row=0, column=0,rowspan=4, sticky="nswe", ipadx=6, ipady=6)

text_frame = Frame(root, style="RoundedFrame", padding=10)

Output = Text(text_frame, height=50, width=100, wrap=WORD, bg="black", fg="white")

 
Display = customtkinter.CTkButton(master=frame_top,
                 text ="172.16.0.6 Vmware",
                 text_font=("Roboto Medium", -26),
                 command = lambda:Take_input6())
Display2 = customtkinter.CTkButton(master=frame_top,
                 text ="172.16.0.7 VMware",
                 text_font=("Roboto Medium", -26),
                 command = lambda:Take_input7())
Display3 = customtkinter.CTkButton(master=frame_top,
                 text ="172.16.0.33 VMware",
                 text_font=("Roboto Medium", -26),
                 command = lambda:Take_input33())
Display4 = customtkinter.CTkButton(master=frame_top,
                 text ="172.16.0.34 VMware",
                 text_font=("Roboto Medium", -26),
                 command = lambda:Take_input34())
Display5 = customtkinter.CTkButton(master=frame_top,
                 text_font=("Roboto Medium", -26),
                 text ="Reset GNS3",
                 command = lambda:confirmgns3())
Display6 = customtkinter.CTkButton(master=frame_top,
                 text_font=("Roboto Medium", -26),
                 text ="Reset Rhel9",
                 command = lambda:confirmgrhel9())
photobutton = customtkinter.CTkButton(root, image = photoimage,
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

el8000label.grid(row=4, column =6, columnspan=1, sticky="ns")
Display.grid(row =1, column=0,pady=10, padx=10)
Display2.grid(row =1, column=1)
Display3.grid(row=2,column=0,pady=10, padx=10)
Display4.grid(row=2,column=1)
photobutton.grid(row=5, column=6, columnspan=1, sticky="w")
Display5.grid(row=3,column=0)
Display6.grid(row=3,column=1,pady=10, padx=10)
Output.grid(row=3,column=2, columnspan=5, rowspan=2)
#Output.grid(row=0,column=4, columnspan=1, rowspan=1)
text_frame.grid(row=4, column=0, columnspan=5, rowspan=2)



root.mainloop()
