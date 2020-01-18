OBJ_FILES=tests/objc/Thing.o tests/objc/Example.o tests/objc/BaseExample.o tests/objc/Blocks.o

all: tests/objc/librubiconharness.dylib

tests/objc/librubiconharness.dylib: $(OBJ_FILES)
	clang -dynamiclib -fobjc-link-runtime $(OBJ_FILES) -o tests/objc/librubiconharness.dylib

clean:
	rm -rf tests/objc/*.o tests/objc/*.d tests/objc/librubiconharness.dylib

%.o: %.m tests/objc/*.h
	clang -x objective-c -I./tests/objc -c $< -o $@

