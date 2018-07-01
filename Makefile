OBJ_FILES=tests/objc/Thing.o tests/objc/Example.o tests/objc/BaseExample.o tests/objc/Blocks.o

OS := $(shell uname)
ifeq ($(OS),Darwin)
	CC = clang
	# By default, build a universal i386/x86_64 binary.
	# Modify here (or on the command line) to build for other architecture(s).
	CFLAGS = -arch i386 -arch x86_64
	LDFLAGS = -dynamiclib -arch i386 -arch x86_64
	LDLIBS = -fobjc-link-runtime
	LIB_EXT = dylib
else
	CC = gcc
	CFLAGS =
	LDFLAGS =
	LDLIBS = -lobjc -lgnustep-base
	LIB_EXT = so
endif

all: tests/objc/librubiconharness.$(LIB_EXT)

tests/objc/librubiconharness.$(LIB_EXT): $(OBJ_FILES)
	$(CC) $(LDFLAGS) $(OBJ_FILES) -o tests/objc/librubiconharness.$(LIB_EXT) $(LDLIBS)

clean:
	rm -rf tests/objc/*.o tests/objc/*.d tests/objc/librubiconharness.$(LIB_EXT)

%.o: %.m tests/objc/*.h
	$(CC) -c $(CFLAGS) $< -o $@

