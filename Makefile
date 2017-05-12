XCODE_MAJOR=`xcodebuild -version | head -n 1 | cut -f 2 -d' ' | cut -d. -f1`
XCODE_MINOR=`xcodebuild -version | head -n 1 | cut -f 2 -d' ' | cut -d. -f2`
XCODE_MICRO=`xcodebuild -version | head -n 1 | cut -f 2 -d' ' | cut -d. -f3`
XCODE_VERSION=$(shell printf '%d' $(XCODE_MAJOR))$(shell printf '%02d' $(XCODE_MINOR))$(shell printf '%02d' $(XCODE_MICRO))

OBJ_FILES=tests/objc/Thing.o tests/objc/Example.o tests/objc/BaseExample.o

# By default, build a universal i386/x86_64 binary.
# Modify here (or on the command line) to build for other architecture(s).
EXTRA_FLAGS=-arch i386 -arch x86_64 -DXCODE_VERSION=$(XCODE_VERSION)

all: tests/objc/librubiconharness.dylib

tests/objc/librubiconharness.dylib: $(OBJ_FILES)
	clang -dynamiclib -fobjc-link-runtime $(EXTRA_FLAGS) $(OBJ_FILES) -o tests/objc/librubiconharness.dylib

clean:
	rm -rf tests/objc/*.o tests/objc/*.d tests/objc/librubiconharness.dylib

%.o: %.m
	clang -x objective-c -I./tests/objc -c $(EXTRA_FLAGS) $< -o $@

