# simple makefile that works both on linux and windows!
# this will compile all .c file into bin dir
# this is my first time making a makefile from scrach and I am somehow proud of it  
# author: alireza-hariri

OUT_DIR := bin

ifdef OS # on windows
	EXT := .exe 
	RM:=rmdir /s /q
else
	EXT := .bin
	RM := rm -r
endif

C_SRCS:=$(wildcard *.c)

OBJS := $(patsubst %.c,$(OUT_DIR)/%$(EXT),$(C_SRCS))
OBJS_O3 := $(patsubst %.c,$(OUT_DIR)/%_O3$(EXT),$(C_SRCS))

all: $(OUT_DIR) $(OBJS) $(OBJS_O3) 

$(OUT_DIR):
	mkdir $(OUT_DIR)

$(OBJS): $(OUT_DIR)/%.exe : ./%.c 
	g++ $^ -o $@ 

$(OBJS_O3): $(OUT_DIR)/%_O3$(EXT) :./%.c
	g++ -O3 $^ -o $@ 

clean:
	$(RM) $(OUT_DIR)
