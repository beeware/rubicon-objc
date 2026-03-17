from __future__ import annotations

import threading

import pytest

from rubicon.objc import (
    ObjCClass,
    ObjCInstance,
)


def test_wrapper_creation():
    """If 2 threads try to create a wrapper for the same object, only 1 wrapper is
    created (#251)"""
    # Create an ObjC instance, and keep a track of the memory address
    Example = ObjCClass("Example")
    obj = Example.alloc().init()
    ptr = obj.ptr

    # The underlying problem is a race condition, so we need to try a
    # bunch of times to make it happen.
    for _ in range(0, 1000):
        # Flush the ObjC instance cache
        ObjCInstance._cached_objects = {}

        # Keep a log of the Example instances that have been created,
        # keyed by thread_id
        instances = {}

        # A worker method that will create a wrapper object from a (known
        # good) memory address, and track the wrapper object created.
        def work():
            instances[threading.get_ident()] = Example(ptr)  # noqa: B023

        # Run the work method in the main thread, and in a secondary thread;
        # wait for both to complete.
        thread = threading.Thread(target=work)
        thread.start()
        work()
        thread.join()

        # There should be 2 instances
        wrappers = list(instances.values())
        assert len(wrappers) == 2

        # They should be pointing at the same memory address
        assert wrappers[0].ptr == wrappers[1].ptr

        # They should be the same object (i.e., one came from the cache)
        assert id(wrappers[0]) == id(wrappers[1])


def test_method_cache():
    """If 2 threads try to access a method on the same object, there's no race condition
    populating the cache (#252)"""
    # Wrap a class with lots of methods, and create the instance
    Example = ObjCClass("Example")
    obj = Example.alloc().init()

    for _ in range(0, 1000):
        # Manually clear the method/property cache on Example.
        # This returns the attributes set in ObjCClass.__new__
        # to their initial values.
        Example.methods_ptr = None
        Example.instance_method_ptrs = {}
        Example.instance_methods = {}
        Example.instance_properties = {}
        Example.forced_properties = set()
        Example.partial_methods = {}

        # A worker method that invokes a method.
        # This will also populate the method cache.
        def work():
            try:
                obj.mutateIntFieldWithValue(42)
            except AttributeError:
                pytest.fail("method should exist; method cache is corrupt")

        # Run the work method in the main thread, and in a secondary thread;
        # wait for both to complete.
        thread = threading.Thread(target=work)
        thread.start()
        work()
        thread.join()


def test_accessor_cache():
    """If 2 threads try to access an accessor on the same object, there's no race
    condition populating the cache (#252)"""
    # Wrap a class with lots of methods, and create the instance
    Example = ObjCClass("Example")
    obj = Example.alloc().init()

    for _ in range(0, 1000):
        # Manually clear the method/property cache on Example.
        # This returns the attributes set in ObjCClass.__new__
        # to their initial values.
        Example.methods_ptr = None
        Example.instance_method_ptrs = {}
        Example.instance_methods = {}
        Example.instance_properties = {}
        Example.forced_properties = set()
        Example.partial_methods = {}

        # A worker method that accesses a property
        # This will also populate the property cache.
        def work():
            try:
                _ = obj.intField
            except AttributeError:
                pytest.fail("accessor should exist; property cache is corrupt")

        # Run the work method in the main thread, and in a secondary thread;
        # wait for both to complete.
        thread = threading.Thread(target=work)
        thread.start()
        work()
        thread.join()


def test_mutator_cache():
    """If 2 threads try to access a mutator on the same object, there's no race
    condition populating the cache (#252)"""
    # Wrap a class with lots of methods, and create the instance
    Example = ObjCClass("Example")
    obj = Example.alloc().init()

    for _ in range(0, 1000):
        # Manually clear the method/property cache on Example.
        # This returns the attributes set in ObjCClass.__new__
        # to their initial values.
        Example.methods_ptr = None
        Example.instance_method_ptrs = {}
        Example.instance_methods = {}
        Example.instance_properties = {}
        Example.forced_properties = set()
        Example.partial_methods = {}

        # A worker method that mutates a property
        # This will also populate the property cache.
        def work():
            try:
                obj.intField = 42
            except AttributeError:
                pytest.fail("mutator should exist; property cache is corrupt")

        # Run the work method in the main thread, and in a secondary thread;
        # wait for both to complete.
        thread = threading.Thread(target=work)
        thread.start()
        work()
        thread.join()
