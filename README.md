# scope-interface
Interfacing Yokogawa DL1540 via GPIB

## Instructions for GPIB-USB installation in Ubuntu
- Get linux-gpib source from http://sourceforge.net/projects/linux-gpib/
- Make sure linux-headers are installed
- Create symbolic link to the System.map file from the kernel source directory: `sudo ln -s /boot/System.map-$(uname -r) /usr/src/linux-headers-$(uname -r)/System.map`
- build and install linux-gpib-kernel by running: `make`, `sudo make install`
    - Do not worry about the possible SSL errors
- build and install linux-gpib-user by running: `./configure --sysconfdir=/etc`, `make`, `sudo make install`
- Reload shared libraries: `sudo ldconfig`
- Create gpib group `sudo groupadd gpib`
- Add current user to the gpib group `sudo usermod -a -G gpib $USER`
- (Disable secure boot, if it's enabled, since the kernel modules are not signed): `sudo mokutil --disable-validation`
- Reboot computer to take the group changes into effect
- Disable secure boot from the MOK utils menu
- Download GPIB firmware from: https://linux-gpib.sourceforge.io/firmware/
- Unzip the agilent_82357a firmware to /usr/local/share/usb/agilent_82357a
- Make sure fxtools is installed from apt
- Plug in the USB

### After updating kernel (Ubuntu)
- Create symbolic link to the System.map file from the kernel source directory: `sudo ln -s /boot/System.map-$(uname -r) /usr/src/linux-headers-$(uname -r)/System.map`
- build and install linux-gpib-kernel by running: `make clean`, `make`, `sudo make install`
- Plug in the USB


