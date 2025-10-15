# `rubicon.objc.eventloop`{.interpreted-text role="mod"} --- Integrating native event loops with `asyncio`{.interpreted-text role="mod"} { #rubicon.objc.eventloop-----integrating-native-event-loops-with-asyncio }

::: {.module}
rubicon.objc.eventloop
:::

:::: {.note}
::: {.title}
Note
:::

The documentation for this module is incomplete. You can help by
`contributing to the documentation <../how-to/contribute/docs>`{.interpreted-text
role="doc"}.
::::

::::::: {.autoclass}
EventLoopPolicy

::: {.automethod}
new_event_loop
:::

::: {.automethod}
get_default_loop
:::

::: {.automethod}
get_child_watcher
:::

::: {.automethod}
set_child_watcher
:::
:::::::

::::: {.autoclass}
CocoaLifecycle

::: {.automethod}
start
:::

::: {.automethod}
stop
:::
:::::

::::: {.autoclass}
iOSLifecycle

::: {.automethod}
start
:::

::: {.automethod}
stop
:::
:::::
