LOCAL_PATH := $(call my-dir)

include $(CLEAR_VARS)

LOCAL_SRC_FILES := \
  main.c

LOCAL_MODULE := ripples
LOCAL_MODULE_TAGS := optional

LOCAL_CFLAGS += -fPIE
LOCAL_LDFLAGS += -fPIE -pie

TOP_SRCDIR := $(abspath $(LOCAL_PATH))

include $(BUILD_EXECUTABLE)
