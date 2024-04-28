========================================
Using and creating Objective-C protocols
========================================

Protocols are used in Objective-C to declare a set of methods and properties
for a class to implement. They have a similar purpose to ABCs (abstract base
classes) in Python.

Looking up a protocol
---------------------

Protocol objects can be looked up using the ``ObjCProtocol`` constructor,
similar to how classes can be looked up using ``ObjCClass``:

.. code-block:: pycon

    >>> NSCopying = ObjCProtocol('NSCopying')
    >>> NSCopying
    <ObjCProtocol: NSCopying>

The ``isinstance`` function can be used to check whether an object conforms to
a protocol:

.. code-block:: pycon

    >>> isinstance(NSObject.new(), NSCopying)
    False
    >>> isinstance(NSArray.array(), NSCopying)
    True

Implementing a protocol
------------------------

When writing a custom Objective-C class, you might want to have it conform to
one or multiple protocols. In Rubicon, this is done by using the ``protocols``
keyword argument in the base class list. For example, if you have a class
``UserAccount`` and want it to conform to ``NSCopyable``, you would write it
like this:

.. code-block:: python

    class UserAccount(NSObject, protocols=[NSCopying]):
        username = objc_property()
        emailAddress = objc_property()

        @objc_method
        def initWithUsername_emailAddress_(self, username, emailAddress):
            self = self.init()
            if self is None:
                return None
            self.username = username
            self.emailAddress = emailAddress
            return self

        # This method is required by NSCopying.
        # The "zone" parameter is obsolete and can be ignored, but must be included for backwards compatibility.
        # This method is not normally used directly. Usually you call the copy method instead,
        # which calls copyWithZone: internally.
        @objc_method
        def copyWithZone_(self, zone):
            return UserAccount.alloc().initWithUsername(self.username, emailAddress=self.emailAddress)

We can now use our class. The ``copy`` method (which uses our implemented
``copyWithZone:`` method) can also be used:

.. code-block:: pycon

    >>> ua = UserAccount.alloc().initWithUsername_emailAddress_(at('person'), at('person@example.com'))
    >>> ua
    <ObjCInstance: UserAccount at 0x106543210: <UserAccount: 0x106543220>>
    >>> ua.copy()
    <ObjCInstance: UserAccount at 0x106543210: <UserAccount: 0x106543220>>

And we can check that the class conforms to the protocol:

.. code-block:: pycon

    >>> isinstance(ua, NSCopying)
    True

Writing custom protocols
------------------------

You can also create custom protocols. This works similarly to creating custom
Objective-C classes:

.. code-block:: python

    class Named(metaclass=ObjCProtocol):
        name = objc_property()

        @objc_method
        def sayName(self):
            ...

There are two notable differences between creating classes and protocols:

1. Protocols do not need to extend exactly one other protocol - they can also
   extend multiple protocols, or none at all. When not extending other
   protocols, as is the case here, we need to explicitly add
   ``metaclass=ObjCProtocol`` to the base class list, to tell Python that this
   is a protocol and not a regular Python class. When extending other
   protocols, Python detects this automatically.
2. Protocol methods do not have a body. Python has no dedicated syntax for
   functions without a body, so we put ``...`` in the body instead. (You could
   technically put code in the body, but this would be misleading and is not
   recommended.)
