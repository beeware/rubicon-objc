===========================================
Memory management for Objective-C instances
===========================================

Reference counting in Objective-C
=================================

Reference counting works differently in Objective-C compared to Python. Python
will automatically track where variables are referenced and free memory when
the reference count drops to zero whereas Objective-C uses explicit reference
counting to manage memory. The methods ``retain``, ``release`` and
``autorelease`` are used to increase and decrease the reference counts as
described in the `Apple developer documentation
<https://developer.apple.com/library/archive/documentation/Cocoa/Conceptual/MemoryMgmt/Articles/MemoryMgmt.html>`__.
When enabling automatic reference counting (ARC), the appropriate calls for
memory management will be inserted for you at compile-time. However, since
Rubicon Objective-C operates at runtime, it cannot make use of ARC.

Reference management in Rubicon
===============================

In most cases, you won't have to manage reference counts in Python, Rubicon
Objective-C will do that work for you. It does so by calling ``retain`` on an
object when Rubicon creates a ``ObjCInstance`` for it on the Python side, and calling
``autorelease`` when the ``ObjCInstance`` is garbage collected in Python. Retaining
the object ensures it is not deallocated while it is still referenced from Python
and releasing it again on ``__del__`` ensures that we do not leak memory.

The only exception to this is when you create an object -- which is always done
through methods starting with "alloc", "new", "copy", or "mutableCopy". Rubicon does
not explicitly retain such objects because we own objects created by us, but Rubicon
does autorelease them when the Python wrapper is garbage collected.

Rubicon Objective-C will not keep track if you additionally manually ``retain`` an
object. You will be responsible to insert appropriate ``release`` or ``autorelease``
calls yourself to prevent leaking memory.

Weak references in Objective-C
------------------------------

You will need to pay attention to reference counting in case of **weak
references**. In Objective-C, as in Python, creating a weak reference means that
the reference count of the object is not incremented and the object will be
deallocated when no strong references remain. Any weak references to the object
are then set to ``nil``.

Some Objective-C objects store references to other objects as a weak reference.
Such properties will be declared in the Apple developer documentation as
"@property(weak)" or "@property(assign)". This is commonly the case for
delegates. For example, in the code below, the ``NSOutlineView`` only stores a
weak reference to the object which is assigned to its delegate property:

.. code-block:: python

    from rubicon.objc import NSObject, ObjCClass
    from rubicon.objc.runtime import load_library

    app_kit = load_library("AppKit")
    NSOutlineView = ObjCClass("NSOutlineView")

    outline_view = NSOutlineView.alloc().init()
    delegate = NSObject.alloc().init()

    outline_view.delegate = delegate

You will need to keep a reference to the Python variable ``delegate`` so that
the corresponding Objective-C instance does not get deallocated.

Reference cycles in Objective-C
-------------------------------

Python has a garbage collector which detects references cycles and frees
objects in such cycles if no other references remain. Cyclical references can
be useful in a number of cases, for instance to refer to a "parent" of an
instance, and Python makes life easier by properly freeing such references. For
example:

.. code-block:: python

    class TreeNode:
        def __init__(self, val):
            self.val = val
            self.parent = None
            self.children = []


    root = TreeNode("/home")

    child = TreeNode("/Documents")
    child.parent = root

    root.children.append(child)

    # This will free both root and child on
    # the next garbage collection cycle:
    del root
    del child


Similar code in Objective-C will lead to memory leaks. This also holds for
Objective-C instances created through Rubicon Objective-C since Python's
garbage collector is unable to detect reference cycles on the Objective-C side.
If you are writing code which would lead to reference cycles, consider storing
objects as weak references instead. The above code would be written as follows
when using Objective-C classes:

.. code-block:: python

    from rubicon.objc import NSObject, NSMutableArray
    from rubicon.objc.api import objc_property, objc_method


    class TreeNode(NSObject):
        val = objc_property()
        children = objc_property()
        parent = objc_property(weak=True)

        @objc_method
        def initWithValue_(self, val):
            self.val = val
            self.children = NSMutableArray.new()
            return self


    root = TreeNode.alloc().initWithValue("/home")

    child = TreeNode.alloc().initWithValue("/Documents")
    child.parent = root

    root.children.addObject(child)

    # This will free both root and child:
    del root
    del child
