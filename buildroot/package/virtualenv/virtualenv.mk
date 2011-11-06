VIRTUALENV_VERSION = 1.6.4
#VIRTUALENV_SOURCE = virtualenv-$(VIRTUALENV_VERSION).tar.gz
VIRTUALENV_SITE = http://pypi.python.org/packages/source/v/virtualenv
VIRTUALENV_DEPENDENCIES = python

define VIRTUALENV_BUILD_CMDS
	(cd $(@D) && $(HOST_DIR)/usr/bin/python setup.py build -e /usr/bin/python)
endef

define VIRTUALENV_INSTALL_TARGET_CMDS
	(cd $(@D) && $(HOST_DIR)/usr/bin/python setup.py install --prefix=$(TARGET_DIR)/usr)
endef

$(eval $(call GENTARGETS,package,virtualenv))
