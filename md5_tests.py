from md5lib import md5  # Your original class


def to_hex(b: bytes) -> str:
    return ''.join('{:02x}'.format(x) for x in b)


def test_md5_vectors():
    print("== Standard MD5 Test Vectors ==")
    test_vectors = [
        (b"", "d41d8cd98f00b204e9800998ecf8427e"),
        (b"a", "0cc175b9c0f1b6a831c399e269772661"),
        (b"abc", "900150983cd24fb0d6963f7d28e17f72"),
        (b"message digest", "f96b697d7cb7938d525a2f31aaf161d0"),
        (b"abcdefghijklmnopqrstuvwxyz", "c3fcd3d76192e4007dfb496cca67e13b"),
        (b"ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz0123456789",
         "d174ab98d277d9f5a5611c2c9f419d9f"),
        (b"12345678901234567890123456789012345678901234567890123456789012345678901234567890",
         "57edf4a22be3c955ac49da2e2107b67a")
    ]

    for msg, expected in test_vectors:
        h = md5()
        h.update(msg)
        result = to_hex(h.digest())
        assert result == expected, f"FAIL: {msg!r} -> {result} != {expected}"
        print(f"PASS: {msg!r} -> {result}")


def test_md5_1_million_as():
    print("== 1 Million 'a' Test ==")
    h = md5()
    h.update(b"a" * 1000000)
    result = to_hex(h.digest())
    expected = "7707d6ae4e027c70eea2a935c2296f21"
    assert result == expected, f"FAIL: 1M 'a' -> {result} != {expected}"
    print(f"PASS: 1M 'a' -> {result}")


def test_md5_chunked_update():
    print("== Chunked Update Test ==")
    h = md5()
    h.update(b"ab")
    h.update(b"c")
    result = to_hex(h.digest())
    expected = "900150983cd24fb0d6963f7d28e17f72"
    assert result == expected, f"FAIL: chunked update -> {result} != {expected}"
    print(f"PASS: chunked update -> {result}")


def test_md5_binary_input():
    print("== Binary Input Test ==")
    h = md5()
    h.update(b"\x00" * 64)
    result = to_hex(h.digest())
    expected = "3b5d3c7d207e37dceeedd301e35e2e58"
    assert result == expected, f"FAIL: null bytes -> {result} != {expected}"
    print(f"PASS: 64 null bytes -> {result}")


def run_all_tests():
    test_md5_vectors()
    test_md5_1_million_as()  # don't do this on embedded systems!
    test_md5_chunked_update()
    test_md5_binary_input()
    print("✅ All original md5 tests passed.")


if __name__ == "__main__":
    run_all_tests()
