# LockDetect

Program used to detect if the lockscreen / screensaver is active on Linux, Mac, and Windows.

## Mac setup:

Requires ``pip install pyobjc-framework-Quartz``

## How do I use it?:

```py
from lockdetect import locked
locked()
```

The above will either return with ``False``, ``True``, or a ``None`` / reason tuple.

You can also do one of the following if you're running Linux and know the exact command from the SCREENSAVERS dictionary:

```py
from lockdetect import locked
locked('FREEDESKTOP_SCREENSAVER')
```

```py
from lockdetect import locked
locked('GNOME_SCREENSAVER')
```

```py
from lockdetect import locked
locked('GNOME3_SCREENSAVER')
```

```py
from lockdetect import locked
locked('KDE_SCREENSAVER')
```
