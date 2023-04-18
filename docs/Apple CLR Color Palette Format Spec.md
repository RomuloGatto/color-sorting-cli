# Apple CLR Color Palette Format Specification

## The Apple Color Palettes

It is a common practice for some _macOS_ users to use the native _Color Picker_ app to create color palettes. Users can use them for front-end development, graphic design or even slide presentations. The application store them at the `~/Library/Colors` directory as mysterious files ending with `.clr`.

## The Color Palette File

The `.clr` file was first born with the _Application Kit_<sup>[5]</sup>. It was a set of _Objective C_ classes and protocols. The framework was developed for the API of the passed away _NeXTSTEP_ operational system. _NeXT_ created the file for storing the data of `NXColorList` objects. It was a class for maps of `NXColor` objects identified by `NXString` keys. Later, _Sun Microsystems_ made a deal with _NeXT_ to make the _NeXTSTEP_ API multiplataform. The companies named it _OpenStep_<sup>[7]</sup> and substituted all the "NX" for "NS" in the classes names<sup>[4]</sup>.

In 1997, _Apple_ bought _NeXT Computer Inc_<sup>[1]</sup> and used its API on developing its own operational systems. Today it appears at the _macOS_, _IOS_, _iPadOS_, _TVOS_, and all other operational systems of the company<sup>[6]</sup>.

## The Messiah

`NSTypedStream` API is, until now, an _Apple_ systems API luxury. Only _Objective C_ and _Swift_ have tools for reading and writing `NSTypedStream` files as the `.clr`. With no official specification, is even harder to deal with them in case you don't have a _macOS_ available.

At 2022, working with [Adrian Simionov](https://github.com/AdrianSimionov), I accepted the mission of developing a decoder for the file. After about 8 hours I finally got a satisfatory result. Giving the work I had, me and Adrian agreed that the specification of the `.clr` should be documented. This would allow more people to write tools for handle this guys, and help us not to forget it too.

## The Specification

### Header

The `.clr` uses the _little-endian_ byte order. It starts with the `NSTypedStream` file signature represented by the integers:
```
4 11 115 116 114 101 97 109 116 121 112 101 100
```

The integers `115 116 114 101 97 109 116 121 112 101 100` represent the characters `streamtyped` in the ASCII table<sup>[1]</sup>. Next we have a pattern, which meaning I could not identify, but __every__ `.clr` file contains it:
```
129 232 3 132 1 105 1
```

### NSColorList

Now we start seeing the actual file data. The following sequence comes to identify the color counting bytes:
```
132 2 64 105 133
```

For files with an amount of colors equal or less than 127, the next byte will be an integer with the amount of colors. In case there are more than 127 colors, the next byte will be `129`, a special byte to tell the next __two__ bytes will be an integer. This 16-bit integer that follows the `129` will have the value equal to the number of colors in the file.

Now we are going start seeing the actual `NSColorList`. It starts with the sequence:
```
132 2 64 64
```
which express the beginning of the color map. Then we use the following sequence to specify the type of the values of the color map:
```
132 132 132
```
then `7`, which is the number of characters in the class name, followed by the actual name of the class:
```
78 83 67 111 108 111 114 0
```
which represent the characters `NSColor` in the ASCII table<sup>[1]</sup> ending with a null byte (`0`). We also have to tell the superclasses of the object class. We use then
```
132 132
```
then `8`, number of character in the superclass name and
```
78 83 79 98 106 101 99 116 0
```
representing `NSObject` in the ASCII table<sup>[1]</sup> ending with a null byte (`0`). We have then the following sequence:
```
133 132 1 99 1 132 4 102 102 102 102
```
and our first `NSColor` object. `NSTypedStream` represent the color as a sequence of the RGBA values in a scale from 0 to 1 ending with the byte `134`. If the value is exactly 0 or exactly 1, NSTypedStream will represent it as an 8-bit integer. If it is a value between 0 and 1, it will represent it as an IEEE Standard floating point<sup>[3]</sup>, after the byte `131`. The byte `131` tells the next 4 bytes will be a 32-bit floating point.

Now, do you remember the sequence of three `132` bytes we used before? We will need it again! That's because now we are going to specify the data type of the keys. The number of characters in the name of the type is `8`, as the `NSObject` class, and the name of the key's class is:
```
78 83 83 116 114 105 110 103
```
representing `NSString` in the ASCII table<sup>[1]</sup>, this time without the null byte (no idea why). Next we have the following sequence:
```
1 148 132 1 43
```
and the bytes representing the name of the color in the ASCII table<sup>[1]</sup>, after an integer with the length of the name. Our _end of data_ byte `134` goes after the name of the color.

All the next chunks of bytes will follow the pattern:
```
148 132 147 151 1 152 {red} {green} {blue} {alpha} 134 132 150 154 {name of the color} 134
```
until it represents all colors.

## Call To Action

It might be hard working with bytes at first. There are some chunks I still don't understand. But, I'm sure that, on time and with people like me and you working on this, it will change. There will be a future where working the .clr will be trivial. Then, we will be able to go back to our lives with the abstractions letting us to worry only with plain text and GUIs.

## References

1. ANSI. (2022). _INCITS 4-1986 (R2022), Information Systems - Coded Character Sets - 7- Bit Standard Code for Information Interchange (7-Bit ASCII)_.
2. Cupertino, C. (1996). Apple Computer, Inc. Agrees to Acquire NeXT Software Inc.. https://web.archive.org/web/20020208190346/http://product.info.apple.com/pr/press.releases/1997/q1/961220.pr.rel.next.html.
3.  IEEE Computer Society. (2019). Standard for Floating-Point Arithmetic. IEEE Std 754-2019, 1-84. 10.1109/IEEESTD.2019.8766229.
4.  NeXT Computer Inc. (1994). _OpenStep Specification_.
5.  NeXT Computer Inc. (1993). _NeXTSTEP Reference (NeXT Developer's Library)_. Addison-Wesley.
6.  Reisinger, D. (2016, December 20). Steve Jobs Sold NeXT to Apple 20 Years Ago Today. Fortune. https://fortune.com/2016/12/20/apple-next-anniversary/.
7.  Sherman, L. (1994, January). SunSoft adopts NeXT objects. NeXTWORLD, 4(1), 17.
