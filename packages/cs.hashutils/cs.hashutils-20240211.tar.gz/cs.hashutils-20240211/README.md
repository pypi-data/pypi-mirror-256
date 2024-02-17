Convenience hashing facilities.

*Latest release 20240211*:
Initial PyPI release: BaseHashCode(bytes) and subclasses for various hash algorithms.

## Class `BaseHashCode(builtins.bytes)`

Base class for hashcodes, subclassed by `SHA1`, `SHA256` et al.

*Method `BaseHashCode.from_buffer(bfr: cs.buffer.CornuCopyBuffer)`*:
Compute hashcode from the contents of the `CornuCopyBuffer` `bfr`.

*Method `BaseHashCode.from_data(bs)`*:
Compute hashcode from the data `bs`.

*Method `BaseHashCode.from_fspath(fspath, **kw)`*:
Compute hashcode from the contents of the file `fspath`.

*Method `BaseHashCode.from_hashbytes(hashbytes)`*:
Factory function returning a `BaseHashCode` object from the hash bytes.

*Method `BaseHashCode.from_hashbytes_hex(hashhex: str)`*:
Factory function returning a `BaseHashCode` object
from the hash bytes hex text.

*Method `BaseHashCode.from_named_hashbytes_hex(hashname, hashhex)`*:
Factory function to return a `HashCode` object
from the hash type name and the hash bytes hex text.

*Method `BaseHashCode.from_prefixed_hashbytes_hex(hashtext: str)`*:
Factory function returning a `BaseHashCode` object
from the hash bytes hex text prefixed by the hashname.
This is the reverse of `__str__`.

*Method `BaseHashCode.hashclass(hashname: str, hashfunc=None, **kw)`*:
Return the class for the hash function named `hashname`.

Parameters:
* `hashname`: the name of the hash function
* `hashfunc`: optional hash function for the class

*Property `BaseHashCode.hashname`*:
The hash code type name, derived from the class name.

*Method `BaseHashCode.hex(self) -> str`*:
Return the hashcode bytes transcribes as a hexadecimal ASCII `str`.

*Method `BaseHashCode.promote(obj)`*:
Promote to a `BaseHashCode` instance.

## Class `MD5(BaseHashCode, builtins.bytes)`

Hash class implementation.

*`MD5.hashfunc`*

## Class `SHA1(BaseHashCode, builtins.bytes)`

Hash class implementation.

*`SHA1.hashfunc`*

## Class `SHA224(BaseHashCode, builtins.bytes)`

Hash class implementation.

*`SHA224.hashfunc`*

## Class `SHA256(BaseHashCode, builtins.bytes)`

Hash class implementation.

*`SHA256.hashfunc`*

## Class `SHA384(BaseHashCode, builtins.bytes)`

Hash class implementation.

*`SHA384.hashfunc`*

## Class `SHA512(BaseHashCode, builtins.bytes)`

Hash class implementation.

*`SHA512.hashfunc`*

# Release Log



*Release 20240211*:
Initial PyPI release: BaseHashCode(bytes) and subclasses for various hash algorithms.
