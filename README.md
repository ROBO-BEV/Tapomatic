# Robotic Beverage Technologies Tapomatic Kiosk Software

Author(s): Blaze Sanders Email: blaze.d.a.sanders@gmail.com Skype: blaze.sanders Twitter: @BlazeDSanders

Freshly tapped zero waste coconuts beverage system

This Git repo holds code for many open source libraries. It's broken down into the following directories (***CompressedLibraryCode, v2020.0***).

Please use Style Guide: https://github.com/google/styleguide/blob/gh-pages/pyguide.md

The code was written on and designed to run on the Ubuntu Mate Linux Distro. But some dev work can be done on PC or Mac.
Download Ubuntu Mate for the Raspberry Pi 4 at www.ubuntu-mate.org/raspberry-pi

You can make a bootable microSD card (8 GB or larger) on Desktop Linux using the following commands: 
sudo apt-get install gddrescue xz-utils
unxz ubuntu-mate-18.04.2-beta1-desktop-armhf+raspi-ext4.img.xz
sudo ddrescue -D --force ubuntu-mate-18.04.2-beta1-desktop-armhf+raspi-ext4.img /dev/sd?

Where the ? in sd? can be determined by using the "lsblk" command to find your microSD card name.

We used ***pipenv*** Virtual Enviroment software for v2020.1: https://realpython.com/pipenv-guide

All documentation is self generated using https://www.python.org/dev/peps/pep-0257/
See examples and usage at https://docutils.sourceforge.io/README.html#quick-start

Static type checking was done using http://mypy-lang.org/

Copy .nanorc in your home directory to use the best IDE every made NANO!

Commit message standard shall follow https://www.conventionalcommits.org/en/v1.0.0/

***
v2020.0:

To run the code in v2020.0 directory complete the following steps:

Download this FULL git repo onto a Raspberry Pi 4 B
1. Use "cd Tapomatics" Linux terminal command to navigate to the highest level directory
2. Use "python3 install.py YOUR_PC_USERNAME" command to install all the necessary libraries
3. Use "cd Tapomatics/v2020.0" command to navigate to the main code directory
4. Finally run the command "python3 GUI.py" to start kiosk software running
5. NOTE: Use "python3" and NOT "python", in step 5 or you will get run time errors!!!
6. Open Google Chrome (best GUI compatibility) and type http://127.0.0.1:5000/ into URL textbox. 
7. Type terminal input as prompted when in debug mode. Have fun nerd!

***
CompressedLibraryCode:

RavenBD is a NoSQL Document Database that allows 1 million reads and 150000 writes per second.


***
Python imports:

Flask is a microframework that does not require particular tools or libraries. It has no database abstraction layer and form validation. However, since it runs in any browser setting up a dev envirment is super simple.
