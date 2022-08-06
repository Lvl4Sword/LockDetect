# LockDetect

Program used to detect if the lockscreen / screensaver is active on Linux, Mac, and Windows.

## How do I use it?:

```py
from lockdetect import locked
locked()
```

The above will either return with ``False``, ``True``, or a ``None`` / reason tuple.
