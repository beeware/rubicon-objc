OBJ_FILES=Thing.o Example.o BaseExample.o Blocks.o

all: librubiconharness.dylib

librubiconharness.dylib: $(OBJ_FILES)
	clang -dynamiclib -fobjc-link-runtime $(OBJ_FILES) -o librubiconharness.dylib

clean:
	rm -rf *.o *.d librubiconharness.dylib

%.o: %.m *.h
	clang -x objective-c -c $< -o $@
