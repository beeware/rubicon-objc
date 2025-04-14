====================================================================================
:mod:`rubicon.objc.eventloop` --- Integrating native event loops with :mod:`asyncio`
====================================================================================

.. module:: rubicon.objc.eventloop

.. note::

    The documentation for this module is incomplete. You can help by
    :doc:`contributing to the documentation <../how-to/contribute/docs>`.

.. autoclass:: EventLoopPolicy

    .. automethod:: new_event_loop
    .. automethod:: get_default_loop
    .. automethod:: get_child_watcher
    .. automethod:: set_child_watcher

.. autoclass:: CocoaLifecycle

    .. automethod:: start
    .. automethod:: stop

.. autoclass:: iOSLifecycle

    .. automethod:: start
    .. automethod:: stop
