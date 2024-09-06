
# Makefile

# Define the build directory
BUILD_DIR ?= $(CURDIR)/.pio/build/innetra_board

# Spine directory
export SPINE_DIR := $(HOME)/.platformio/packages/framework-innetra

# Object files
obj-y += src/main.o

VPATH += src

# Application name
export APP := $(notdir $(CURDIR))

# Include the wrapper Makefile
-include $(SPINE_DIR)/scripts/Makefile.wrapper

            