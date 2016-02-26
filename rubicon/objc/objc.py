from __future__ import print_function, absolute_import, division, unicode_literals

import platform
import struct

from ctypes import *
from ctypes import util

from .types import *

__LP64__ = (8*struct.calcsize("P") == 64)
__i386__ = (platform.machine() == 'i386')
__x86_64__ = (platform.machine() == 'x86_64')

if sizeof(c_void_p) == 4:
    c_ptrdiff_t = c_int32
elif sizeof(c_void_p) == 8:
    c_ptrdiff_t = c_int64

######################################################################

objc = cdll.LoadLibrary(util.find_library(b'objc'))

######################################################################

# BOOL class_addIvar(Class cls, const char *name, size_t size, uint8_t alignment, const char *types)
objc.class_addIvar.restype = c_bool
objc.class_addIvar.argtypes = [c_void_p, c_char_p, c_size_t, c_uint8, c_char_p]

# BOOL class_addMethod(Class cls, SEL name, IMP imp, const char *types)
objc.class_addMethod.restype = c_bool

# BOOL class_addProtocol(Class cls, Protocol *protocol)
objc.class_addProtocol.restype = c_bool
objc.class_addProtocol.argtypes = [c_void_p, c_void_p]

# BOOL class_conformsToProtocol(Class cls, Protocol *protocol)
objc.class_conformsToProtocol.restype = c_bool
objc.class_conformsToProtocol.argtypes = [c_void_p, c_void_p]

# Ivar * class_copyIvarList(Class cls, unsigned int *outCount)
# Returns an array of pointers of type Ivar describing instance variables.
# The array has *outCount pointers followed by a NULL terminator.
# You must free() the returned array.
objc.class_copyIvarList.restype = POINTER(c_void_p)
objc.class_copyIvarList.argtypes = [c_void_p, POINTER(c_uint)]

# Method * class_copyMethodList(Class cls, unsigned int *outCount)
# Returns an array of pointers of type Method describing instance methods.
# The array has *outCount pointers followed by a NULL terminator.
# You must free() the returned array.
objc.class_copyMethodList.restype = POINTER(c_void_p)
objc.class_copyMethodList.argtypes = [c_void_p, POINTER(c_uint)]

# objc_property_t * class_copyPropertyList(Class cls, unsigned int *outCount)
# Returns an array of pointers of type objc_property_t describing properties.
# The array has *outCount pointers followed by a NULL terminator.
# You must free() the returned array.
objc.class_copyPropertyList.restype = POINTER(c_void_p)
objc.class_copyPropertyList.argtypes = [c_void_p, POINTER(c_uint)]

# Protocol ** class_copyProtocolList(Class cls, unsigned int *outCount)
# Returns an array of pointers of type Protocol* describing protocols.
# The array has *outCount pointers followed by a NULL terminator.
# You must free() the returned array.
objc.class_copyProtocolList.restype = POINTER(c_void_p)
objc.class_copyProtocolList.argtypes = [c_void_p, POINTER(c_uint)]

# id class_createInstance(Class cls, size_t extraBytes)
objc.class_createInstance.restype = c_void_p
objc.class_createInstance.argtypes = [c_void_p, c_size_t]

# Method class_getClassMethod(Class aClass, SEL aSelector)
# Will also search superclass for implementations.
objc.class_getClassMethod.restype = c_void_p
objc.class_getClassMethod.argtypes = [c_void_p, c_void_p]

# Ivar class_getClassVariable(Class cls, const char* name)
objc.class_getClassVariable.restype = c_void_p
objc.class_getClassVariable.argtypes = [c_void_p, c_char_p]

# Method class_getInstanceMethod(Class aClass, SEL aSelector)
# Will also search superclass for implementations.
objc.class_getInstanceMethod.restype = c_void_p
objc.class_getInstanceMethod.argtypes = [c_void_p, c_void_p]

# size_t class_getInstanceSize(Class cls)
objc.class_getInstanceSize.restype = c_size_t
objc.class_getInstanceSize.argtypes = [c_void_p]

# Ivar class_getInstanceVariable(Class cls, const char* name)
objc.class_getInstanceVariable.restype = c_void_p
objc.class_getInstanceVariable.argtypes = [c_void_p, c_char_p]

# const char *class_getIvarLayout(Class cls)
objc.class_getIvarLayout.restype = c_char_p
objc.class_getIvarLayout.argtypes = [c_void_p]

# IMP class_getMethodImplementation(Class cls, SEL name)
objc.class_getMethodImplementation.restype = c_void_p
objc.class_getMethodImplementation.argtypes = [c_void_p, c_void_p]

# IMP class_getMethodImplementation_stret(Class cls, SEL name)
#objc.class_getMethodImplementation_stret.restype = c_void_p
#objc.class_getMethodImplementation_stret.argtypes = [c_void_p, c_void_p]

# const char * class_getName(Class cls)
objc.class_getName.restype = c_char_p
objc.class_getName.argtypes = [c_void_p]

# objc_property_t class_getProperty(Class cls, const char *name)
objc.class_getProperty.restype = c_void_p
objc.class_getProperty.argtypes = [c_void_p, c_char_p]

# Class class_getSuperclass(Class cls)
objc.class_getSuperclass.restype = c_void_p
objc.class_getSuperclass.argtypes = [c_void_p]

# int class_getVersion(Class theClass)
objc.class_getVersion.restype = c_int
objc.class_getVersion.argtypes = [c_void_p]

# const char *class_getWeakIvarLayout(Class cls)
objc.class_getWeakIvarLayout.restype = c_char_p
objc.class_getWeakIvarLayout.argtypes = [c_void_p]

# BOOL class_isMetaClass(Class cls)
objc.class_isMetaClass.restype = c_bool
objc.class_isMetaClass.argtypes = [c_void_p]

# IMP class_replaceMethod(Class cls, SEL name, IMP imp, const char *types)
objc.class_replaceMethod.restype = c_void_p
objc.class_replaceMethod.argtypes = [c_void_p, c_void_p, c_void_p, c_char_p]

# BOOL class_respondsToSelector(Class cls, SEL sel)
objc.class_respondsToSelector.restype = c_bool
objc.class_respondsToSelector.argtypes = [c_void_p, c_void_p]

# void class_setIvarLayout(Class cls, const char *layout)
objc.class_setIvarLayout.restype = None
objc.class_setIvarLayout.argtypes = [c_void_p, c_char_p]

# Class class_setSuperclass(Class cls, Class newSuper)
objc.class_setSuperclass.restype = c_void_p
objc.class_setSuperclass.argtypes = [c_void_p, c_void_p]

# void class_setVersion(Class theClass, int version)
objc.class_setVersion.restype = None
objc.class_setVersion.argtypes = [c_void_p, c_int]

# void class_setWeakIvarLayout(Class cls, const char *layout)
objc.class_setWeakIvarLayout.restype = None
objc.class_setWeakIvarLayout.argtypes = [c_void_p, c_char_p]

######################################################################

# const char * ivar_getName(Ivar ivar)
objc.ivar_getName.restype = c_char_p
objc.ivar_getName.argtypes = [c_void_p]

# ptrdiff_t ivar_getOffset(Ivar ivar)
objc.ivar_getOffset.restype = c_ptrdiff_t
objc.ivar_getOffset.argtypes = [c_void_p]

# const char * ivar_getTypeEncoding(Ivar ivar)
objc.ivar_getTypeEncoding.restype = c_char_p
objc.ivar_getTypeEncoding.argtypes = [c_void_p]

######################################################################

# char * method_copyArgumentType(Method method, unsigned int index)
# You must free() the returned string.
objc.method_copyArgumentType.restype = c_char_p
objc.method_copyArgumentType.argtypes = [c_void_p, c_uint]

# char * method_copyReturnType(Method method)
# You must free() the returned string.
objc.method_copyReturnType.restype = c_char_p
objc.method_copyReturnType.argtypes = [c_void_p]

# void method_exchangeImplementations(Method m1, Method m2)
objc.method_exchangeImplementations.restype = None
objc.method_exchangeImplementations.argtypes = [c_void_p, c_void_p]

# void method_getArgumentType(Method method, unsigned int index, char *dst, size_t dst_len)
# Functionally similar to strncpy(dst, parameter_type, dst_len).
objc.method_getArgumentType.restype = None
objc.method_getArgumentType.argtypes = [c_void_p, c_uint, c_char_p, c_size_t]

# IMP method_getImplementation(Method method)
objc.method_getImplementation.restype = c_void_p
objc.method_getImplementation.argtypes = [c_void_p]

# SEL method_getName(Method method)
objc.method_getName.restype = c_void_p
objc.method_getName.argtypes = [c_void_p]

# unsigned method_getNumberOfArguments(Method method)
objc.method_getNumberOfArguments.restype = c_uint
objc.method_getNumberOfArguments.argtypes = [c_void_p]

# void method_getReturnType(Method method, char *dst, size_t dst_len)
# Functionally similar to strncpy(dst, return_type, dst_len)
objc.method_getReturnType.restype = None
objc.method_getReturnType.argtypes = [c_void_p, c_char_p, c_size_t]

# const char * method_getTypeEncoding(Method method)
objc.method_getTypeEncoding.restype = c_char_p
objc.method_getTypeEncoding.argtypes = [c_void_p]

# IMP method_setImplementation(Method method, IMP imp)
objc.method_setImplementation.restype = c_void_p
objc.method_setImplementation.argtypes = [c_void_p, c_void_p]

######################################################################

# Class objc_allocateClassPair(Class superclass, const char *name, size_t extraBytes)
objc.objc_allocateClassPair.restype = c_void_p
objc.objc_allocateClassPair.argtypes = [c_void_p, c_char_p, c_size_t]

# Protocol **objc_copyProtocolList(unsigned int *outCount)
# Returns an array of *outcount pointers followed by NULL terminator.
# You must free() the array.
objc.objc_copyProtocolList.restype = POINTER(c_void_p)
objc.objc_copyProtocolList.argtypes = [POINTER(c_int)]

# id objc_getAssociatedObject(id object, void *key)
objc.objc_getAssociatedObject.restype = c_void_p
objc.objc_getAssociatedObject.argtypes = [c_void_p, c_void_p]

# id objc_getClass(const char *name)
objc.objc_getClass.restype = c_void_p
objc.objc_getClass.argtypes = [c_char_p]

# int objc_getClassList(Class *buffer, int bufferLen)
# Pass None for buffer to obtain just the total number of classes.
objc.objc_getClassList.restype = c_int
objc.objc_getClassList.argtypes = [c_void_p, c_int]

# id objc_getMetaClass(const char *name)
objc.objc_getMetaClass.restype = c_void_p
objc.objc_getMetaClass.argtypes = [c_char_p]

# Protocol *objc_getProtocol(const char *name)
objc.objc_getProtocol.restype = c_void_p
objc.objc_getProtocol.argtypes = [c_char_p]

# You should set return and argument types depending on context.
# id objc_msgSend(id theReceiver, SEL theSelector, ...)
# id objc_msgSendSuper(struct objc_super *super, SEL op,  ...)

# The _stret and _fpret variants only exist on x86-based architectures.
if __i386__ or __x86_64__:
    # void objc_msgSendSuper_stret(struct objc_super *super, SEL op, ...)
    objc.objc_msgSendSuper_stret.restype = None

    # double objc_msgSend_fpret(id self, SEL op, ...)
    objc.objc_msgSend_fpret.restype = c_double

    # void objc_msgSend_stret(void * stretAddr, id theReceiver, SEL theSelector,  ...)
    objc.objc_msgSend_stret.restype = None

# void objc_registerClassPair(Class cls)
objc.objc_registerClassPair.restype = None
objc.objc_registerClassPair.argtypes = [c_void_p]

# void objc_removeAssociatedObjects(id object)
objc.objc_removeAssociatedObjects.restype = None
objc.objc_removeAssociatedObjects.argtypes = [c_void_p]

# void objc_setAssociatedObject(id object, void *key, id value, objc_AssociationPolicy policy)
objc.objc_setAssociatedObject.restype = None
objc.objc_setAssociatedObject.argtypes = [c_void_p, c_void_p, c_void_p, c_int]

######################################################################

# id object_copy(id obj, size_t size)
objc.object_copy.restype = c_void_p
objc.object_copy.argtypes = [c_void_p, c_size_t]

# id object_dispose(id obj)
objc.object_dispose.restype = c_void_p
objc.object_dispose.argtypes = [c_void_p]

# Class object_getClass(id object)
objc.object_getClass.restype = c_void_p
objc.object_getClass.argtypes = [c_void_p]

# const char *object_getClassName(id obj)
objc.object_getClassName.restype = c_char_p
objc.object_getClassName.argtypes = [c_void_p]

# Ivar object_getInstanceVariable(id obj, const char *name, void **outValue)
objc.object_getInstanceVariable.restype = c_void_p
objc.object_getInstanceVariable.argtypes = [c_void_p, c_char_p, c_void_p]

# id object_getIvar(id object, Ivar ivar)
objc.object_getIvar.restype = c_void_p
objc.object_getIvar.argtypes = [c_void_p, c_void_p]

# Class object_setClass(id object, Class cls)
objc.object_setClass.restype = c_void_p
objc.object_setClass.argtypes = [c_void_p, c_void_p]

# Ivar object_setInstanceVariable(id obj, const char *name, void *value)
# Set argtypes based on the data type of the instance variable.
objc.object_setInstanceVariable.restype = c_void_p

# void object_setIvar(id object, Ivar ivar, id value)
objc.object_setIvar.restype = None
objc.object_setIvar.argtypes = [c_void_p, c_void_p, c_void_p]

######################################################################

# const char *property_getAttributes(objc_property_t property)
objc.property_getAttributes.restype = c_char_p
objc.property_getAttributes.argtypes = [c_void_p]

# const char *property_getName(objc_property_t property)
objc.property_getName.restype = c_char_p
objc.property_getName.argtypes = [c_void_p]

######################################################################

# BOOL protocol_conformsToProtocol(Protocol *proto, Protocol *other)
objc.protocol_conformsToProtocol.restype = c_bool
objc.protocol_conformsToProtocol.argtypes = [c_void_p, c_void_p]


class OBJC_METHOD_DESCRIPTION(Structure):
    _fields_ = [("name", c_void_p), ("types", c_char_p)]

# struct objc_method_description *protocol_copyMethodDescriptionList(Protocol *p, BOOL isRequiredMethod, BOOL isInstanceMethod, unsigned int *outCount)
# You must free() the returned array.
objc.protocol_copyMethodDescriptionList.restype = POINTER(OBJC_METHOD_DESCRIPTION)
objc.protocol_copyMethodDescriptionList.argtypes = [c_void_p, c_bool, c_bool, POINTER(c_uint)]

# objc_property_t * protocol_copyPropertyList(Protocol *protocol, unsigned int *outCount)
objc.protocol_copyPropertyList.restype = c_void_p
objc.protocol_copyPropertyList.argtypes = [c_void_p, POINTER(c_uint)]

# Protocol **protocol_copyProtocolList(Protocol *proto, unsigned int *outCount)
objc.protocol_copyProtocolList = POINTER(c_void_p)
objc.protocol_copyProtocolList.argtypes = [c_void_p, POINTER(c_uint)]

# struct objc_method_description protocol_getMethodDescription(Protocol *p, SEL aSel, BOOL isRequiredMethod, BOOL isInstanceMethod)
objc.protocol_getMethodDescription.restype = OBJC_METHOD_DESCRIPTION
objc.protocol_getMethodDescription.argtypes = [c_void_p, c_void_p, c_bool, c_bool]

# const char *protocol_getName(Protocol *p)
objc.protocol_getName.restype = c_char_p
objc.protocol_getName.argtypes = [c_void_p]

######################################################################

# const char* sel_getName(SEL aSelector)
objc.sel_getName.restype = c_char_p
objc.sel_getName.argtypes = [c_void_p]

# SEL sel_getUid(const char *str)
# Use sel_registerName instead.

# BOOL sel_isEqual(SEL lhs, SEL rhs)
objc.sel_isEqual.restype = c_bool
objc.sel_isEqual.argtypes = [c_void_p, c_void_p]

# SEL sel_registerName(const char *str)
objc.sel_registerName.restype = c_void_p
objc.sel_registerName.argtypes = [c_char_p]


######################################################################

def ensure_bytes(x):
    if isinstance(x, bytes):
        return x
    return x.encode('ascii')


######################################################################

class SEL(c_void_p):
    pass


def get_selector(name):
    "Return a reference to the selector with the given name."
    return SEL(objc.sel_registerName(ensure_bytes(name)))


def get_class(name):
    "Return a reference to the class with the given name."
    return c_void_p(objc.objc_getClass(ensure_bytes(name)))


def get_metaclass(name):
    "Return a reference to the metaclass for the given name."
    return c_void_p(objc.objc_getMetaClass(ensure_bytes(name)))


def get_superclass_of_object(obj):
    "Return a reference to the superclass of the given object."
    cls = c_void_p(objc.object_getClass(obj))
    return c_void_p(objc.class_getSuperclass(cls))


# http://www.sealiesoftware.com/blog/archive/2008/10/30/objc_explain_objc_msgSend_stret.html
# http://www.x86-64.org/documentation/abi-0.99.pdf  (pp.17-23)
# executive summary: on x86-64, who knows?
def should_use_stret(restype):
    """Try to figure out when a return type will be passed on stack."""
    if type(restype) != type(Structure):
        return False
    if not __LP64__ and sizeof(restype) <= 8:
        return False
    if __LP64__ and sizeof(restype) <= 16:  # maybe? I don't know?
        return False
    return True


# http://www.sealiesoftware.com/blog/archive/2008/11/16/objc_explain_objc_msgSend_fpret.html
def should_use_fpret(restype):
    """Determine if objc_msgSend_fpret is required to return a floating point type."""
    if not (__i386__ or __x86_64__):
        # Unneeded on non-intel processors
        return False
    if __LP64__ and restype == c_longdouble:
        # Use only for long double on x86_64
        return True
    if not __LP64__ and restype in (c_float, c_double, c_longdouble):
        return True
    return False


def send_message(receiver, selName, *args, **kwargs):
    """Send a mesage named selName to the receiver with the provided arguments.

    This is the equivalen of [receiver selname:args]

    By default, assumes that return type for the message is c_void_p,
    and that all arguments are wrapped inside c_void_p. Use the restype
    and argtypes keyword arguments to change these values. restype should
    be a ctypes type and argtypes should be a list of ctypes types for
    the arguments of the message only.
    """
    if isinstance(receiver, text):
        receiver = get_class(receiver)
    selector = get_selector(selName)
    restype = kwargs.get('restype', c_void_p)
    argtypes = kwargs.get('argtypes', [])
    # Choose the correct version of objc_msgSend based on return type.
    if should_use_fpret(restype):
        objc.objc_msgSend_fpret.restype = restype
        objc.objc_msgSend_fpret.argtypes = [c_void_p, c_void_p] + argtypes
        result = objc.objc_msgSend_fpret(receiver, selector, *args)
    elif should_use_stret(restype):
        objc.objc_msgSend_stret.argtypes = [POINTER(restype), c_void_p, c_void_p] + argtypes
        result = restype()
        objc.objc_msgSend_stret(byref(result), receiver, selector, *args)
    else:
        objc.objc_msgSend.restype = restype
        objc.objc_msgSend.argtypes = [c_void_p, c_void_p] + argtypes
        result = objc.objc_msgSend(receiver, selector, *args)
        if restype == c_void_p:
            result = c_void_p(result)
    return result


class OBJC_SUPER(Structure):
    _fields_ = [('receiver', c_void_p), ('class', c_void_p)]

OBJC_SUPER_PTR = POINTER(OBJC_SUPER)


#http://stackoverflow.com/questions/3095360/what-exactly-is-super-in-objective-c
def send_super(receiver, selName, *args, **kwargs):
    """Send a message named selName to the super of the receiver.

    This is the equivalent of [super selname:args].
    """
    if hasattr(receiver, '_as_parameter_'):
        receiver = receiver._as_parameter_
    superclass = get_superclass_of_object(receiver)
    super_struct = OBJC_SUPER(receiver, superclass)
    selector = get_selector(selName)
    restype = kwargs.get('restype', c_void_p)
    argtypes = kwargs.get('argtypes', None)
    objc.objc_msgSendSuper.restype = restype
    if argtypes:
        objc.objc_msgSendSuper.argtypes = [OBJC_SUPER_PTR, c_void_p] + argtypes
    else:
        objc.objc_msgSendSuper.argtypes = None
    result = objc.objc_msgSendSuper(byref(super_struct), selector, *args)
    if restype == c_void_p:
        result = c_void_p(result)
    return result


######################################################################


def encoding_from_annotation(f, offset=1):
    try:
        encoding = [f.__annotations__['return'], ObjCInstance, SEL]
    except KeyError:
        encoding = [ObjCInstance, ObjCInstance, SEL]

    for i in range(offset, f.__code__.co_argcount):
        varname = f.__code__.co_varnames[i]
        try:
            enc = f.__annotations__[varname]
        except KeyError:
            enc = ObjCInstance
        encoding.append(enc)
    return encoding


cfunctype_table = {}


# Limited to basic types and pointers to basic types.
# Does not try to handle arrays, arbitrary structs, unions, or bitfields.
# Assume that encoding is a bytes object and not unicode.
def cfunctype_for_encoding(encoding):
    # Otherwise, create a new CFUNCTYPE for the encoding.
    typecodes = {
        c_char: c_char,
        c_int: c_int,
        int: c_int,
        c_short: c_short,
        c_long: c_long,
        c_longlong: c_longlong,
        c_ubyte: c_ubyte,
        c_uint: c_uint,
        c_ushort: c_ushort,
        c_ulong: c_ulong,
        c_ulonglong: c_ulonglong,
        c_float: c_float,
        float: c_float,
        c_double: c_double,
        c_bool: c_bool,
        bool: c_bool,
        None: None,
        c_char_p: c_char_p,
        str: c_char_p,
        ObjCInstance: c_void_p,
        ObjCClass: c_void_p,
        SEL: c_void_p,
        # function: c_void_p,
        NSPoint: NSPoint,
        NSSize: NSSize,
        NSRect: NSRect,
        NSRange: NSRange,
        py_object: py_object
    }
    argtypes = []
    for code in encoding:
        if code in typecodes:
            argtypes.append(typecodes[code])
        else:
            raise Exception('unknown type encoding: %s', code)

    cfunctype = CFUNCTYPE(*argtypes)

    return cfunctype


def typestring_for_encoding(encoding):
    typecodes = {
        c_char: b'c',
        c_int: b'i',
        int: b'i',
        c_short: b's',
        c_long: b'l',
        c_longlong: b'q',
        c_ubyte: b'C',
        c_uint: b'I',
        c_ushort: b'S',
        c_ulong: b'L',
        c_ulonglong: b'Q',
        c_float: b'f',
        float: b'f',
        c_double: b'd',
        c_bool: b'B',
        bool: b'B',
        None: b'v',
        c_char_p: b'*',
        str: b'*',
        ObjCInstance: b'@',
        ObjCClass: b'#',
        SEL: b':',
        NSPoint: NSPointEncoding,
        NSSize: NSSizeEncoding,
        NSRect: NSRectEncoding,
        NSRange: NSRangeEncoding,
        py_object: PyObjectEncoding,
    }
    return b''.join(typecodes[e] for e in encoding)


######################################################################

def add_method(cls, selName, method, encoding):
    """Add a new instance method named selName to cls.

    method should be a Python method that does all necessary type conversions.

    encoding is an array describing the argument types of the method.
    The first type code of types is the return type (e.g. 'v' if void)
    The second type code must be an ObjCInstance for id self.
    The third type code must be a selector.
    Additional type codes are for types of other arguments if any.
    """
    assert(encoding[1] is ObjCInstance)  # ensure id self typecode
    assert(encoding[2] == SEL)  # ensure SEL cmd typecode
    selector = get_selector(selName)
    types = typestring_for_encoding(encoding)

    # Check if we've already created a CFUNCTYPE for this encoding.
    # If so, then return the cached CFUNCTYPE.
    try:
        cfunctype = cfunctype_table[types]
    except KeyError:
        cfunctype = cfunctype_for_encoding(encoding)
        cfunctype_table[types] = cfunctype

    imp = cfunctype(method)
    objc.class_addMethod.argtypes = [c_void_p, c_void_p, cfunctype, c_char_p]
    objc.class_addMethod(cls, selector, imp, types)
    return imp


def add_ivar(cls, name, vartype):
    "Add a new instance variable of type vartype to cls."
    return objc.class_addIvar(cls, ensure_bytes(name), sizeof(vartype), alignment(vartype), encoding_for_ctype(vartype))


def set_instance_variable(obj, varname, value, vartype):
    "Do the equivalent of `obj.varname = value`, where value is of type vartype."
    objc.object_setInstanceVariable.argtypes = [c_void_p, c_char_p, vartype]
    objc.object_setInstanceVariable(obj, ensure_bytes(varname), value)


def get_instance_variable(obj, varname, vartype):
    "Return the value of `obj.varname`, where the value is of type vartype."
    variable = vartype()
    objc.object_getInstanceVariable(obj, ensure_bytes(varname), byref(variable))
    return variable.value


######################################################################

class ObjCMethod(object):
    """This represents an unbound Objective-C method (really an IMP)."""

    # Note, need to map 'c' to c_byte rather than c_char, because otherwise
    # ctypes converts the value into a one-character string which is generally
    # not what we want at all, especially when the 'c' represents a bool var.
    typecodes = {
        b'c': c_byte,
        b'i': c_int,
        b's': c_short,
        b'l': c_long,
        b'q': c_longlong,
        b'C': c_ubyte,
        b'I': c_uint,
        b'S': c_ushort,
        b'L': c_ulong,
        b'Q': c_ulonglong,
        b'f': c_float,
        b'd': c_double,
        b'B': c_bool,
        b'v': None,
        b'Vv': None,
        b'*': c_char_p,
        b'@': c_void_p,
        b'#': c_void_p,
        b':': c_void_p,
        b'^v': c_void_p,
        b'?': c_void_p,
        NSPointEncoding: NSPoint,
        NSSizeEncoding: NSSize,
        NSRectEncoding: NSRect,
        NSRangeEncoding: NSRange,
        PyObjectEncoding: py_object
    }

    cfunctype_table = {}

    def __init__(self, method):
        """Initialize with an Objective-C Method pointer.  We then determine
        the return type and argument type information of the method."""
        self.selector = c_void_p(objc.method_getName(method))
        self.name = objc.sel_getName(self.selector)
        self.pyname = self.name.replace(b':', b'_')
        self.encoding = objc.method_getTypeEncoding(method)
        self.return_type = objc.method_copyReturnType(method)
        self.nargs = objc.method_getNumberOfArguments(method)
        self.imp = c_void_p(objc.method_getImplementation(method))
        self.argument_types = []

        for i in range(self.nargs):
            buffer = c_buffer(512)
            objc.method_getArgumentType(method, i, buffer, len(buffer))
            self.argument_types.append(buffer.value)
        # Get types for all the arguments.
        try:
            self.argtypes = [self.ctype_for_encoding(t) for t in self.argument_types]
        except:
            print('No argtypes encoding for %s (%s)' % (self.name, self.argument_types))
            self.argtypes = None
        # Get types for the return type.
        try:
            if self.return_type == b'@':
                self.restype = ObjCInstance
            elif self.return_type == b'#':
                self.restype = ObjCClass
            else:
                self.restype = self.ctype_for_encoding(self.return_type)
        except:
            print('No restype encoding for %s (%s)' % (self.name, self.return_type))
            self.restype = None
        self.func = None

    def ctype_for_encoding(self, encoding):
        """Return ctypes type for an encoded Objective-C type."""
        if encoding in self.typecodes:
            return self.typecodes[encoding]
        elif encoding[0:1] == b'^' and encoding[1:] in self.typecodes:
            return POINTER(self.typecodes[encoding[1:]])
        elif encoding[0:1] == b'^' and encoding[1:] in [CGImageEncoding, NSZoneEncoding]:
            # special cases
            return c_void_p
        elif encoding[0:1] == b'r' and encoding[1:] in self.typecodes:
            # const decorator, don't care
            return self.typecodes[encoding[1:]]
        elif encoding[0:2] == b'r^' and encoding[2:] in self.typecodes:
            # const pointer, also don't care
            return POINTER(self.typecodes[encoding[2:]])
        else:
            raise Exception('unknown encoding for %s: %s' % (self.name, encoding))

    def get_prototype(self):
        """Returns a ctypes CFUNCTYPE for the method."""
        if self.restype == ObjCInstance or self.restype == ObjCClass:
            # Some hacky stuff to get around ctypes issues on 64-bit.  Can't let
            # ctypes convert the return value itself, because it truncates the pointer
            # along the way.  So instead, we must do set the return type to c_void_p to
            # ensure we get 64-bit addresses and then convert the return value manually.
            self.prototype = CFUNCTYPE(c_void_p, *self.argtypes)
        else:
            self.prototype = CFUNCTYPE(self.restype, *self.argtypes)
        return self.prototype

    def __repr__(self):
        return "<ObjCMethod: %s %s>" % (self.name, self.encoding)

    def get_callable(self):
        """Returns a python-callable version of the method's IMP."""
        if not self.func:
            prototype = self.get_prototype()
            self.func = cast(self.imp, prototype)
            if self.restype == ObjCInstance or self.restype == ObjCClass:
                self.func.restype = c_void_p
            else:
                self.func.restype = self.restype
            self.func.argtypes = self.argtypes
        return self.func

    def __call__(self, objc_id, *args):
        """Call the method with the given id and arguments.  You do not need
        to pass in the selector as an argument since it will be automatically
        provided."""
        f = self.get_callable()
        try:
            # Automatically convert Python strings into ObjC strings
            from .core_foundation import from_value, to_value
            result = f(objc_id, self.selector, *(from_value(arg) for arg in args))
            # Convert result to python type if it is a instance or class pointer.
            if self.restype == ObjCInstance:
                result = to_value(ObjCInstance(result))
            elif self.restype == ObjCClass:
                result = ObjCClass(result)
            return result
        except ArgumentError as error:
            # Add more useful info to argument error exceptions, then reraise.
            error.args += ('selector = ' + self.name.decode('utf-8'),
                           'argtypes =' + text(self.argtypes),
                           'encoding = ' + self.encoding.decode('utf-8'))
            raise


######################################################################

class ObjCBoundMethod(object):
    """This represents an Objective-C method (an IMP) which has been bound
    to some id which will be passed as the first parameter to the method."""

    def __init__(self, method, objc_id):
        """Initialize with a method and ObjCInstance or ObjCClass object."""
        self.method = method
        self.objc_id = objc_id

    def __repr__(self):
        return '<ObjCBoundMethod %s (%s)>' % (self.method.name, self.objc_id)

    def __call__(self, *args):
        """Call the method with the given arguments."""
        return self.method(self.objc_id, *args)

######################################################################


def cache_instance_method(self, name):
    """Returns a python representation of the named instance method,
    either by looking it up in the cached list of methods or by searching
    for and creating a new method object."""
    try:
        return self.__dict__['instance_methods'][name]
    except KeyError:
        selector = get_selector(name.replace('_', ':'))
        method = c_void_p(objc.class_getInstanceMethod(self.__dict__['ptr'], selector))
        if method.value:
            objc_method = ObjCMethod(method)
            self.__dict__['instance_methods'][name] = objc_method
            return objc_method
    return None


def cache_class_method(self, name):
    """Returns a python representation of the named class method,
    either by looking it up in the cached list of methods or by searching
    for and creating a new method object."""
    try:
        return self.__dict__['class_methods'][name]
    except KeyError:
        selector = get_selector(name.replace('_', ':'))
        method = c_void_p(objc.class_getClassMethod(self.__dict__['ptr'], selector))

        if method.value:
            objc_method = ObjCMethod(method)
            self.__dict__['class_methods'][name] = objc_method
            return objc_method
    return None


def cache_instance_property_methods(self, name):
    """Return the accessor and mutator for the named property.
    """
    if name.endswith('_'):
        # If the requested name ends with _, that's a marker that we're
        # dealing with a method call, not a property, so we can shortcut
        # the process.
        methods = None
    else:
        # Check 1: Does the class respond to the property?
        responds = objc.class_getProperty(self.__dict__['ptr'], name.encode('utf-8'))

        # Check 2: Does the class have an instance method to retrieve the given name
        accessor_selector = get_selector(name)
        accessor = objc.class_getInstanceMethod(self.__dict__['ptr'], accessor_selector)

        # Check 3: Is there a setName: method to set the property with the given name
        mutator_selector = get_selector('set' + name[0].title() + name[1:] + ':')
        mutator = objc.class_getInstanceMethod(self.__dict__['ptr'], mutator_selector)

        # If the class responds as a property, or it has both an accessor *and*
        # and mutator, then treat it as a property in Python.
        if responds or (accessor and mutator):
            if accessor:
                objc_accessor = ObjCMethod(c_void_p(accessor))
            else:
                objc_accessor = None

            if mutator:
                objc_mutator = ObjCMethod(c_void_p(mutator))
            else:
                objc_mutator = None

            methods = (objc_accessor, objc_mutator)
        else:
            methods = None
    return methods


def cache_instance_property_accessor(self, name):
    """Returns a python representation of an accessor for the named
    property. Existence of a property is done by looking for the write
    selector (set<Name>:).
    """
    try:
        methods = self.__dict__['instance_properties'][name]
    except KeyError:
        methods = cache_instance_property_methods(self, name)
        self.__dict__['instance_properties'][name] = methods
    if methods:
        return methods[0]
    return None


def cache_instance_property_mutator(self, name):
    """Returns a python representation of an accessor for the named
    property. Existence of a property is done by looking for the write
    selector (set<Name>:).
    """
    try:
        methods = self.__dict__['instance_properties'][name]
    except KeyError:
        methods = cache_instance_property_methods(self, name)
        self.__dict__['instance_properties'][name] = methods
    if methods:
        return methods[1]
    return None


def cache_class_property_methods(self, name):
    """Return the accessor and mutator for the named property. Existence
    of a property is done by looking for the pair of selectors "name" and
    "set<Name>:". If both exist, we assume this is a static property.
    """
    if name.endswith('_'):
        # If the requested name ends with _, that's a marker that we're
        # dealing with a method call, not a property, so we can shortcut
        # the process.
        methods = None
    else:
        accessor_selector = get_selector(name)
        accessor = c_void_p(objc.class_getClassMethod(self.__dict__['ptr'], accessor_selector))
        if accessor.value:
            objc_accessor = ObjCMethod(accessor)
        else:
            objc_accessor = None

        mutator_selector = get_selector('set' + name[0].title() + name[1:] + ':')
        mutator = c_void_p(objc.class_getClassMethod(self.__dict__['ptr'], mutator_selector))
        if mutator.value:
            objc_mutator = ObjCMethod(mutator)
        else:
            objc_mutator = None

        if objc_accessor and objc_mutator:
            methods = (objc_accessor, objc_mutator)
        else:
            methods = None
    return methods


def cache_class_property_accessor(self, name):
    """Returns a python representation of an accessor for the named
    property. Existence of a property is done by looking for the write
    selector (set<Name>:).
    """
    try:
        methods = self.__dict__['class_properties'][name]
    except KeyError:
        methods = cache_class_property_methods(self, name)
        self.__dict__['class_properties'][name] = methods
    if methods:
        return methods[0]
    return None


def cache_class_property_mutator(self, name):
    """Returns a python representation of an accessor for the named
    property. Existence of a property is done by looking for the write
    selector (set<Name>:).
    """
    try:
        methods = self.__dict__['class_properties'][name]
    except KeyError:
        methods = cache_class_property_methods(self, name)
        self.__dict__['class_properties'][name] = methods
    if methods:
        return methods[1]
    return None


######################################################################

def convert_method_arguments(encoding, args):
    """Used to convert Objective-C method arguments to Python values
    before passing them on to the Python-defined method.
    """
    from .core_foundation import to_value
    new_args = []
    for e, a in zip(encoding[3:], args):
        if issubclass(e, ObjCInstance):
            new_args.append(to_value(ObjCInstance(a)))
        elif e == ObjCClass:
            new_args.append(ObjCClass(a))
        else:
            new_args.append(a)
    return new_args


def objc_method(f):
    encoding = encoding_from_annotation(f)

    def _objc_method(objc_self, objc_cmd, *args):
        from .core_foundation import at
        py_self = ObjCInstance(objc_self)
        args = convert_method_arguments(encoding, args)
        result = f(py_self, *args)
        if isinstance(result, ObjCClass):
            result = result.ptr.value
        elif isinstance(result, ObjCInstance):
            result = result.ptr.value
        elif isinstance(result, text):
            result = at(result).ptr.value
        return result

    def register(cls):
        return add_method(cls.__dict__['ptr'], f.__name__.replace('_', ':'), _objc_method, encoding)

    _objc_method.register = register

    return _objc_method


# def objc_classmethod(encoding):
#     """Function decorator for class methods."""
#     # Add encodings for hidden self and cmd arguments.
#     encoding = ensure_bytes(encoding)
#     typecodes = parse_type_encoding(encoding)
#     typecodes.insert(1, b'@:')
#     encoding = b''.join(typecodes)

def objc_classmethod(f):
    encoding = encoding_from_annotation(f)

    def _objc_classmethod(objc_cls, objc_cmd, *args):
        from .core_foundation import at
        py_cls = ObjCClass(objc_cls)
        args = convert_method_arguments(encoding, args)
        result = f(py_cls, *args)
        if isinstance(result, ObjCClass):
            result = result.ptr.value
        elif isinstance(result, ObjCInstance):
            result = result.ptr.value
        elif isinstance(result, text):
            result = at(result).ptr.value
        return result

    def register(cls):
        return add_method(cls.__dict__['metaclass'], f.__name__.replace('_', ':'), _objc_classmethod, encoding)

    _objc_classmethod.register = register

    return _objc_classmethod


class objc_ivar(object):
    """Add instance variable named varname to the subclass.
    varname should be a string.
    vartype is a ctypes type.
    The class must be registered AFTER adding instance variables.
    """
    def __init__(self, vartype):
        self.vartype = vartype

    def pre_register(self, ptr, name):
        return add_ivar(ptr, name, self.vartype)


# def objc_rawmethod(encoding):
#     """Decorator for instance methods without any fancy shenanigans.
#     The function must have the signature f(self, cmd, *args)
#     where both self and cmd are just pointers to objc objects.
#     """
#     # Add encodings for hidden self and cmd arguments.
#     encoding = ensure_bytes(encoding)
#     typecodes = parse_type_encoding(encoding)
#     typecodes.insert(1, b'@:')
#     encoding = b''.join(typecodes)

def objc_rawmethod(f):
    encoding = encoding_from_annotation(f, offset=2)
    name = f.__name__.replace('_', ':')

    def register(cls):
        return add_method(cls, name, f, encoding)
    f.register = register
    return f

######################################################################


class ObjCClass(type):
    """Python wrapper for an Objective-C class."""

    # We only create one Python object for each Objective-C class.
    # Any future calls with the same class will return the previously
    # created Python object.  Note that these aren't weak references.
    # After you create an ObjCClass, it will exist until the end of the
    # program.
    _registered_classes = {}

    def __new__(cls, *args):
        """Create a new ObjCClass instance or return a previously created
        instance for the given Objective-C class.  The argument may be either
        the name of the class to retrieve, a pointer to the class, or the
        usual (name, bases, attrs) triple that is provided when called as
        a subclass."""

        if len(args) == 1:
            # A single argument provided. If it's a string, treat it as
            # a class name. Anything else treat as a class pointer.

            # Determine name and ptr values from passed in argument.
            class_name_or_ptr = args[0]
            attrs = {}

            if isinstance(class_name_or_ptr, (bytes, text)):
                name = ensure_bytes(class_name_or_ptr)
                ptr = get_class(name)
                if ptr.value is None:
                    raise NameError("ObjC Class '%s' couldn't be found." % class_name_or_ptr)
            else:
                ptr = class_name_or_ptr
                # Make sure that ptr value is wrapped in c_void_p object
                # for safety when passing as ctypes argument.
                if not isinstance(ptr, c_void_p):
                    ptr = c_void_p(ptr)
                name = objc.class_getName(ptr)
                # "nil" is an ObjC answer confirming the ptr didn't work.
                if name == b'nil':
                    raise RuntimeError("Couldn't create ObjC class for pointer '%s'." % class_name_or_ptr)

        else:
            name, bases, attrs = args
            name = ensure_bytes(name)
            if not isinstance(bases[0], ObjCClass):
                raise RuntimeError("Base class isn't an ObjCClass.")

            ptr = get_class(name)
            if ptr.value is None:
                # Create the ObjC class description
                ptr = c_void_p(objc.objc_allocateClassPair(bases[0].__dict__['ptr'], name, 0))

                # Pre-Register all the instance variables
                for attr, obj in attrs.items():
                    try:
                        obj.pre_register(ptr, attr)
                    except AttributeError:
                        # The class attribute doesn't have a pre_register method.
                        pass

                # Register the ObjC class
                objc.objc_registerClassPair(ptr)
            else:
                raise RuntimeError("ObjC runtime already contains a registered class named '%s'." % name.decode('utf-8'))

        # Check if we've already created a Python object for this class
        # and if so, return it rather than making a new one.
        try:
            objc_class = cls._registered_classes[name]
        except KeyError:

            # We can get the metaclass only after the class is registered.
            metaclass = get_metaclass(name)

            # Py2/3 compatibility; the class name must be "str".
            # If the unicode class exists, we're in Python 2.
            try:
                unicode
                objc_class_name = name
            except NameError:
                objc_class_name = name.decode('utf-8')

            # Otherwise create a new Python object and then initialize it.
            objc_class = super(ObjCClass, cls).__new__(cls, objc_class_name, (ObjCInstance,), {
                    'ptr': ptr,
                    'metaclass': metaclass,
                    'name': objc_class_name,
                    'instance_methods': {},     # mapping of name -> instance method
                    'class_methods': {},        # mapping of name -> class method
                    'instance_properties': {},  # mapping of name -> (accessor method, mutator method)
                    'class_properties': {},     # mapping of name -> (accessor method, mutator method)
                    'imp_table': {},            # Mapping of name -> Native method references
                    '_as_parameter_': ptr,      # for ctypes argument passing
                })

            # Store the new class in dictionary of registered classes.
            cls._registered_classes[name] = objc_class

        # Register all the methods, class methods, etc
        for attr, obj in attrs.items():
            try:
                objc_class.__dict__['imp_table'][attr] = obj.register(objc_class)
            except AttributeError:
                # The class attribute doesn't have a register method.
                pass

        return objc_class

    def __repr__(self):
        return "<ObjCClass: %s at %s>" % (self.__dict__['name'], text(self.__dict__['ptr'].value))

    def __getattr__(self, name):
        """Returns a callable method object with the given name."""
        # If name refers to a class method, then return a callable object
        # for the class method with self.__dict__['ptr'] as hidden first parameter.
        if not name.endswith('_'):
            method = cache_class_property_accessor(self, name)
            if method:
                return ObjCBoundMethod(method, self.__dict__['ptr'])()

        method = cache_class_method(self, name)
        if method:
            return ObjCBoundMethod(method, self.__dict__['ptr'])

        # Otherwise, raise an exception.
        raise AttributeError('ObjCClass %s has no attribute %s' % (self.name, name))

    def __setattr__(self, name, value):
        # Set the value of an attribute.
        method = cache_class_property_mutator(self, name)
        if method:
            ObjCBoundMethod(method, self.__dict__['ptr'])(value)
            return

        raise AttributeError('ObjCClass %s cannot set attribute %s' % (self.__dict__['name'], name))


######################################################################

class ObjCInstance(object):
    """Python wrapper for an Objective-C instance."""

    _cached_objects = {}

    def __new__(cls, object_ptr):
        """Create a new ObjCInstance or return a previously created one
        for the given object_ptr which should be an Objective-C id."""
        # Make sure that object_ptr is wrapped in a c_void_p.
        if not isinstance(object_ptr, c_void_p):
            object_ptr = c_void_p(object_ptr)

        # If given a nil pointer, return None.
        if not object_ptr.value:
            return None

        # Check if we've already created an python ObjCInstance for this
        # object_ptr id and if so, then return it.  A single ObjCInstance will
        # be created for any object pointer when it is first encountered.
        # This same ObjCInstance will then persist until the object is
        # deallocated.
        if object_ptr.value in cls._cached_objects:
            return cls._cached_objects[object_ptr.value]

        # Otherwise, create a new ObjCInstance.
        objc_instance = super(ObjCInstance, cls).__new__(cls)
        objc_instance.__dict__['ptr'] = object_ptr
        objc_instance.__dict__['_as_parameter_'] = object_ptr
        # Determine class of this object.
        class_ptr = c_void_p(objc.object_getClass(object_ptr))
        objc_instance.__dict__['objc_class'] = ObjCClass(class_ptr)

        # Store new object in the dictionary of cached objects, keyed
        # by the (integer) memory address pointed to by the object_ptr.
        cls._cached_objects[object_ptr.value] = objc_instance

        # Create a DeallocationObserver and associate it with this object.
        # When the Objective-C object is deallocated, the observer will remove
        # the ObjCInstance corresponding to the object from the cached objects
        # dictionary, effectively destroying the ObjCInstance.
        observer = send_message(send_message('DeallocationObserver', 'alloc'), 'initWithObject:', objc_instance)
        objc.objc_setAssociatedObject(objc_instance, observer, observer, 0x301)

        # The observer is retained by the object we associate it to.  We release
        # the observer now so that it will be deallocated when the associated
        # object is deallocated.
        send_message(observer, 'release')

        return objc_instance

    def __repr__(self):
        if self.__dict__['objc_class'].__dict__['name'] == '__NSCFString':
            # Display contents of NSString objects
            from .core_foundation import to_str
            string = to_str(self)
            return "<ObjCInstance %#x: %s (%s) at %s>" % (id(self), self.__dict__['objc_class'].name, string, text(self.__dict__['ptr'].value))

        return "<ObjCInstance %#x: %s at %s>" % (id(self), self.__dict__['objc_class'].name, text(self.__dict__['ptr'].value))

    def __getattr__(self, name):
        """Returns a callable method object with the given name."""
        # Search for named instance method in the class object and if it
        # exists, return callable object with self as hidden argument.
        # Note: you should give self and not self.__dict__['ptr'] as a parameter to
        # ObjCBoundMethod, so that it will be able to keep the ObjCInstance
        # alive for chained calls like MyClass.alloc().init() where the
        # object created by alloc() is not assigned to a variable.

        # If there's a property with this name; return the value directly.
        # If the name ends with _, we can shortcut this step, because it's
        # clear that we're dealing with a method call.
        if not name.endswith('_'):
            method = cache_instance_property_accessor(self.__dict__['objc_class'], name)
            if method:
                return ObjCBoundMethod(method, self)()

        method = cache_instance_method(self.__dict__['objc_class'], name)
        if method:
            return ObjCBoundMethod(method, self)

        # Otherwise raise an exception.
        raise AttributeError('ObjCInstance %s has no attribute %s' % (self.__dict__['objc_class'].name, name))

    def __setattr__(self, name, value):
        # Set the value of an attribute.
        method = cache_instance_property_mutator(self.__dict__['objc_class'], name)
        if method:
            ObjCBoundMethod(method, self)(value)
            return

        raise AttributeError('ObjCInstance %s cannot set attribute %s' % (self.__dict__['objc_class'].name, name))

######################################################################

# Instances of DeallocationObserver are associated with every
# Objective-C object that gets wrapped inside an ObjCInstance.
# Their sole purpose is to watch for when the Objective-C object
# is deallocated, and then remove the object from the dictionary
# of cached ObjCInstance objects kept by the ObjCInstance class.
#
# The methods of the class defined below are decorated with
# rawmethod() instead of method() because DeallocationObservers
# are created inside of ObjCInstance's __new__ method and we have
# to be careful to not create another ObjCInstance here (which
# happens when the usual method decorator turns the self argument
# into an ObjCInstance), or else get trapped in an infinite recursion.

NSObject = ObjCClass('NSObject')


class DeallocationObserver(NSObject):

    observed_object = objc_ivar(c_void_p)

    @objc_rawmethod
    def initWithObject_(self, cmd, anObject):
        self = send_super(self, 'init')
        self = self.value
        set_instance_variable(self, 'observed_object', anObject, c_void_p)
        return self

    @objc_rawmethod
    def dealloc(self, cmd) -> None:
        anObject = get_instance_variable(self, 'observed_object', c_void_p)
        ObjCInstance._cached_objects.pop(anObject, None)
        send_super(self, 'dealloc')

    @objc_rawmethod
    def finalize(self, cmd) -> None:
        # Called instead of dealloc if using garbage collection.
        # (which would have to be explicitly started with
        # objc_startCollectorThread(), so probably not too much reason
        # to have this here, but I guess it can't hurt.)
        anObject = get_instance_variable(self, 'observed_object', c_void_p)
        ObjCInstance._cached_objects.pop(anObject, None)
        send_super(self, 'finalize')
