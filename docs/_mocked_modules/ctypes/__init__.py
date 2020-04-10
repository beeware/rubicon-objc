"""Bare minimum mock version of ctypes.

This shadows the real ctypes module when building the documentation,
so that :mod:`rubicon.objc` can be imported by Sphinx autodoc even when no Objective-C runtime is available.

This module only emulates enough of ctypes to make the docs build.
Most parts are in no way accurately implemented, and some ctypes features are missing entirely.

Parts of this file are based on the source code of the ctypes module from CPython,
under the terms of Python's license (see ``PYTHON_LICENSE`` for details).
Specifically, the following parts are (partially) based on CPython source code:

* the definitions of the "ctypes primitive types" (the :class:`_SimpleCData` subclasses and their aliases)
* the implementations of :func:`CFUNCTYPE` and :func:`PYFUNCTYPE`
* the implementations of :class:`CDLL`, :class:`PyDLL` and :class:`LibraryLoader`
* the definitions of the :data:`pythonapi`, :data:`cdll` and :data:`pydll` globals
"""

import struct

# We pretend to be a 64-bit system.
_POINTER_SIZE = 8

class ArgumentError(Exception):
    pass

_array_type_cache = {}

class _CDataMeta(type):
    def __mul__(self, count):
        try:
            return _array_type_cache[self, count]
        except KeyError:
            array_type = type(
                "{}_Array_{}".format(self.__name__, str(count)),
                (Array,),
                {'_type_': self, '_length_': count},
            )
            _array_type_cache[self, count] = array_type
            return array_type

class _CData(object, metaclass=_CDataMeta):
    @classmethod
    def from_address(cls, address):
        return cls()
    
    @classmethod
    def in_dll(cls, dll, name):
        return cls()
    
    def _auto_unwrap(self):
        return self

class _SimpleCData(_CData):
    @classmethod
    def _sizeof(cls):
        return struct.calcsize(cls._type_)
    
    def __new__(cls, value=None):
        self = super().__new__(cls)
        self.value = value if value is not None else cls._DEFAULT_VALUE
        return self
    
    def __init__(self, value=None):
        pass
    
    def _auto_unwrap(self):
        if _SimpleCData in type(self).__bases__:
            return self.value
        else:
            return self

class py_object(_SimpleCData):
    _type_ = "O"
    _DEFAULT_VALUE = None
    
    @classmethod
    def _sizeof(cls):
        return _POINTER_SIZE

class c_short(_SimpleCData):
    _DEFAULT_VALUE = 0
    _type_ = "h"

class c_ushort(_SimpleCData):
    _DEFAULT_VALUE = 0
    _type_ = "H"

class c_long(_SimpleCData):
    _DEFAULT_VALUE = 0
    _type_ = "l"

class c_ulong(_SimpleCData):
    _DEFAULT_VALUE = 0
    _type_ = "L"

class c_int(_SimpleCData):
    _DEFAULT_VALUE = 0
    _type_ = "i"

class c_uint(_SimpleCData):
    _DEFAULT_VALUE = 0
    _type_ = "I"

class c_float(_SimpleCData):
    _DEFAULT_VALUE = 0.0
    _type_ = "f"

class c_double(_SimpleCData):
    _DEFAULT_VALUE = 0.0
    _type_ = "d"

class c_longdouble(_SimpleCData):
    _DEFAULT_VALUE = 0.0
    _type_ = "g"

c_longlong = c_long
c_ulonglong = c_ulong

class c_ubyte(_SimpleCData):
    _DEFAULT_VALUE = 0
    _type_ = "B"

class c_byte(_SimpleCData):
    _DEFAULT_VALUE = 0
    _type_ = "b"

class c_char(_SimpleCData):
    _DEFAULT_VALUE = b'\x00'
    _type_ = "c"

class c_char_p(_SimpleCData):
    _DEFAULT_VALUE = None
    _type_ = "z"
    
    @classmethod
    def _sizeof(cls):
        return _POINTER_SIZE

class c_void_p(_SimpleCData):
    _DEFAULT_VALUE = None
    _type_ = "P"
    
    @classmethod
    def _sizeof(cls):
        return _POINTER_SIZE

class c_bool(_SimpleCData):
    _DEFAULT_VALUE = False
    _type_ = "?"

class c_wchar_p(_SimpleCData):
    _DEFAULT_VALUE = None
    _type_ = "Z"
    
    @classmethod
    def _sizeof(cls):
        return _POINTER_SIZE

class c_wchar(_SimpleCData):
    _DEFAULT_VALUE = '\x00'
    _type_ = "u"

c_size_t = c_ulong
c_ssize_t = c_long
c_int8 = c_byte
c_uint8 = c_ubyte
c_int16 = c_short
c_uint16 = c_ushort
c_int32 = c_int
c_uint32 = c_uint
c_int64 = c_long
c_uint64 = c_ulong

class _Pointer(_CData):
    pass

_pointer_type_cache = {None: c_void_p}

def POINTER(ctype):
    try:
        return _pointer_type_cache[ctype]
    except KeyError:
        pointer_ctype = type('LP_{}'.format(ctype.__name__), (_Pointer,), {'_type_': ctype})
        _pointer_type_cache[ctype] = pointer_ctype
        return pointer_ctype

def pointer(cvalue):
    return POINTER(type(cvalue))(cvalue)

class Array(_CData):
    pass

class Structure(_CData):
    def __init__(self, *args):
        super().__init__()
        
        if args:
            for (name, _ctype), value in zip(type(self)._fields_, args):
                setattr(self, name, value)
        else:
            for name, ctype in type(self)._fields_:
                setattr(self, name, ctype()._auto_unwrap())

class Union(_CData):
    pass

class CFuncPtr(_CData):
    _restype_ = None
    _argtypes_ = ()
    
    def __init__(self, src):
        super().__init__()
        
        if isinstance(src, tuple):
            (name, dll) = src
            self._func_name = name
            self._dll_name = dll._name
        else:
            self._func_name = None
            self._dll_name = None
        
        self.restype = type(self)._restype_
        self.argtypes = type(self)._argtypes_
    
    def __call__(self, *args):
        if self.restype is None:
            return None
        else:
            if self._dll_name == 'objc' and self._func_name in {'objc_getClass', 'objc_getProtocol'}:
                res = self.restype(hash(args[0]))
            else:
                res = self.restype()
            return res._auto_unwrap()

_c_functype_cache = {}

def CFUNCTYPE(restype, *argtypes):
    try:
        return _c_functype_cache[(restype, argtypes)]
    except KeyError:
        class CFunctionType(CFuncPtr):
            _argtypes_ = argtypes
            _restype_ = restype
        _c_functype_cache[(restype, argtypes)] = CFunctionType
        return CFunctionType

def PYFUNCTYPE(restype, *argtypes):
    class CFunctionType(CFuncPtr):
        _argtypes_ = argtypes
        _restype_ = restype
    return CFunctionType

def sizeof(ctype):
    return ctype._sizeof()

def addressof(cvalue):
    return id(cvalue)

def alignment(ctype):
    return sizeof(ctype)

def byref(ctype):
    return pointer(ctype)

def cast(cvalue, ctype):
    if isinstance(cvalue, ctype):
        return cvalue
    else:
        return ctype(cvalue.value)

def memmove(dst, src, count):
    raise NotImplementedError('memmove({}, {}, {})'.format(dst, src, count))

def string_at(address):
    return c_char_p(b'')

class CDLL(object):
    _func_restype_ = c_int
    
    def __init__(self, name):
        super().__init__()
        
        self._name = name

        class _FuncPtr(CFuncPtr):
            _restype_ = self._func_restype_
        self._FuncPtr = _FuncPtr

    def __getattr__(self, name):
        if name.startswith('__') and name.endswith('__'):
            raise AttributeError(name)
        func = self.__getitem__(name)
        setattr(self, name, func)
        return func

    def __getitem__(self, name_or_ordinal):
        func = self._FuncPtr((name_or_ordinal, self))
        if not isinstance(name_or_ordinal, int):
            func.__name__ = name_or_ordinal
        return func

class PyDLL(CDLL):
    pass

pythonapi = PyDLL(None)

class LibraryLoader(object):
    def __init__(self, dlltype):
        self._dlltype = dlltype

    def __getattr__(self, name):
        if name[0] == '_':
            raise AttributeError(name)
        dll = self._dlltype(name)
        setattr(self, name, dll)
        return dll

    def __getitem__(self, name):
        return getattr(self, name)

    def LoadLibrary(self, name):
        return self._dlltype(name)

cdll = LibraryLoader(CDLL)
pydll = LibraryLoader(PyDLL)
