
OBJ_FILES=tests/objc/Thing.o tests/objc/Example.o tests/objc/BaseExample.o

all: tests/objc/librubiconharness.dylib

tests/objc/librubiconharness.dylib: $(OBJ_FILES)
	clang -dynamiclib $(OBJ_FILES) -fobjc-arc -fobjc-link-runtime -o tests/objc/librubiconharness.dylib

clean:
	rm -rf tests/objc/*.o tests/objc/*.d tests/objc/librubiconharness.dylib

%.o : %.m
	clang -x objective-c -fobjc-arc -I./tests/objc -c $< -o $@

