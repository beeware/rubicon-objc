import collections.abc
import inspect
import os
from collections import deque

from enum import Enum

from ctypes import *
from ctypes import util

from .types import *
from .types import __LP64__, __i386__, __x86_64__, __arm__, __arm64__

if sizeof(c_void_p) == 4:
    c_ptrdiff_t = c_int32
elif sizeof(c_void_p) == 8:
    c_ptrdiff_t = c_int64
else:
    raise TypeError("Don't know a c_ptrdiff_t for %d-byte pointers" % sizeof(c_void_p))

######################################################################

_lib_path = ["/usr/lib"]
_framework_path = ["/System/Library/Frameworks"]
def _load_or_error(name):
    path = util.find_library(name)
    if path is not None:
        return CDLL(path)

    # On iOS (and probably also watchOS and tvOS), ctypes.util.find_library doesn't work and always returns None.
    # This is because the sandbox hides all system libraries from the filesystem and pretends they don't exist.
    # However they can still be loaded if the path is known, so we try to load the library from a few known locations.
    
    for loc in _lib_path:
        try:
            return CDLL(os.path.join(loc, "lib" + name + ".dylib"))
        except OSError:
            pass
    
    for loc in _framework_path:
        try:
            return CDLL(os.path.join(loc, name + ".framework", name))
        except OSError:
            pass
    
    raise ValueError("Library {!r} not found".format(name))

c = _load_or_error('c')
objc = _load_or_error('objc')
Foundation = _load_or_error('Foundation')

@with_encoding(b'@')
class objc_id(c_void_p):
    pass


@with_encoding(b'@?')
class objc_block(c_void_p):
    pass


@with_preferred_encoding(b':')
class SEL(c_void_p):
    @property
    def name(self):
        if self.value is None:
            raise ValueError("Cannot get name of null selector")

        return objc.sel_getName(self)

    def __new__(cls, init=None):
        if isinstance(init, (bytes, str)):
            self = objc.sel_registerName(ensure_bytes(init))
            self._inited = True
            return self
        else:
            self = super().__new__(cls, init)
            self._inited = False
            return self

    def __init__(self, init=None):
        if not self._inited:
            super().__init__(init)

    def __repr__(self):
        return "{cls.__module__}.{cls.__qualname__}({name!r})".format(cls=type(self), name=None if self.value is None else self.name)

@with_preferred_encoding(b'#')
class Class(objc_id):
    pass

class IMP(c_void_p):
    pass

class Method(c_void_p):
    pass

class Ivar(c_void_p):
    pass

class objc_property_t(c_void_p):
    pass

######################################################################

# void free(void *)
c.free.restype = None
c.free.argtypes = [c_void_p]

# BOOL class_addIvar(Class cls, const char *name, size_t size, uint8_t alignment, const char *types)
objc.class_addIvar.restype = c_bool
objc.class_addIvar.argtypes = [Class, c_char_p, c_size_t, c_uint8, c_char_p]

# BOOL class_addMethod(Class cls, SEL name, IMP imp, const char *types)
objc.class_addMethod.restype = c_bool
objc.class_addMethod.argtypes = [Class, SEL, IMP, c_char_p]

# BOOL class_addProtocol(Class cls, Protocol *protocol)
objc.class_addProtocol.restype = c_bool
objc.class_addProtocol.argtypes = [Class, objc_id]

# BOOL class_conformsToProtocol(Class cls, Protocol *protocol)
objc.class_conformsToProtocol.restype = c_bool
objc.class_conformsToProtocol.argtypes = [Class, objc_id]

# Ivar * class_copyIvarList(Class cls, unsigned int *outCount)
# Returns an array of pointers of type Ivar describing instance variables.
# The array has *outCount pointers followed by a NULL terminator.
# You must free() the returned array.
objc.class_copyIvarList.restype = POINTER(Ivar)
objc.class_copyIvarList.argtypes = [Class, POINTER(c_uint)]

# Method * class_copyMethodList(Class cls, unsigned int *outCount)
# Returns an array of pointers of type Method describing instance methods.
# The array has *outCount pointers followed by a NULL terminator.
# You must free() the returned array.
objc.class_copyMethodList.restype = POINTER(Method)
objc.class_copyMethodList.argtypes = [Class, POINTER(c_uint)]

# objc_property_t * class_copyPropertyList(Class cls, unsigned int *outCount)
# Returns an array of pointers of type objc_property_t describing properties.
# The array has *outCount pointers followed by a NULL terminator.
# You must free() the returned array.
objc.class_copyPropertyList.restype = POINTER(objc_property_t)
objc.class_copyPropertyList.argtypes = [Class, POINTER(c_uint)]

# Protocol ** class_copyProtocolList(Class cls, unsigned int *outCount)
# Returns an array of pointers of type Protocol* describing protocols.
# The array has *outCount pointers followed by a NULL terminator.
# You must free() the returned array.
objc.class_copyProtocolList.restype = POINTER(objc_id)
objc.class_copyProtocolList.argtypes = [Class, POINTER(c_uint)]

# Method class_getClassMethod(Class aClass, SEL aSelector)
# Will also search superclass for implementations.
objc.class_getClassMethod.restype = Method
objc.class_getClassMethod.argtypes = [Class, SEL]

# Ivar class_getClassVariable(Class cls, const char* name)
objc.class_getClassVariable.restype = Ivar
objc.class_getClassVariable.argtypes = [Class, c_char_p]

# Method class_getInstanceMethod(Class aClass, SEL aSelector)
# Will also search superclass for implementations.
objc.class_getInstanceMethod.restype = Method
objc.class_getInstanceMethod.argtypes = [Class, SEL]

# size_t class_getInstanceSize(Class cls)
objc.class_getInstanceSize.restype = c_size_t
objc.class_getInstanceSize.argtypes = [Class]

# Ivar class_getInstanceVariable(Class cls, const char* name)
objc.class_getInstanceVariable.restype = Ivar
objc.class_getInstanceVariable.argtypes = [Class, c_char_p]

# const char *class_getIvarLayout(Class cls)
objc.class_getIvarLayout.restype = c_char_p
objc.class_getIvarLayout.argtypes = [Class]

# IMP class_getMethodImplementation(Class cls, SEL name)
objc.class_getMethodImplementation.restype = IMP
objc.class_getMethodImplementation.argtypes = [Class, SEL]

# const char * class_getName(Class cls)
objc.class_getName.restype = c_char_p
objc.class_getName.argtypes = [Class]

# objc_property_t class_getProperty(Class cls, const char *name)
objc.class_getProperty.restype = objc_property_t
objc.class_getProperty.argtypes = [Class, c_char_p]

# Class class_getSuperclass(Class cls)
objc.class_getSuperclass.restype = Class
objc.class_getSuperclass.argtypes = [Class]

# int class_getVersion(Class theClass)
objc.class_getVersion.restype = c_int
objc.class_getVersion.argtypes = [Class]

# const char *class_getWeakIvarLayout(Class cls)
objc.class_getWeakIvarLayout.restype = c_char_p
objc.class_getWeakIvarLayout.argtypes = [Class]

# BOOL class_isMetaClass(Class cls)
objc.class_isMetaClass.restype = c_bool
objc.class_isMetaClass.argtypes = [Class]

# IMP class_replaceMethod(Class cls, SEL name, IMP imp, const char *types)
objc.class_replaceMethod.restype = IMP
objc.class_replaceMethod.argtypes = [Class, SEL, Ivar, c_char_p]

# BOOL class_respondsToSelector(Class cls, SEL sel)
objc.class_respondsToSelector.restype = c_bool
objc.class_respondsToSelector.argtypes = [Class, SEL]

# void class_setIvarLayout(Class cls, const char *layout)
objc.class_setIvarLayout.restype = None
objc.class_setIvarLayout.argtypes = [Class, c_char_p]

# void class_setVersion(Class theClass, int version)
objc.class_setVersion.restype = None
objc.class_setVersion.argtypes = [Class, c_int]

# void class_setWeakIvarLayout(Class cls, const char *layout)
objc.class_setWeakIvarLayout.restype = None
objc.class_setWeakIvarLayout.argtypes = [Class, c_char_p]

######################################################################

# const char * ivar_getName(Ivar ivar)
objc.ivar_getName.restype = c_char_p
objc.ivar_getName.argtypes = [Ivar]

# ptrdiff_t ivar_getOffset(Ivar ivar)
objc.ivar_getOffset.restype = c_ptrdiff_t
objc.ivar_getOffset.argtypes = [Ivar]

# const char * ivar_getTypeEncoding(Ivar ivar)
objc.ivar_getTypeEncoding.restype = c_char_p
objc.ivar_getTypeEncoding.argtypes = [Ivar]

######################################################################

# void method_exchangeImplementations(Method m1, Method m2)
objc.method_exchangeImplementations.restype = None
objc.method_exchangeImplementations.argtypes = [Method, Method]

# IMP method_getImplementation(Method method)
objc.method_getImplementation.restype = IMP
objc.method_getImplementation.argtypes = [Method]

# SEL method_getName(Method method)
objc.method_getName.restype = SEL
objc.method_getName.argtypes = [Method]

# const char * method_getTypeEncoding(Method method)
objc.method_getTypeEncoding.restype = c_char_p
objc.method_getTypeEncoding.argtypes = [Method]

# IMP method_setImplementation(Method method, IMP imp)
objc.method_setImplementation.restype = IMP
objc.method_setImplementation.argtypes = [Method, IMP]

######################################################################

# Class objc_allocateClassPair(Class superclass, const char *name, size_t extraBytes)
objc.objc_allocateClassPair.restype = Class
objc.objc_allocateClassPair.argtypes = [Class, c_char_p, c_size_t]

# Protocol **objc_copyProtocolList(unsigned int *outCount)
# Returns an array of *outcount pointers followed by NULL terminator.
# You must free() the array.
objc.objc_copyProtocolList.restype = POINTER(objc_id)
objc.objc_copyProtocolList.argtypes = [POINTER(c_int)]

# id objc_getAssociatedObject(id object, void *key)
objc.objc_getAssociatedObject.restype = objc_id
objc.objc_getAssociatedObject.argtypes = [objc_id, c_void_p]

# Class objc_getClass(const char *name)
objc.objc_getClass.restype = Class
objc.objc_getClass.argtypes = [c_char_p]

# Class objc_getMetaClass(const char *name)
objc.objc_getMetaClass.restype = Class
objc.objc_getMetaClass.argtypes = [c_char_p]

# Protocol *objc_getProtocol(const char *name)
objc.objc_getProtocol.restype = objc_id
objc.objc_getProtocol.argtypes = [c_char_p]

# You should set return and argument types depending on context.
# id objc_msgSend(id theReceiver, SEL theSelector, ...)
# id objc_msgSendSuper(struct objc_super *super, SEL op,  ...)

# The _stret variants only exist on x86-based architectures and ARM32.
if __i386__ or __x86_64__ or __arm__:
    # void objc_msgSendSuper_stret(struct objc_super *super, SEL op, ...)
    objc.objc_msgSendSuper_stret.restype = None

    # void objc_msgSend_stret(void * stretAddr, id theReceiver, SEL theSelector,  ...)
    objc.objc_msgSend_stret.restype = None

# The _fpret variant only exists on x86-based architectures.
if __i386__ or __x86_64__:
    # double objc_msgSend_fpret(id self, SEL op, ...)
    objc.objc_msgSend_fpret.restype = c_double

# void objc_registerClassPair(Class cls)
objc.objc_registerClassPair.restype = None
objc.objc_registerClassPair.argtypes = [Class]

# void objc_removeAssociatedObjects(id object)
objc.objc_removeAssociatedObjects.restype = None
objc.objc_removeAssociatedObjects.argtypes = [objc_id]

# void objc_setAssociatedObject(id object, void *key, id value, objc_AssociationPolicy policy)
objc.objc_setAssociatedObject.restype = None
objc.objc_setAssociatedObject.argtypes = [objc_id, c_void_p, objc_id, c_int]

######################################################################

# BOOL object_isClass(id obj)
objc.object_isClass.restype = c_bool
objc.object_isClass.argtypes = [objc_id]

# Class object_getClass(id object)
objc.object_getClass.restype = Class
objc.object_getClass.argtypes = [objc_id]

# const char *object_getClassName(id obj)
objc.object_getClassName.restype = c_char_p
objc.object_getClassName.argtypes = [objc_id]

# Ivar object_getInstanceVariable(id obj, const char *name, void **outValue)
objc.object_getInstanceVariable.restype = Ivar
objc.object_getInstanceVariable.argtypes = [objc_id, c_char_p, POINTER(c_void_p)]

# id object_getIvar(id object, Ivar ivar)
objc.object_getIvar.restype = objc_id
objc.object_getIvar.argtypes = [objc_id, Ivar]

# Ivar object_setInstanceVariable(id obj, const char *name, void *value)
# Set argtypes based on the data type of the instance variable.
objc.object_setInstanceVariable.restype = Ivar

# void object_setIvar(id object, Ivar ivar, id value)
objc.object_setIvar.restype = None
objc.object_setIvar.argtypes = [objc_id, Ivar, objc_id]

######################################################################

# const char *property_getAttributes(objc_property_t property)
objc.property_getAttributes.restype = c_char_p
objc.property_getAttributes.argtypes = [objc_property_t]

# const char *property_getName(objc_property_t property)
objc.property_getName.restype = c_char_p
objc.property_getName.argtypes = [objc_property_t]

######################################################################

# BOOL protocol_conformsToProtocol(Protocol *proto, Protocol *other)
objc.protocol_conformsToProtocol.restype = c_bool
objc.protocol_conformsToProtocol.argtypes = [objc_id, objc_id]


class objc_method_description(Structure):
    _fields_ = [("name", SEL), ("types", c_char_p)]

# struct objc_method_description *protocol_copyMethodDescriptionList(Protocol *p, BOOL isRequiredMethod, BOOL isInstanceMethod, unsigned int *outCount)
# You must free() the returned array.
objc.protocol_copyMethodDescriptionList.restype = POINTER(objc_method_description)
objc.protocol_copyMethodDescriptionList.argtypes = [objc_id, c_bool, c_bool, POINTER(c_uint)]

# objc_property_t * protocol_copyPropertyList(Protocol *protocol, unsigned int *outCount)
objc.protocol_copyPropertyList.restype = POINTER(objc_property_t)
objc.protocol_copyPropertyList.argtypes = [objc_id, POINTER(c_uint)]

# Protocol **protocol_copyProtocolList(Protocol *proto, unsigned int *outCount)
objc.protocol_copyProtocolList = POINTER(objc_id)
objc.protocol_copyProtocolList.argtypes = [objc_id, POINTER(c_uint)]

# struct objc_method_description protocol_getMethodDescription(Protocol *p, SEL aSel, BOOL isRequiredMethod, BOOL isInstanceMethod)
objc.protocol_getMethodDescription.restype = objc_method_description
objc.protocol_getMethodDescription.argtypes = [objc_id, SEL, c_bool, c_bool]

# const char *protocol_getName(Protocol *p)
objc.protocol_getName.restype = c_char_p
objc.protocol_getName.argtypes = [objc_id]

######################################################################

# const char* sel_getName(SEL aSelector)
objc.sel_getName.restype = c_char_p
objc.sel_getName.argtypes = [SEL]

# BOOL sel_isEqual(SEL lhs, SEL rhs)
objc.sel_isEqual.restype = c_bool
objc.sel_isEqual.argtypes = [SEL, SEL]

# SEL sel_registerName(const char *str)
objc.sel_registerName.restype = SEL
objc.sel_registerName.argtypes = [c_char_p]


######################################################################

def ensure_bytes(x):
    if isinstance(x, bytes):
        return x
    # "All char * in the runtime API should be considered to have UTF-8 encoding."
    # https://developer.apple.com/documentation/objectivec/objective_c_runtime?preferredLanguage=occ
    return x.encode('utf-8')


######################################################################


def get_class(name):
    "Return a reference to the class with the given name."
    return objc.objc_getClass(ensure_bytes(name))


def get_metaclass(name):
    "Return a reference to the metaclass for the given name."
    return objc.objc_getMetaClass(ensure_bytes(name))


def get_superclass_of_object(obj):
    "Return a reference to the superclass of the given object."
    cls = objc.object_getClass(obj)
    return objc.class_getSuperclass(cls)


# http://www.sealiesoftware.com/blog/archive/2008/10/30/objc_explain_objc_msgSend_stret.html
# http://www.x86-64.org/documentation/abi-0.99.pdf  (pp.17-23)
# executive summary: on x86-64, who knows?
def should_use_stret(restype):
    """Determine if objc_msgSend_stret is required to return a struct type."""
    if type(restype) != type(Structure):
        # Not needed when restype is not a structure.
        return False
    elif __i386__:
        # On i386: Use for structures not sized exactly like an integer (1, 2, 4, or 8 bytes).
        return sizeof(restype) not in (1, 2, 4, 8)
    elif __x86_64__:
        # On x86_64: Use for structures larger than 16 bytes.
        # (The ABI docs say that there are some special cases
        # for vector types, but those can't really be used
        # with ctypes anyway.)
        return sizeof(restype) > 16
    elif __arm__:
        # On ARM32: Use for all structures, regardless of size.
        return True
    else:
        # Other platforms: Doesn't exist.
        return False


# http://www.sealiesoftware.com/blog/archive/2008/11/16/objc_explain_objc_msgSend_fpret.html
def should_use_fpret(restype):
    """Determine if objc_msgSend_fpret is required to return a floating point type."""
    if __x86_64__:
        # On x86_64: Use only for long double.
        return restype == c_longdouble
    elif __i386__:
        # On i386: Use for all floating-point types.
        return restype in (c_float, c_double, c_longdouble)
    else:
        # Other platforms: Doesn't exist.
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
    if type(receiver) in (ObjCClass, ObjCInstance):
        receiver = receiver._as_parameter_

    if isinstance(receiver, (str, bytes)):
        receiver = cast(get_class(receiver), objc_id)
    elif type(receiver) in (objc_id, Class, c_void_p):
        receiver = cast(receiver, objc_id)
    else:
        raise TypeError("Invalid type for receiver: {tp.__module__}.{tp.__qualname__}".format(tp=type(receiver)))

    selector = SEL(selName)
    restype = kwargs.get('restype', c_void_p)
    argtypes = kwargs.get('argtypes', [])

    # Choose the correct version of objc_msgSend based on return type.
    # Use objc['name'] instead of objc.name to get a new function object
    # that is independent of the one on the objc library.
    # This way multiple threads sending messages don't overwrite
    # each other's function signatures.
    if should_use_fpret(restype):
        send = objc['objc_msgSend_fpret']
        send.restype = restype
        send.argtypes = [objc_id, SEL] + argtypes
        result = send(receiver, selector, *args)
    elif should_use_stret(restype):
        send = objc['objc_msgSend_stret']
        send.restype = restype
        send.argtypes = [objc_id, SEL] + argtypes
        result = send(receiver, selector, *args)
    else:
        send = objc['objc_msgSend']
        send.restype = restype
        send.argtypes = [objc_id, SEL] + argtypes
        result = send(receiver, selector, *args)
        if restype == c_void_p:
            result = c_void_p(result)
    return result


class objc_super(Structure):
    _fields_ = [('receiver', objc_id), ('super_class', Class)]


#http://stackoverflow.com/questions/3095360/what-exactly-is-super-in-objective-c
def send_super(receiver, selName, *args, **kwargs):
    """Send a message named selName to the super of the receiver.

    This is the equivalent of [super selname:args].
    """
    if hasattr(receiver, '_as_parameter_'):
        receiver = receiver._as_parameter_
    superclass = get_superclass_of_object(receiver)
    super_struct = objc_super(receiver, superclass)
    selector = SEL(selName)
    restype = kwargs.get('restype', c_void_p)
    argtypes = kwargs.get('argtypes', None)

    send = objc['objc_msgSendSuper']
    send.restype = restype
    if argtypes:
        send.argtypes = [POINTER(objc_super), SEL] + argtypes
    else:
        send.argtypes = None
    result = send(byref(super_struct), selector, *args)
    if restype == c_void_p:
        result = c_void_p(result)
    return result


######################################################################


def encoding_from_annotation(f, offset=1):
    argspec = inspect.getfullargspec(inspect.unwrap(f))

    encoding = [argspec.annotations.get('return', ObjCInstance), ObjCInstance, SEL]

    for varname in argspec.args[offset:]:
        encoding.append(argspec.annotations.get(varname, ObjCInstance))

    return encoding

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
    signature = tuple(ctype_for_type(tp) for tp in encoding)
    assert signature[1] == objc_id  # ensure id self typecode
    assert signature[2] == SEL  # ensure SEL cmd typecode
    selector = SEL(selName)
    types = b"".join(encoding_for_ctype(ctype) for ctype in signature)

    cfunctype = CFUNCTYPE(*signature)
    imp = cfunctype(method)
    objc.class_addMethod(cls, selector, cast(imp, IMP), types)
    return imp


def add_ivar(cls, name, vartype):
    "Add a new instance variable of type vartype to cls."
    return objc.class_addIvar(cls, ensure_bytes(name), sizeof(vartype), alignment(vartype), encoding_for_ctype(ctype_for_type(vartype)))


def set_instance_variable(obj, varname, value, vartype):
    "Do the equivalent of `obj.varname = value`, where value is of type vartype."
    objc.object_setInstanceVariable.argtypes = [objc_id, c_char_p, vartype]
    objc.object_setInstanceVariable(obj, ensure_bytes(varname), value)


def get_instance_variable(obj, varname, vartype):
    "Return the value of `obj.varname`, where the value is of type vartype."
    variable = vartype()
    objc.object_getInstanceVariable(obj, ensure_bytes(varname), byref(variable))
    return variable.value


######################################################################

class ObjCMethod(object):
    """This represents an unbound Objective-C method (really an IMP)."""

    def __init__(self, method):
        """Initialize with an Objective-C Method pointer.  We then determine
        the return type and argument type information of the method."""
        self.selector = objc.method_getName(method)
        self.name = self.selector.name
        self.pyname = self.name.replace(b':', b'_')
        self.encoding = objc.method_getTypeEncoding(method)
        self.restype, *self.argtypes = ctypes_for_method_encoding(self.encoding)
        self.imp = objc.method_getImplementation(method)
        self.func = None

    def get_prototype(self):
        """Returns a ctypes CFUNCTYPE for the method."""
        return CFUNCTYPE(self.restype, *self.argtypes)

    def __repr__(self):
        return "<ObjCMethod: %s %s>" % (self.name, self.encoding)

    def get_callable(self):
        """Returns a python-callable version of the method's IMP."""
        if not self.func:
            self.func = cast(self.imp, self.get_prototype())
            self.func.restype = self.restype
            self.func.argtypes = self.argtypes
        return self.func

    def __call__(self, receiver, *args, convert_args=True, convert_result=True):
        """Call the method with the given id and arguments.  You do not need
        to pass in the selector as an argument since it will be automatically
        provided."""
        f = self.get_callable()

        if convert_args:
            from .core_foundation import from_value
            converted_args = []
            for argtype, arg in zip(self.argtypes[2:], args):
                if isinstance(arg, Enum):
                    # Convert Python enum objects to their values
                    arg = arg.value

                if argtype == objc_id:
                    # Convert Python objects to Core Foundation objects
                    arg = from_value(arg)
                elif isinstance(arg, collections.abc.Iterable) and issubclass(argtype, (Structure, Array)):
                    arg = compound_value_for_sequence(arg, argtype)

                if argtype == objc_block:
                    raise NotImplementedError('Passing blocks to objc is not supported yet')

                converted_args.append(arg)
        else:
            converted_args = args

        try:
            result = f(receiver, self.selector, *converted_args)
        except ArgumentError as error:
            # Add more useful info to argument error exceptions, then reraise.
            error.args = (error.args[0] + ' (selector = {self.name}, argtypes = {self.argtypes}, encoding = {self.encoding})'.format(self=self),)
            raise
        else:
            if not convert_result:
                return result

            # Convert result to python type if it is a instance or class pointer.
            from .core_foundation import to_value
            if self.restype == objc_id:
                result = to_value(ObjCInstance(result))
            elif self.restype == Class:
                result = ObjCClass(result)
            return result

######################################################################

class ObjCPartialMethod(object):
    _sentinel = object()

    def __init__(self, name_start):
        super().__init__()

        self.name_start = name_start
        self.methods = {}

    def __repr__(self):
        return "{cls.__module__}.{cls.__qualname__}({self.name_start!r})".format(cls=type(self), self=self)

    def __call__(self, receiver, first_arg=_sentinel, **kwargs):
        if first_arg is ObjCPartialMethod._sentinel:
            if kwargs:
                raise TypeError("Missing first (positional) argument")

            args = []
            rest = frozenset()
        else:
            args = [first_arg]
            # Add "" to rest to indicate that the method takes arguments
            rest = frozenset(kwargs) | frozenset(("",))

        try:
            meth, order = self.methods[rest]
        except KeyError:
            raise ValueError("No method with selector parts {}".format(set(kwargs)))

        meth = ObjCMethod(meth)
        args += [kwargs[name] for name in order]
        return meth(receiver, *args)

######################################################################

class ObjCBoundMethod(object):
    """This represents an Objective-C method (an IMP) which has been bound
    to some id which will be passed as the first parameter to the method."""

    def __init__(self, method, receiver):
        """Initialize with a method and ObjCInstance or ObjCClass object."""
        self.method = method
        if type(receiver) == Class:
            self.receiver = cast(receiver, objc_id)
        else:
            self.receiver = receiver

    def __repr__(self):
        return '<ObjCBoundMethod %s (%s)>' % (self.method.name, self.receiver)

    def __call__(self, *args, **kwargs):
        """Call the method with the given arguments."""
        return self.method(self.receiver, *args, **kwargs)

######################################################################


def cache_method(cls, name):
    """Returns a python representation of the named instance method,
    either by looking it up in the cached list of methods or by searching
    for and creating a new method object."""

    supercls = cls
    objc_method = None
    while supercls is not None:
        # Load the class's methods if we haven't done so yet.
        if supercls.methods_ptr is None:
            supercls._reload_methods()

        try:
            objc_method = supercls.instance_methods[name]
            break
        except KeyError:
            pass

        try:
            objc_method = ObjCMethod(supercls.instance_method_ptrs[name])
            break
        except KeyError:
            pass

        supercls = supercls.superclass

    if objc_method is None:
        return None
    else:
        cls.instance_methods[name] = objc_method
        return objc_method


def cache_property_methods(cls, name):
    """Return the accessor and mutator for the named property.
    """
    if name.endswith('_'):
        # If the requested name ends with _, that's a marker that we're
        # dealing with a method call, not a property, so we can shortcut
        # the process.
        methods = None
    else:
        # Check 1: Does the class respond to the property?
        responds = objc.class_getProperty(cls, name.encode('utf-8'))

        # Check 2: Does the class have an instance method to retrieve the given name
        accessor = cache_method(cls, name)

        # Check 3: Is there a setName: method to set the property with the given name
        mutator = cache_method(cls, 'set' + name[0].title() + name[1:] + ':')

        # If the class responds as a property, or it has both an accessor *and*
        # and mutator, then treat it as a property in Python.
        if responds or (accessor and mutator) or (name in cls.forced_properties):
            methods = (accessor, mutator)
        else:
            methods = None
    return methods


def cache_property_accessor(cls, name):
    """Returns a python representation of an accessor for the named
    property. Existence of a property is done by looking for the write
    selector (set<Name>:).
    """
    try:
        methods = cls.instance_properties[name]
    except KeyError:
        methods = cache_property_methods(cls, name)
        cls.instance_properties[name] = methods
    if methods:
        return methods[0]
    return None


def cache_property_mutator(cls, name):
    """Returns a python representation of an accessor for the named
    property. Existence of a property is done by looking for the write
    selector (set<Name>:).
    """
    try:
        methods = cls.instance_properties[name]
    except KeyError:
        methods = cache_property_methods(cls, name)
        cls.instance_properties[name] = methods
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
        elif e == objc_block:
            new_args.append(to_value(ObjCInstance(a)))
        else:
            new_args.append(a)
    return new_args


def objc_method(f):
    encoding = encoding_from_annotation(f)

    def _objc_method(receiver, objc_cmd, *args):
        from .core_foundation import at
        py_self = ObjCInstance(receiver)
        args = convert_method_arguments(encoding, args)
        result = f(py_self, *args)
        if isinstance(result, ObjCClass):
            result = result.ptr.value
        elif isinstance(result, ObjCInstance):
            result = result.ptr.value
        elif isinstance(result, str):
            result = at(result).ptr.value
        return result

    def register(cls, attr):
        name = attr.replace("_", ":")
        cls.imp_keep_alive_table[name] = add_method(cls, name, _objc_method, encoding)

    _objc_method.register = register

    return _objc_method


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
        elif isinstance(result, str):
            result = at(result).ptr.value
        return result

    def register(cls, attr):
        name = attr.replace("_", ":")
        cls.imp_keep_alive_table[name] = add_method(cls.objc_class, name, _objc_classmethod, encoding)

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

    def pre_register(self, ptr, attr):
        return add_ivar(ptr, attr, self.vartype)


class objc_property(object):
    def __init__(self):
        pass

    def register(self, cls, attr):
        def getter(_self) -> ObjCInstance:
            return getattr(_self, '_' + attr, None)

        def setter(_self, new):
            if not hasattr(_self, '_' + attr):
                setattr(_self, '_' + attr, None)
            if getattr(_self, '_' + attr) is None:
                setattr(_self, '_' + attr, new)
                if new is not None:
                    getattr(_self, '_' + attr).retain()
            else:
                if not getattr(_self, '_' + attr).isEqualTo_(new):
                    getattr(_self, '_' + attr).release()
                    setattr(_self, '_' + attr, new)
                    if new is not None:
                        getattr(_self, '_' + attr).retain()

        getter_encoding = encoding_from_annotation(getter)
        setter_encoding = encoding_from_annotation(setter)

        def _objc_getter(objc_self, objc_cmd, *args):
            from .core_foundation import at
            py_self = ObjCInstance(objc_self)
            args = convert_method_arguments(getter_encoding, args)
            result = getter(py_self, *args)
            if isinstance(result, ObjCClass):
                result = result.ptr.value
            elif isinstance(result, ObjCInstance):
                result = result.ptr.value
            elif isinstance(result, str):
                result = at(result).ptr.value
            return result

        def _objc_setter(objc_self, objc_cmd, *args):
            from .core_foundation import at
            py_self = ObjCInstance(objc_self)
            args = convert_method_arguments(setter_encoding, args)
            result = setter(py_self, *args)
            if isinstance(result, ObjCClass):
                result = result.ptr.value
            elif isinstance(result, ObjCInstance):
                result = result.ptr.value
            elif isinstance(result, str):
                result = at(result).ptr.value
            return result

        setter_name = 'set' + attr[0].upper() + attr[1:] + ':'

        cls.imp_keep_alive_table[attr] = add_method(cls.ptr, attr, _objc_getter, getter_encoding)
        cls.imp_keep_alive_table[setter_name] = add_method(cls.ptr, setter_name, _objc_setter, setter_encoding)


def objc_rawmethod(f):
    encoding = encoding_from_annotation(f, offset=2)

    def register(cls, attr):
        name = attr.replace("_", ":")
        cls.imp_keep_alive_table[name] = add_method(cls, name, f, encoding)
    f.register = register
    return f

######################################################################

class ObjCInstance(object):
    """Python wrapper for an Objective-C instance."""

    _cached_objects = {}

    @property
    def objc_class(self):
        return ObjCClass(objc.object_getClass(self))

    @classmethod
    def _select_mixin(cls, object_ptr):
        nsmutablearray = objc.objc_getClass(b'NSMutableArray')
        if send_message(object_ptr, 'isKindOfClass:', nsmutablearray):
            return ObjCMutableListInstance

        nsarray = objc.objc_getClass(b'NSArray')
        if send_message(object_ptr, 'isKindOfClass:', nsarray):
            return ObjCListInstance

        nsmutabledictionary = objc.objc_getClass(b'NSMutableDictionary')
        if send_message(object_ptr, 'isKindOfClass:', nsmutabledictionary):
            return ObjCMutableDictInstance

        nsdictionary = objc.objc_getClass(b'NSDictionary')
        if send_message(object_ptr, 'isKindOfClass:', nsdictionary):
            return ObjCDictInstance

        return cls

    def __new__(cls, object_ptr, _name=None, _bases=None, _ns=None):
        """Create a new ObjCInstance or return a previously created one
        for the given object_ptr which should be an Objective-C id."""
        # Make sure that object_ptr is wrapped in an objc_id.
        is_block = isinstance(object_ptr, objc_block)
        if not isinstance(object_ptr, objc_id):
            object_ptr = cast(object_ptr, objc_id)

        # If given a nil pointer, return None.
        if not object_ptr.value:
            return None

        # Check if we've already created a Python ObjCInstance for this
        # object_ptr id and if so, then return it.  A single ObjCInstance will
        # be created for any object pointer when it is first encountered.
        # This same ObjCInstance will then persist until the object is
        # deallocated.
        if object_ptr.value in cls._cached_objects:
            return cls._cached_objects[object_ptr.value]

        # If the given pointer points to a class, return an ObjCClass instead (if we're not already creating one).
        if not issubclass(cls, ObjCClass) and objc.object_isClass(object_ptr):
            return ObjCClass(object_ptr)

        # Otherwise, create a new ObjCInstance.
        if issubclass(cls, type):
            # Special case for ObjCClass to pass on the class name, bases and namespace to the type constructor.
            self = super().__new__(cls, _name, _bases, _ns)
        else:
            if is_block:
                cls = ObjCBlockInstance
            else:
                cls = cls._select_mixin(object_ptr)
            self = super().__new__(cls)
        super(ObjCInstance, type(self)).__setattr__(self, "ptr", object_ptr)
        super(ObjCInstance, type(self)).__setattr__(self, "_as_parameter_", object_ptr)
        if is_block:
            super(ObjCInstance, type(self)).__setattr__(self, "block", ObjCBlock(object_ptr))
        # Store new object in the dictionary of cached objects, keyed
        # by the (integer) memory address pointed to by the object_ptr.
        cls._cached_objects[object_ptr.value] = self

        # Classes are never deallocated, so they don't need a DeallocationObserver.
        # This is also necessary to make the definition of DeallocationObserver work - otherwise creating the ObjCClass for DeallocationObserver would try to instantiate a DeallocationObserver itself.
        if not objc.object_isClass(object_ptr):
            # Create a DeallocationObserver and associate it with this object.
            # When the Objective-C object is deallocated, the observer will remove
            # the ObjCInstance corresponding to the object from the cached objects
            # dictionary, effectively destroying the ObjCInstance.
            observer = send_message(send_message('DeallocationObserver', 'alloc', restype=objc_id, argtypes=[]), 'initWithObject:', self, restype=objc_id, argtypes=[objc_id])
            objc.objc_setAssociatedObject(self, observer, observer, 0x301)

            # The observer is retained by the object we associate it to.  We release
            # the observer now so that it will be deallocated when the associated
            # object is deallocated.
            send_message(observer, 'release')

        return self

    def __str__(self):
        from . import core_foundation
        if core_foundation.is_str(self):
            return core_foundation.to_str(self)
        else:
            return self.debugDescription

    def __repr__(self):
        return "<%s.%s %#x: %s at %#x: %s>" % (
            type(self).__module__,
            type(self).__qualname__,
            id(self),
            self.objc_class.name,
            self.ptr.value,
            self.debugDescription,
        )

    def __getattr__(self, name):
        """Returns a callable method object with the given name."""
        # Search for named instance method in the class object and if it
        # exists, return callable object with self as hidden argument.
        # Note: you should give self and not self.ptr as a parameter to
        # ObjCBoundMethod, so that it will be able to keep the ObjCInstance
        # alive for chained calls like MyClass.alloc().init() where the
        # object created by alloc() is not assigned to a variable.

        # If there's a property with this name; return the value directly.
        # If the name ends with _, we can shortcut this step, because it's
        # clear that we're dealing with a method call.
        if not name.endswith('_'):
            method = cache_property_accessor(self.objc_class, name)
            if method:
                return ObjCBoundMethod(method, self)()

        # See if there's a partial method starting with the given name,
        # either on self's class or any of the superclasses.
        cls = self.objc_class
        while cls is not None:
            # Load the class's methods if we haven't done so yet.
            if cls.methods_ptr is None:
                cls._reload_methods()

            try:
                method = cls.partial_methods[name]
                break
            except KeyError:
                cls = cls.superclass
        else:
            method = None

        if method is not None:
            # If the partial method can only resolve to one method that takes no arguments,
            # return that method directly, instead of a mostly useless partial method.
            if set(method.methods) == {frozenset()}:
                method, _ = method.methods[frozenset()]
                method = ObjCMethod(method)

            return ObjCBoundMethod(method, self)

        # See if there's a method whose full name matches the given name.
        method = cache_method(self.objc_class, name.replace("_", ":"))
        if method:
            return ObjCBoundMethod(method, self)
        else:
            raise AttributeError('%s.%s %s has no attribute %s' % (type(self).__module__, type(self).__qualname__, self.objc_class.name, name))

    def __setattr__(self, name, value):
        if name in self.__dict__:
            # For attributes already in __dict__, use the default __setattr__.
            super(ObjCInstance, type(self)).__setattr__(self, name, value)
        else:
            method = cache_property_mutator(self.objc_class, name)
            if method:
                # Convert enums to their underlying values.
                if isinstance(value, Enum):
                    value = value.value
                ObjCBoundMethod(method, self)(value)
            else:
                super(ObjCInstance, type(self)).__setattr__(self, name, value)


class ObjCListInstance(ObjCInstance):
    def __getitem__(self, item):
        if isinstance(item, slice):
            start = item.start or 0
            if start < 0:
                start = len(self) + start
            stop = item.stop or len(self)
            if stop < 0:
                stop = len(self) + stop
            step = item.step or 1
            return [self.objectAtIndex(x) for x in range(start, stop, step)]

        if item < 0:
            item = len(self) + item
        if item >= len(self):
            raise IndexError('list index out of range')

        return self.objectAtIndex(item)

    def __len__(self):
        return send_message(self.ptr, 'count').value or 0

    def __iter__(self):
        for i in range(len(self)):
            yield self.objectAtIndex(i)

    def __contains__(self, item):
        return self.containsObject_(item)

    def __eq__(self, other):
        for a, b in zip(self, other):
            if a != b:
                return False
        return True

    def index(self, value):
        idx = self.indexOfObject_(value)
        if idx == NSNotFound:
            raise ValueError('%r is not in list' % value)
        return idx

    def count(self, value):
        return len([x for x in self if x == value])

    def copy(self):
        return self.objc_class.arrayWithArray_(self)

class ObjCMutableListInstance(ObjCListInstance):
    def _slice_to_range_params(self, s):
        step = s.step or 1
        start = s.start
        stop = s.stop

        if start is not None and start < 0:
            start = len(self) + start
        if stop is not None and stop < 0:
            stop = len(self) + stop

        if step < 0:
            start = start or (len(self) - 1)
            stop = stop or -1
        else:
            start = start or 0
            stop = stop or len(self)

        return start, stop, step

    def __setitem__(self, item, value):
        if isinstance(item, slice):
            start, stop, step = self._slice_to_range_params(item)

            if step == 1:
                for idx in range(start, stop):
                    self.removeObjectAtIndex_(start)
                for item in reversed(value):
                    self.insertObject_atIndex_(item, start)
            else:
                indexes = range(start, stop, step)
                if len(value) != len(indexes):
                    raise ValueError('attempt to assign sequence of size %d '
                                     'to extended slice of size %d' %
                                     (len(value), len(indexes)))
                for idx, value in zip(indexes, value):
                    self.replaceObjectAtIndex_withObject_(idx, value)

            return

        if item < 0:
            item = len(self) + item
        if item >= len(self):
            raise IndexError('list assignment index out of range')

        self.replaceObjectAtIndex_withObject_(item, value)

    def __delitem__(self, item):
        if isinstance(item, slice):
            indexes = list(range(*self._slice_to_range_params(item)))
            indexes.sort(reverse=True)
            for index in indexes:
                self.removeObjectAtIndex(index)
            return

        if item < 0:
            item = len(self) + item
        if item >= len(self):
            raise IndexError('list assignment index out of range')

        self.removeObjectAtIndex_(item)

    def append(self, value):
        self.addObject_(value)

    def extend(self, values):
        for value in values:
            self.addObject_(value)

    def clear(self):
        self.removeAllObjects()

    def pop(self, item=-1):
        value = self[item]
        del self[item]
        return value

    def remove(self, value):
        del self[self.index(value)]

    def reverse(self):
        self.removeAllObjects  # this is a test
        new_contents = self.reverseObjectEnumerator().allObjects()
        self.removeAllObjects()
        self.addObjectsFromArray_(new_contents)

    def insert(self, idx, value):
        self.insertObject_atIndex_(value, idx)

class ObjCDictInstance(ObjCInstance):
    def __getitem__(self, item):
        v = self.objectForKey_(item)
        if v is None:
            raise KeyError(item)
        return v

    def __len__(self):
        return self.count

    def __iter__(self):
        for key in self.allKeys():
            yield key

    def __contains__(self, item):
        return self.objectForKey_(item) is not None

    def __eq__(self, other):
        if self.keys() != other.keys():
            return False

        for k in self:
            if self[k] != other[k]:
                return False

        return True

    def get(self, item, default=None):
        v = self.objectForKey_(item)
        if v is None:
            return default
        return v

    def keys(self):
        return self.allKeys()

    def values(self):
        return self.allValues()

    def items(self):
        for key in self.allKeys():
            yield key, self.objectForKey_(key)

    def copy(self):
        return self.objc_class.dictionaryWithDictionary_(self)


class ObjCMutableDictInstance(ObjCDictInstance):
    no_pop_default = object()

    def __setitem__(self, item, value):
        self.setObject_forKey_(value, item)

    def __delitem__(self, item):
        if item not in self:
            raise KeyError(item)

        self.removeObjectForKey_(item)

    def clear(self):
        self.removeAllObjects()

    def pop(self, item, default=no_pop_default):
        if item not in self:
            if default is not self.no_pop_default:
                return default
            else:
                raise KeyError(item)

        value = self.objectForKey_(item)
        self.removeObjectForKey_(item)
        return value

    def popitem(self):
        key = self.allKeys().firstObject()
        value = self.objectForKey_(key)
        self.removeObjectForKey_(key)
        return (key, value)

    def setdefault(self, key, default=None):
        value = self.objectForKey_(key)
        if value is None:
            value = default
        if value is not None:
            self.setObject_forKey_(default, key)
        return value

    def update(self, new=None, **kwargs):
        if new is None:
            new = kwargs
        else:
            new = dict(new)

        for k, v in new.items():
            self.setObject_forKey_(v, k)

# The inheritance order is important here.
# type must come after ObjCInstance, so super() refers to ObjCInstance.
# This allows the ObjCInstance constructor to receive the class pointer
# as well as the name, bases, attrs arguments.
# The other way around this would not be possible, because then
# the type constructor would be called before ObjCInstance's, and there
# would be no opportunity to pass extra arguments.
class ObjCClass(ObjCInstance, type):
    """Python wrapper for an Objective-C class."""

    @property
    def superclass(self):
        super_ptr = objc.class_getSuperclass(self)
        if super_ptr.value is None:
            return None
        else:
            return ObjCClass(super_ptr)

    def __new__(cls, *args, **kwargs):
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

            if isinstance(class_name_or_ptr, (bytes, str)):
                name = ensure_bytes(class_name_or_ptr)
                ptr = get_class(name)
                if ptr.value is None:
                    raise NameError("ObjC Class '%s' couldn't be found." % class_name_or_ptr)
            else:
                ptr = cast(class_name_or_ptr, Class)
                if ptr.value is None:
                    raise ValueError("Cannot create ObjCClass from nil pointer")
                elif not objc.object_isClass(ptr):
                    raise ValueError("Pointer {} ({:#x}) does not refer to a class".format(ptr, ptr.value))
                name = objc.class_getName(ptr)
                # "nil" is an ObjC answer confirming the ptr didn't work.
                if name == b'nil':
                    raise RuntimeError("Couldn't create ObjC class for pointer '%s'." % class_name_or_ptr)
                if not issubclass(cls, ObjCMetaClass) and objc.class_isMetaClass(ptr):
                    return ObjCMetaClass(ptr)

        else:
            name, bases, attrs = args
            name = ensure_bytes(name)
            if not isinstance(bases[0], ObjCClass):
                raise RuntimeError("Base class isn't an ObjCClass.")

            ptr = get_class(name)
            if ptr.value is None:
                # Create the ObjC class description
                ptr = objc.objc_allocateClassPair(bases[0].ptr, name, 0)
                if ptr is None:
                    raise RuntimeError("Class pair allocation failed")

                # Pre-Register all the instance variables
                for attr, obj in attrs.items():
                    if hasattr(obj, "pre_register"):
                        obj.pre_register(ptr, attr)

                # Register the ObjC class
                objc.objc_registerClassPair(ptr)
            else:
                raise RuntimeError("ObjC runtime already contains a registered class named '%s'." % name.decode('utf-8'))

        objc_class_name = name.decode('utf-8')

        # Create the class object. If there is already a cached instance for ptr,
        # it is returned and the additional arguments are ignored.
        # Logically this can only happen when creating an ObjCClass from an existing
        # name or pointer, not when creating a new class.
        # If there is no cached instance for ptr, a new one is created and cached.
        self = super().__new__(cls, ptr, objc_class_name, (ObjCInstance,), {
            '_class_inited': False,
            'name': objc_class_name,
            'methods_ptr_count': c_uint(0),
            'methods_ptr': None,
            # Mapping of name -> method pointer
            'instance_method_ptrs': {},
            # Mapping of name -> instance method
            'instance_methods': {},
            # Mapping of name -> (accessor method, mutator method)
            'instance_properties': {},
            # Explicitly declared properties
            'forced_properties': set(),
            # Mapping of first selector part -> ObjCPartialMethod instances
            'partial_methods': {},
            # Mapping of name -> CFUNCTYPE callback function
            # This only contains the IMPs of methods created in Python,
            # which need to be kept from being garbage-collected.
            # It does not contain any other methods, do not use it for calling methods.
            'imp_keep_alive_table': {},
        })

        if not self._class_inited:
            self._class_inited = True

            # Register all the methods, class methods, etc
            registered_something = False
            for attr, obj in attrs.items():
                if hasattr(obj, "register"):
                    registered_something = True
                    obj.register(self, attr)

            # If anything was registered, reload the methods of this class (and the metaclass, because there may be new class methods).
            if registered_something:
                self._reload_methods()
                self.objc_class._reload_methods()

        return self

    def declare_property(self, name):
        self.forced_properties.add(name)

    def declare_class_property(self, name):
        self.objc_class.forced_properties.add(name)

    def __repr__(self):
        return "<%s.%s: %s at %#x>" % (
            type(self).__module__,
            type(self).__qualname__,
            self.name,
            self.ptr.value,
        )

    def __del__(self):
        c.free(self.methods_ptr)

    def _reload_methods(self):
        old_methods_ptr = self.methods_ptr
        self.methods_ptr = objc.class_copyMethodList(self, byref(self.methods_ptr_count))
        # old_methods_ptr may be None, but free(NULL) is a no-op, so that's fine.
        c.free(old_methods_ptr)

        for i in range(self.methods_ptr_count.value):
            method = self.methods_ptr[i]
            name = objc.method_getName(method).name.decode("utf-8")
            self.instance_method_ptrs[name] = method

            first, *rest = name.split(":")
            # Selectors end in a colon iff the method takes arguments.
            # Because of this, rest must either be empty (method takes no arguments) or the last element must be an empty string (method takes arguments).
            assert not rest or rest[-1] == ""

            try:
                partial = self.partial_methods[first]
            except KeyError:
                partial = self.partial_methods[first] = ObjCPartialMethod(first)

            # order is rest without the dummy "" part
            order = rest[:-1]
            partial.methods[frozenset(rest)] = (method, order)


class ObjCMetaClass(ObjCClass):
    """Python wrapper for an Objective-C metaclass."""

    def __new__(cls, name_or_ptr):
        if isinstance(name_or_ptr, (bytes, str)):
            name = ensure_bytes(name_or_ptr)
            ptr = objc.objc_getMetaClass(name)
            if ptr.value is None:
                raise NameError("Objective-C metaclass {} not found".format(name))
        else:
            ptr = cast(name_or_ptr, Class)
            if ptr.value is None:
                raise ValueError("Cannot create ObjCMetaClass for nil pointer")
            elif not objc.object_isClass(ptr) or not objc.class_isMetaClass(ptr):
                raise ValueError("Pointer {} ({:#x}) does not refer to a metaclass".format(ptr, ptr.value))

        return super().__new__(cls, ptr)

register_ctype_for_type(ObjCInstance, objc_id)
register_ctype_for_type(ObjCClass, Class)


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

# Try to reuse an existing DeallocationObserver class.
# This allows reloading the module without having to restart
# the interpreter, although any changes to DeallocationObserver
# itself are only applied after a restart of course.
try:
    DeallocationObserver = ObjCClass("DeallocationObserver")
except NameError:
    class DeallocationObserver(NSObject):

        observed_object = objc_ivar(objc_id)

        @objc_rawmethod
        def initWithObject_(self, cmd, anObject):
            self = send_super(self, 'init')
            self = self.value
            set_instance_variable(self, 'observed_object', anObject, objc_id)
            return self

        @objc_rawmethod
        def dealloc(self, cmd) -> None:
            anObject = get_instance_variable(self, 'observed_object', objc_id)
            ObjCInstance._cached_objects.pop(anObject, None)
            send_super(self, 'dealloc')

        @objc_rawmethod
        def finalize(self, cmd) -> None:
            # Called instead of dealloc if using garbage collection.
            # (which would have to be explicitly started with
            # objc_startCollectorThread(), so probably not too much reason
            # to have this here, but I guess it can't hurt.)
            anObject = get_instance_variable(self, 'observed_object', objc_id)
            ObjCInstance._cached_objects.pop(anObject, None)
            send_super(self, 'finalize')


class ObjCBlockStruct(Structure):
    _fields_ = [
        ('isa', c_void_p),
        ('flags', c_int),
        ('reserved', c_int),
        ('invoke', CFUNCTYPE(c_void_p, c_void_p)),
        ('descriptor', c_void_p),
    ]


def create_block_descriptor_struct(has_helpers, has_signature):
    descriptor_fields = [
        ('reserved', c_ulong),
        ('size', c_ulong),
    ]
    if has_helpers:
        descriptor_fields.extend([
            ('copy_helper', CFUNCTYPE(c_void_p, c_void_p, c_void_p)),
            ('dispose_helper', CFUNCTYPE(c_void_p, c_void_p)),
        ])
    if has_signature:
        descriptor_fields.extend([
            ('signature', c_char_p),
        ])
    return type(
        'ObjCBlockDescriptor',
        (Structure, ),
        {'_fields_': descriptor_fields}
    )


def cast_block_descriptor(block):
    descriptor_struct = create_block_descriptor_struct(block.has_helpers, block.has_signature)
    return cast(block.struct.contents.descriptor, POINTER(descriptor_struct))


AUTO = object()


class ObjCBlock:
    def __init__(self, pointer, return_type=AUTO, *arg_types):
        if isinstance(pointer, ObjCInstance):
            pointer = pointer.ptr
        self.pointer = pointer
        self.struct = cast(self.pointer, POINTER(ObjCBlockStruct))
        self.has_helpers = self.struct.contents.flags & (1<<25)
        self.has_signature = self.struct.contents.flags & (1<<30)
        self.descriptor = cast_block_descriptor(self)
        self.signature = self.descriptor.contents.signature if self.has_signature else None
        if return_type is AUTO:
            if arg_types:
                raise ValueError('Cannot use arg_types with return_type AUTO')
            if not self.has_signature:
                raise ValueError('Cannot use AUTO types for blocks without signatures')
            return_type, *arg_types = ctypes_for_method_encoding(self.signature)
        self.struct.contents.invoke.restype = ctype_for_type(return_type)
        self.struct.contents.invoke.argtypes = (objc_id, ) + tuple(ctype_for_type(arg_type) for arg_type in arg_types)

    def __repr__(self):
        representation = '<ObjCBlock@{}'.format(hex(addressof(self.pointer)))
        if self.has_helpers:
            representation += ',has_helpers'
        if self.has_signature:
            representation += ',has_signature:' + self.signature
        representation += '>'
        return representation

    def __call__(self, *args):
        return self.struct.contents.invoke(self.pointer, *args)


class ObjCBlockInstance(ObjCInstance):
    def __call__(self, *args):
        return self.block(*args)
