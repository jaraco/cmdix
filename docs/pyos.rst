
PyOS
====

.. contents:: :local:

PyOS bla bla bla


Configure
---------

bla bla

::

   make menuconfig

To configure busybox use:

::

   make busybox-menuconfig

Be sure to save your changes to busybox.conf.

To configure the kernel type:

::

   make linux-menuconfig


Build
-----

To build the enviornent, just use

::

   make

A clean build requires about 3 gigabytes of diskspace, and can take several
hours to complete on old hardware.


Test build with QEMU
--------------------

A great way to test your build is to run it in a virtual machine.
On Linux, you can use QEMU:

::

   qemu-kvm -kernel output/images/bzImage

