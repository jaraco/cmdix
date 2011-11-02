PYCOREUTILS_VERSION = -1
PYCOREUTILS_SITE = ..
PYCOREUTILS_SITE_METHOD = bzr
PYCOREUTILS_DEPENDENCIES = python

define PYCOREUTILS_BUILD_CMDS
	(cd $(@D) && $(HOST_DIR)/usr/bin/python setup.py build)
endef

define PYCOREUTILS_INSTALL_TARGET_CMDS
	(cd $(@D) && $(HOST_DIR)/usr/bin/python setup.py install --prefix=$(TARGET_DIR)/usr)
	(cd $(TARGET_DIR) && ln -fs usr/bin/coreutils.py init)
	(cd $(TARGET_DIR)/sbin && ln -fs ../usr/bin/coreutils.py init)
        sed -i "s/#\!.*python/#\!\/usr\/bin\/python/g" $(TARGET_DIR)/usr/bin/coreutils.py 
endef

$(eval $(call GENTARGETS,package,pycoreutils))
