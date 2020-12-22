# Settings for Xtensa toolchain for the hifi kernels.
# REQUIRED:
#  Environment variables:
#   - XTENSA_BASE  must be set to location of
#     the Xtensa developer tools installation directory.
#  Command line arguments:
#   - XTENSA_TOOLS_VERSION: For example: RI-2019.2-linux
#   - XTENSA_CORE: The name of the Xtensa core to use
#      For example: hifi3

ifeq ($(TARGET), xtensa_hifi)
  TARGET_ARCH := hifi3_bd5

$(eval $(call add_third_party_download,$(XTENSA_HIFI4_URL),$(XTENSA_HIFI4_MD5),xa_nnlib_hifi4,))
$(eval $(call add_third_party_download,$(XTENSA_HIFI5_URL),$(XTENSA_HIFI5_MD5),xa_nnlib_hifi5,))

  ifndef XTENSA_BASE
    $(error XTENSA_BASE is undefined)
  endif

  ifndef XTENSA_TOOLS_VERSION
    $(error XTENSA_TOOLS_VERSION is undefined)
  endif

  ifndef XTENSA_CORE
    $(error XTENSA_CORE is undefined)
  endif

  $(eval $(call add_third_party_download,$(XTENSA_HIFI4_URL),$(XTENSA_HIFI4_MD5),xa_nnlib_hifi4,))
  $(eval $(call add_third_party_download,$(XTENSA_HIFI5_URL),$(XTENSA_HIFI5_MD5),xa_nnlib_hifi5,))

  PLATFORM_ARGS = \
    -mno-mul16 \
    -mno-mul32 \
    -mno-div32 \
    -fsigned-char \
    -fno-exceptions \
    -mlongcalls \
    -INLINE:requested \
    -mcoproc \
    -fno-zero-initialized-in-bss \
    -mtext-section-literals \
    -fno-unsafe-math-optimizations \


  export PATH := $(XTENSA_BASE)/tools/$(XTENSA_TOOLS_VERSION)/XtensaTools/bin:$(PATH)
  TARGET_TOOLCHAIN_PREFIX := xt-
  CXX_TOOL := clang++
  CC_TOOL := clang

  CXXFLAGS += $(PLATFORM_ARGS)
  CCFLAGS += $(PLATFORM_ARGS)

ifneq (,$(filter hifi4%, $(TARGET_ARCH)))
  # TODO(pnikam-cad): analyse and fix issues seen with -O3 optimization level
  # 1. Fusion F1, quantization_util_test
  CXXFLAGS += -O0
endif

  # TODO(b/150240249): Do not remove -fno-rtti once that works for the Xtensa toolchain.
  CXXFLAGS := $(filter-out -fno-rtti, $(CXXFLAGS))

  # Enable sim-local for local RAM based setups 
  #LDFLAGS += -mlsp=sim-local


  TEST_SCRIPT := tensorflow/lite/micro/testing/test_xtensa_hifi_binary.sh

  # These are microcontroller-specific rules for converting the ELF output
  # of the linker into a binary image that can be loaded directly.
  OBJCOPY := $(TARGET_TOOLCHAIN_PREFIX)objcopy

  $(BINDIR)/%.bin: $(BINDIR)/%
	  echo "here"
	  @mkdir -p $(dir $@)
	  $(OBJCOPY) $< $@ -O binary

# TODO(pnikam-cad): Debug and fix the following test cases
  EXCLUDED_EXAMPLE_TESTS := \
    tensorflow/lite/micro/examples/magic_wand/Makefile.inc \
    
  MICRO_LITE_EXAMPLE_TESTS := $(filter-out $(EXCLUDED_EXAMPLE_TESTS), $(MICRO_LITE_EXAMPLE_TESTS))
endif
