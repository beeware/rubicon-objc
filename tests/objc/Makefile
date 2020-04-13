OBJCC = clang
OBJCLD_SHARED = $(OBJCC) -shared

OBJCLDFLAGS = -fobjc-link-runtime

OUTPUT_DIR = build
OBJECTS_DIR = $(OUTPUT_DIR)/objects

HEADER_FILES = $(wildcard *.h)
SOURCE_FILES = $(wildcard *.m)
OBJ_FILES = $(addprefix $(OBJECTS_DIR)/,$(addsuffix .o,$(SOURCE_FILES)))

LIB_NAME = librubiconharness.dylib

all: $(OUTPUT_DIR)/$(LIB_NAME)

$(OUTPUT_DIR)/$(LIB_NAME): $(OBJ_FILES)
	@mkdir -p $(@D)
	$(OBJCLD_SHARED) $(OBJCLDFLAGS) $(OBJ_FILES) $(OBJCLDLIBS) -o $@

clean:
	$(RM) -r $(OUTPUT_DIR)

$(OBJECTS_DIR)/%.m.o: %.m $(HEADER_FILES)
	@mkdir -p $(@D)
	$(OBJCC) $(OBJCFLAGS) -c $< -o $@
