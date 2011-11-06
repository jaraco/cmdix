PYCOREUTILS_VERSION = -1
PYCOREUTILS_SITE = ..
PYCOREUTILS_SITE_METHOD = bzr
PYCOREUTILS_DEPENDENCIES = python

define PYCOREUTILS_BUILD_CMDS
	(cd $(@D) && $(HOST_DIR)/usr/bin/python setup.py build -e /usr/bin/python)
endef

define PYCOREUTILS_INSTALL_TARGET_CMDS
	(cd $(@D) && $(HOST_DIR)/usr/bin/python setup.py install --prefix=$(TARGET_DIR)/usr)
	(cd $(TARGET_DIR) && ln -fs usr/bin/pycoreutils init)
	(cd $(TARGET_DIR)/sbin && ln -fs ../usr/bin/pycoreutils init)
        $(HOST_DIR)/usr/bin/python $(TARGET_DIR)/usr/bin/pycoreutils --createlinks $(TARGET_DIR)/usr/bin
endef

$(eval $(call GENTARGETS,package,pycoreutils))
