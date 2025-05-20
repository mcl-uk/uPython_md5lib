# uPython md5lib
microPython-compatible md5 calculator

Some versions of hashlib have now dropped support for the md5 hashing algorithm, if you need md5 for legacy reasons then here's a micro-python compatible implementation.

It was derived from https://github.com/Utkarsh87/md5-hashing.

But this implementation is of an md5 class compatible with hashlib.md5, complete with .update() and .digest() methods and accepting and generating byte-string data.

Usage example:
<code>from md5lib import md5
myHash = md5(b'your input byte-string')
for i in range(n): myHash.update(b'more bytes')
print(myHash.digest())
</code>
