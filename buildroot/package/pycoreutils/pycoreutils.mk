PYCOREUTILS_VERSION = -1
PYCOREUTILS_SITE = ..
PYCOREUTILS_SITE_METHOD = bzr
PYCOREUTILS_DEPENDENCIES = python

define PYCOREUTILS_BUILD_CMDS
	(cd $(@D) && $(HOST_DIR)/usr/bin/python setup.py build -e /usr/bin/python)
endef

define PYCOREUTILS_INSTALL_TARGET_CMDS
        rm -f $(addprefix $(TARGET_DIR)/usr/bin/,bzip2 bunzip2 bzcat)
	(cd $(@D) && $(HOST_DIR)/usr/bin/python setup.py install --prefix=$(TARGET_DIR)/usr)
	(cd $(TARGET_DIR) && ln -fs usr/bin/pycoreutils init)
	(cd $(TARGET_DIR)/sbin && ln -fs ../usr/bin/pycoreutils init)
	(cd $(TARGET_DIR)/bin && ln -fs ../usr/bin/pycoreutils mount)
	(cd $(TARGET_DIR)/bin && ln -fs ../usr/bin/pycoreutils sh)
        PYTHONPATH=$(TARGET_DIR)/usr/lib/python2.7/site-packages $(HOST_DIR)/usr/bin/python $(TARGET_DIR)/usr/bin/pycoreutils --createlinks $(TARGET_DIR)/usr/bin
endef

$(eval $(call GENTARGETS,package,pycoreutils))
