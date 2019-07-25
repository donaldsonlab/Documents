# Overview

There are many different ways to get the PS Eye working on a Windows PC. This is pretty confusing, so expect to be confused.

Driver | Cost | Notes
--- | --- | ---
**IPISoft PS3EYEDriver** | Free | Supports multiple cameras. Applications like ex. skype cant see the cameras. The most easy PSEYE driver setup !
**PS3EYEDriver** | Free | Wraps libusb. Open source and continues to be worked on so sometimes can be flaky. Supports as many cameras as there is bandwidth for. Instructions are below.
**CL Eye Platform Driver** | $2.99 USD | Exposes the camera as a DirectShow object so can be used easily by this and other software (e.g. Skype, I think, no guarantees). Only supports one camera.
**CL Eye Platform SDK** | $4.99 USD | Supports multiple cameras. Only works if you use your own (non-redistributable, developer version) CLEyeMulticam.dll. Delete the dll that comes with PSMoveService to use the DLL that gets installed with the SDK.
**CL Eye redistributable + registered camera** | $?? USD * n_cameras | Apparently, after you register your cameras, the redistributable CLEyeMulticam.dll that we supply works. I don't think I ever correctly registered my camera so I don't know if it actually works.

# Setup the camera drivers

## Option A) IPIsoft PSEYE Driver Installation

**NOTE: If you have already install libusb based drivers, please uninstall those drivers first in Windows device manager**

This installation option is very simple. Just download the driver for your Windows OS architecture and all PSEYE Cameras should be recognized. IPISoft is software for Motion Capture Full Body system. This PS3Eye driver was not originally intended to be used with PSMoveService (opensource software), though it does appear to work. Therefore, please do not spam the support of IPISoft with questions about this driver. Use at your own risk.

Downloads:

64-bit OS:

http://files.ipisoft.com/drivers/PlayStation3_Eye_iPi-x64.msi 

32-bit OS:

http://files.ipisoft.com/drivers/PlayStation3_Eye_iPi-x86.msi 

Result in 'Device Manager', tested successfully in Windows 10 x64:

![](http://i.imgur.com/4Kdyp96.jpg)

Source info: 
http://docs.ipisoft.com/User_Guide_for_Multiple_PS_Eye_Cameras_Configuration 

## Option B) Libusb PSEYE Driver Installation

The instructions below apply to our customized version of the [PS3EYEDriver wrapper](https://github.com/HipsterSloth/PS3EYEDriver/tree/psmoveservice) around [libusb](http://libusb.info/). 

### Libusb Driver Pre-Install

Download UsbDeview from [Nirsoft.net](http://www.nirsoft.net/utils/usbdeview-x64.zip). This is a handy utility for showing all connected usb devices attached to your system and what drivers they are running. Once downloaded, launch `usbdeview.exe`.

1. After you have plugged in the PS Eye camera you should see entries for the camera and the microphone of the ps3 eye.
    * The cameras take a lot of USB bandwidth. This is especially a concern if using more than one camera. We have some tips [here](https://github.com/cboulay/PSMoveService/wiki/Troubleshooting-(Windows)#general-weird-camera-behavior-clean-camera-driver-reinstall) on how to manage your camera-connections. Also see [what Oculus has to say](https://www.oculus.com/blog/oculus-roomscale-balancing-bandwidth-on-usb/) on the matter.
2. Under the "service name" column for the camera you should see "usbccgp" for the camera device and "usbaudio" for the audio device. 
  a. If you don't see "usbccgp" for the camera, right-click on the entry with the purple dot and select "uninstall selected devices", after which, unplug the ps3eye camera, and then plug it back in.
3. Close usbdeview

[[images/USBCameraPreInstall.jpg]]

### Libusb Driver Install
Download the Zadig usb utility from [here](http://zadig.akeo.ie/). This is another handy usb utility for installing custom usb drivers. In our case we're going to use it to install the libusb driver over the top of the default Windows driver for the PS Eye camera. Once downloaded, Launch `zadig_2.2.exe`. 

1. From the options menu launch select "List all devices"
2. From the device list drop down select "USB Camera-B4.09.24.1 (Interface 0)"
3. From the driver drop down select "libusb-win32 (v 1.2.6.0)"
4. Click the Install Driver option
5. There should be a few second delay and then it should say "driver installed successfully"

Note: Computer reboot might be require to complete installation.
Note 2: Having an error message from the timeout expiration might not mean the driver was not install properly.

[[images/ZadigInstall.jpg]]

### Libusb Driver Post-Install
1. Launch `usbdeview.exe` again.
2. You should now see an entry in the "service name" column for the PS3Eye camera that says "libusb0"
  a. If you don't see "libusb0" for the camera, right-click on the entry with the purple dot and select "uninstall selected devices", then unplug the ps3eye camera, then plug it back in, and try reinstalling the lib usb driver.
3. Close usbdeview

[[images/USBCameraPostInstall.jpg]]

## Testing
Now that the camera drivers are installed you should be able to run `test_camera.exe` and see a video feed (640x480/60Hz) for each camera you have plugged in (up to 3 cameras max).

If `test_camera.exe` closes immediately, or the video feed is stuck on a solid color, don't panic. This is sadly a common occurrence, especially on a initial setup. It's quite likely that you have to [do some driver shenanigans in zadig](https://github.com/cboulay/PSMoveService/wiki/Troubleshooting-%28Windows%29#cameras-arent-showing-up-using-libusb-driver) to make this work. 

If that worked the first time, please take a moment to celebrate your good fortune. Then launch `PSMoveService.exe`. You should see messages about any attached cameras getting opened in the log window.

Then launch the `PSMoveConfigTool.exe` and open the "Tracker Settings" and "Test Video Feed" sub menu. If your camera is set up properly then this should show you the images from the camera at 640x480/60Hz. While you have the video feed up, it's also a good time to grab the move controller and see if the frame encompasses enough of your intended interaction area with the controller.

Also when the PS Eye camera is recording you should see the red LED turn on. Sometimes this light will get stuck on in the event of an application crash. Most of the time it won't matter, but you can reset the camera simply by unplugging it and then plugging it back in again.

[[images/Recording.jpg]]

# Proceed to the next step
[[PSMove-Bluetooth-Pairing]]
