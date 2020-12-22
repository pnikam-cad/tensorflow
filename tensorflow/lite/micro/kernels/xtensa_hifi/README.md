# Building TensorFlow Lite for Microcontrollers for Cadence Tensilica HiFi DSPs

This document describes the steps to build and run the Tensorflow Lite Micro on
the Cadence HiFi DSPs.

## Pre-requisites

The Xtensa development tools and the target processor configurations should be
installed on the system. Please check [https://tensilicatools.com] for more
information about downloading and installing the required tools.

Set environment variable XTENSA_BASE to point to the Xtensa developer tools 
installation directory.
(Please refer tensorflow/lite/micro/tools/make/targets/xtensa_hifi_makefile.inc) 

## Optimized HiFi NN Library support  
  
Two HiFi NN Libraries are integerated into TensorFlow Lite for Microcontrollers:
HiFi 4 NN Library
HiFi 5 NN Library

These libraries contain HiFi optimized implementation of various low level 
NN kernels.
The folder, tensorflow/lite/micro/kernels/xtensa_hifi, contains the integration
code for using the HiFi NN Libraries.
  
HiFi NN Library support is available for following HiFi DSPs:
Using HiFi 4 NN Library:
  HiFi 4 
  HiFi 3Z
  Fusion F1
Using HiFi 5 NN Library:
  HiFi 5
  

## Building for HiFi Processors

To build the code using Xtensa tools for the processor configuration selected by
XTENSA_CORE, set TARGET=xtensa_hifi. Additionally TARGET_ARCH can be used to
select optimized HiFi NN kernels specific to the processor configuration.

For HiFi 4, HiFi 3z, Fusion F1 DSPs:
setenv XTENSA_BASE <path_to_XtDevTools/install>
make -f tensorflow/lite/micro/tools/make/Makefile TARGET=xtensa_hifi TARGET_ARCH=hifi4 XTENSA_TOOLS_VERSION=RI-2020.5-linux XTENSA_CORE=<HiFi 4/ HiFi 3z / FusionF1 Config> <build_target>

For HiFi 5 DSP:
setenv XTENSA_BASE <path_to_XtDevTools/install>
make -f tensorflow/lite/micro/tools/make/Makefile TARGET=xtensa_hifi TARGET_ARCH=hifi5 XTENSA_TOOLS_VERSION=RI-2020.5-linux XTENSA_CORE=<HiFi 5 Config> <build_target>

Build targets can be:
test : Build and run all test cases
test_person_detection_test: Person detection example
test_person_detection_test_int8: Person detection int8 example
test_micro_speech_test: Micro speech example
test_keyword_benchmark: Wakeword detection benchmark
clean: Clean all builds
clean_downloads: Delete third party download files (previous NN Library downloads)

