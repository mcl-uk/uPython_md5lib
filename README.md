# uPython md5lib
microPython-compatible md5 calculator

Some versions of hashlib have now dropped support for the md5 hashing algorithm, if you need md5 for legacy reasons then here's a micro-python compatible implementation.

This implementation is of an md5 class compatible with that of hashlib.md5, complete with .update() and .digest() methods and accepting and generating byte-string data.
Derived from https://github.com/Utkarsh87/md5-hashing.

Usage example:

<code>from md5lib import md5
myHash = md5(b'your input byte-string')
for i in range(100): myHash.update(b'more bytes')
print(myHash.digest())
</code>

Test script:

<code>import os
from md5lib import md5
from hashlib import md5 as refMD5
n = int.from_bytes(os.urandom(1))
w = int.from_bytes(os.urandom(1))
bs = os.urandom(w)
refHash = refMD5(bs)
for i in range(n): refHash.update(bs)
print(refHash.digest())
myHash = md5(bs)
for i in range(n): myHash.update(bs)
print(myHash.digest())
</code>
