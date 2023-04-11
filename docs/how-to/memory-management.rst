===========================================
Memory management for Objective-C instances
===========================================

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

Reference counting in Rubicon Objective-C
-----------------------------------------

You won't have to manage reference counts in Python, Rubicon Objective-C will do
that work for you. It does so by tracking when you gain ownership of an object.
This is the case when you create an Objective-C instance using a method whose
name begins with ``alloc``, ``new``, ``copy``, or ``mutableCopy``. Rubicon
Objective-C will then insert a ``release`` call when the Python variable that
corresponds to the Objective-C instance is deallocated.

An exception to this is when you manually ``retain`` an object. Rubicon
Objective-C will not keep track of such retain calls and you will be
responsible to insert appropriate ``release`` calls yourself.

You will also need to pay attention to reference counting in case of **weak
references**. In Objective-C, creating a **weak reference** means that the
reference count of the object is not incremented and the object will still be
deallocated when no strong references remain. Any weak references to the object
are then set to ``nil``.

Some objects will store references to other objects as a weak reference. Such
properties will be declared in the Apple developer documentation as
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
