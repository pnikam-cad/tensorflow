# Building TensorFlow Lite for Microcontrollers for Cadence Tensilica HiFi DSPs

This document describes the steps to build and run the Tensorflow Lite Micro on
the Cadence HiFi DSPs.

## Pre-requisites

The Xtensa development tools and the target processor configurations should be
installed on the system. Please check [https://tensilicatools.com] for more
information about downloading and installing the required tools.

The PATH variable should be set to include the <xtensa_tools_root>/bin
directory. The XTENSA_SYSTEM and XTENSA_CORE environment variables should be set
to the required tools version and the required processor configuration.

## Building for HiFi Processors

To build the code using Xtensa tools for the processor configuration selected by
XTENSA_CORE , set TARGET=xtensa_hifi. TARGET_ARCH can be used to
select optimized HiFi NN kernels specific to the processor configuration.
Currently the HiFi 4 and HiFi 5 NN Library kernels are integrated.

The command to build for HiFi 4 DSP configurations is as follows:
make -f tensorflow/lite/micro/tools/make/Makefile TARGET=xtensa_hifi TARGET_ARCH=hifi4 test_micro_speech_test

The command to build for HiFi 5 DSP configurations with NN option is as follows:
make -f tensorflow/lite/micro/tools/make/Makefile TARGET=xtensa_hifi TARGET_ARCH=hifi5 test_micro_speech_test

Xtensa specific TF Lite Micro kernels are implemented in this folder:
tensorflow/lite/micro/kernels/xtensa_hifi/

A scratch memory allocation is needed for the HiFi optimized kernels. This
allocation is currently done on stack and it's size can be controlled by
defining 'XTENSA_NNLIB_MAX_SCRATCH_SIZE' approproately in the file
'tensorflow/lite/micro/tools/make/ext_libs/xtensa_hifi_nn_library.inc

The files containing the HiFi optimized NN kernels are downloaded in this folder:
tensorflow/lite/micro/tools/make/downloads/xa_nnlib_hifi4/
tensorflow/lite/micro/tools/make/downloads/xa_nnlib_hifi5/
