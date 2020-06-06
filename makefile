#------------------------------------------------------------------------------
# File       : 通用Makefile
# Enviroment : windows
# Author     : Shibo Jiang
# Time       : 2017.11.17
# Version    : 0.5
# Notes      : 针对STM32F429这款芯片，需要安装make和python的环境
#------------------------------------------------------------------------------

#--------------------------------- 编译参数 ------------------------------------
# 参数名称：显示编译
# 参数说明：在调用工程时输入 make V=1 来显示编译过程，否则默认不显示编译时的指令

ifneq ($(V),1)
Q		:= @
NULL	:= 2>\dev\null
endif

# 参数名称：目标目录，及目标名称
# 参数说明：工程编译生成对象存放的文件夹，及工程文件名称

TARGET_FOLDER := build_result
TARGET := .\$(TARGET_FOLDER)\LedProject

# 参数名称：优化等级
# 参数说明：默认共提供5级优化
#           -O0     无优化(默认) 
#
#           -O/-O1  使用能减少目标文 件 大小以及执行时间并且不会使编译时间明显增
#                   加的优化.在编译大型程序的时候会显著增加编译时内存的使用. 
#
#           -O2     包含-O1的优化并增加了不需要在目标文件大小和执行速度上进行折衷
#                   的优化.编译器不执行循环展开以及函数内联.此选项将增加编译时间和
#                   目标文件的执行性能. 
#
#           -Os     专门优化目标文件大小,执行所有的不增加目标文件大小的-O2优化选
#                   项.并且执行专门减小目标文件大小的优化选项. 
#
#           -O3     打开所有-O2的优化选项并且增加 -finline-functions, 
#                   -funswitch-loops,-fpredictive-commoning, -fgcse-after-reload
#                   and -ftree-vectorize优化选项. 

OPT		:= -O0

# 参数名称：C语言标准
# 参数说明：该选项用于设定编译时执行的C语言标准，提供的选项分别为
#          -std=c90/-ansi/-std=iso9899:1990     各时期标准C版本
#          -std=iso9899:199409                  
#          -std=c99/-std=iso9899:1999           
#          -std=c11/-std=iso9899:2011           
#          -std=gnu90                           或一下具有GNU特性的语言标准 
#          -std=gnu99
#          -std=gnu11

CSTD	:= -std=c11

# 参数名称：CPP语言标准
# 参数说明：该选项用于设定编译时执行的CPP语言标准，提供的选项分别为
#           -std=c++98\-ansi\-std=c++03         同上
#           -std=c++11
#           -std=gnu++98
#           -std=gnu++11


CXXSTD  := -std=c++11

# 参数名称：包含路径
# 参数说明：就是 include 设置，用于为编译器提供寻找.h文件的路径

INC_FLAGS := -I .\$(TARGET_FOLDER)\files_h

# 参数名称：链接文件
# 参数说明：指定链接器链接文件时使用的链接脚本文件

LDSCRIPT := $(shell find -name 'stm32_f103ze_gcc.ld')

# 参数名称：python脚本
# 参数说明：指定make调用的python脚本文件
PYTHON_SCRIPT  := $(shell find -name 'makefile_script.py')

# 参数名称：宏定义
# 参数说明：编译时预编译的宏定义

DEFINES := -D __weak="__attribute__((weak))"
DEFINES += -D __packed="__attribute__((__packed__))"
DEFINES += -D USE_STDPERIPH_DRIVER
DEFINES += -D STM32F10X_HD

# 参数名称：浮点运算参数
# 参数说明：-mfloat-abi用于设定浮点运算模式，共三种选择
#            soft          软件实现
#            softfp        使用浮点运算器但以软方式调用协议
#            hard          使用浮点运算器以FPU-specific调用协议
#
#           -mfpu用于指定FPU类型，根据MCU型号确定，具体可参照gcc.pdf page：206
#           进行设定

# FP_FLAGS := -mfpu=fpv4-sp-d16
# FP_FLAGS += -mfloat-abi=softfp
FP_FLAGS :=

# 参数名称：内核参数
# 参数说明：用于设定编译时使用的内核型号及指令集参数

ARCH_FLAGS :=
ARCH_FLAGS := -mthumb
ARCH_FLAGS += -mcpu=cortex-m3

# 参数名称：警告设置
# 参数说明：用于设定编译时产生警告的级别和内容,部分参数C与C++间不兼容，具体的参数功
#          能及说明请阅读gcc说明书进行了解

CWARN_FLAGS += -Wall -Wshadow
#CWARN_FLAGS += -Wundef  -Wextra  -Wredundant-decls
CWARN_FLAGS += -fno-common -ffunction-sections -fdata-sections
CWARN_FLAGS += -Wimplicit-function-declaration  
#CWARN_FLAGS += -Wmissing-prototypes
CWARN_FLAGS += -Wstrict-prototypes

CXXWARN_CXXFLAGS += -Wall -Wshadow
#CXXWARN_CXXFLAGS += -Wundef  -Wextra  -Wredundant-decls
CXXWARN_CXXFLAGS += -fno-common -ffunction-sections -fdata-sections
CXXWARN_CXXFLAGS += -Weffc++

# 参数名称：警告设置
# 参数说明：用于设定编译时产生警告的级别和内容,部分参数C与C++间不兼容，具体的参数功
#          能及说明请阅读gcc说明书进行了解
LDLIBS		+= -Wl,--start-group -lc -lgcc -lnosys -Wl,--end-group


#----------------------------- 搜索工程目录下的源代码 ---------------------------

AS_SRC := $(shell find ./$(TARGET_FOLDER)/files_s -name '*.s')  
AS_OBJ := $(AS_SRC:%.s=%.o)

C_SRC := $(shell find ./$(TARGET_FOLDER)/files_c -name '*.c')  
C_OBJ := $(C_SRC:%.c=%.o)  

CXX_SRC := $(shell find ./$(TARGET_FOLDER)/files_cpp -name '*.cpp')  
CXX_OBJ := $(CXX_SRC:%.cpp=%.o)


#--------------------------------- 参数整合 ------------------------------------
# C flags
CFLAGS := $(OPT) $ $(CSTD) $(INC_FLAGS) $(FP_FLAGS) 
CFLAGS += $(DEFINES) $(ARCH_FLAGS) $(CWARN_FLAGS) -g

# C++ flags
CXXFLAGS := $(OPT) $ $(CSTD) $(INC_FLAGS) $(FP_FLAGS) 
CXXFLAGS += $(DEFINES) $(ARCH_FLAGS) $(CXXWARN_CXXFLAGS) -g 

# Linker flags
LDFLAGS		:= --static
LDFLAGS		+= -Wl,-Map=$(TARGET).map -Wl,--gc-sections
LDFLAGS		+= -T$(LDSCRIPT) $(ARCH_FLAGS) $(LDLIBS)

# OBJ
OBJ := $(RUN_PY) $(AS_OBJ) $(C_OBJ) $(CXX_OBJ)

#-------------------------------- 编译器调用指令 --------------------------------
PREFIX	:= arm-none-eabi

CC		:= $(PREFIX)-gcc
CXX		:= $(PREFIX)-g++
LD		:= $(PREFIX)-gcc
AR		:= $(PREFIX)-ar
AS		:= $(PREFIX)-as
OBJCOPY	:= $(PREFIX)-objcopy
OBJDUMP	:= $(PREFIX)-objdump
GDB		:= $(PREFIX)-gdb


#----------------------------------- 编译对象 -----------------------------------
# @python3 $(PYTHON_SCRIPT)
all: help

	@echo Have already runned python script, please do next e.g. make elf.

elf: $(TARGET).elf
bin: $(TARGET).bin
hex: $(TARGET).hex
list: $(TARGET).list
images: $(TARGET).images

%.images: %.bin %.hex %.list %.map
	@echo "*** $* images generated ***."
	
%.bin: %.elf          
	@echo "  OBJCOPY $(*).bin."
	$(Q)$(OBJCOPY) -Obinary $(*).elf $(*).bin
	
%.hex: %.elf
	@echo "  OBJCOPY $(*).hex."
	$(Q)$(OBJCOPY) -Oihex $(*).elf $(*).hex
	
%.list: %.elf
	@echo "  OBJDUMP $(*).list."
	$(Q)$(OBJDUMP) -S $(*).elf > $(*).list
	
%.elf %.map: $(OBJ) $(LDSCRIPT)
	@echo "  LD      $(TARGET).elf."
	$(Q)$(LD) $(OBJ) $(LDFLAGS) -o $(TARGET).elf
	
$(AS_OBJ): %.o:%.s
	@echo "  AS      $(*).s"
	$(Q)$(CC) $(ARCH_FLAGS) $(FP_FLAGS) -g -Wa,--no-warn -x assembler-with-cpp -o $(*).o -c $(*).s
	
$(C_OBJ): %.o:%.c
	@echo "  CC      $(*).c"
	$(Q)$(CC) $(CFLAGS) -o $(*).o -c $(*).c
	
$(CXX_OBJ): %.o:%.cxx
	@echo "  CXX     $(*).cpp"
	$(Q)$(CXX) $(CXXFLAGS) -o $(*).o -c $(*).cpp

clean:
	@echo "CLEAN result folder"
	$(Q)$(RM) -f -r $(shell find ./ -name '$(TARGET_FOLDER)')

cleanobject:
	@echo "CLEAN $(*).o"
	@echo "CLEAN $(*).d"
	@echo "CLEAN $(*).elf"
	@echo "CLEAN $(*).bin"
	$(Q)$(RM) $(shell find -name '*.o' -o -name '*.d' -o -name '*.elf' -o -name '*.bin') 
	@echo "CLEAN $(*).hex"
	@echo "CLEAN $(*).srec"
	@echo "CLEAN $(*).list"
	@echo "CLEAN $(*).map"
	$(Q)$(RM) $(shell find -name '*.hex' -o -name '*.srec' -o -name '*.list' -o -name '*.map') 
	@echo "CLEAN generated.$(*)"
	$(Q)$(RM) $(shell find -name 'generated.*' -o -name '*.srec' -o -name '*.list' -o -name '*.map')

help:
	@echo The following are some of the valid targets for this Makefile:
	@echo ... images
	@echo ... elf
	@echo ... bin
	@echo ... hex
	@echo ... list
	@echo ... clean
	@echo ... cleanobject
	@echo ... help
	
.PHONY: images clean elf bin hex list help cleanobject