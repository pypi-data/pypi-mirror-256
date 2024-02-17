class InvalidChecksumError(Exception):
    """MD5 or Blake3 checksum of a local file does not match the one from the server."""

    pass