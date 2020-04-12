OBJCC = clang
OBJCLD_SHARED = $(OBJCC) -shared

OBJCLDFLAGS = -fobjc-link-runtime

OBJ_FILES=Thing.o Example.o BaseExample.o Blocks.o

all: librubiconharness.dylib

librubiconharness.dylib: $(OBJ_FILES)
	$(OBJCLD_SHARED) $(OBJCLDFLAGS) $(OBJ_FILES) $(OBJCLDLIBS) -o $@

clean:
	$(RM) -r *.o *.d librubiconharness.dylib

%.o: %.m *.h
	$(OBJCC) $(OBJCFLAGS) -c $< -o $@
