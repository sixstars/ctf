LOCAL_PATH := $(call my-dir)

include $(CLEAR_VARS)

LOCAL_SRC_FILES := \
  main.c \
  forcecrc32.c

LOCAL_MODULE := libZapus
LOCAL_MODULE_TAGS := optional

# LOCAL_CFLAGS += -fPIE
# LOCAL_LDFLAGS += -fPIE -pie

TOP_SRCDIR := $(abspath $(LOCAL_PATH))

include $(BUILD_SHARED_LIBRARY)
