
all: darwin iphoneos iphonesimulator

clean:
	rm -rf tests/*.dylib
	rm -rf tests/*.so
	rm -rf testbed/objc/build
	rm -rf build/testbed

darwin:
	make -C testbed/objc -f Makefile.darwin

iphoneos:
	make -C testbed/objc -f Makefile.iphoneos

iphonesimulator:
	make -C testbed/objc -f Makefile.iphonesimulator


PHONY: all clean darwin iphoneos iphonesimulator
