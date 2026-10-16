export THEOS ?= $(PWD)/theos
export THEOS_PACKAGE_SCHEME = roothide

include $(THEOS)/makefiles/common.mk

TWEAK_NAME = MangoThermalFix
MangoThermalFix_FILES = patch_dummy.m
MangoThermalFix_CFLAGS = -fobjc-arc
MangoThermalFix_FRAMEWORKS = Foundation
MangoThermalFix_LIBRARIES = substrate

include $(THEOS_MAKE_PATH)/tweak.mk

before-all::
	python3 patch.py layout/Library/MobileSubstrate/DynamicLibraries/MangoPanelBackgroundPlayback.dylib
