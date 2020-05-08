def chunk(it, size):
    """Creates an iterator from a passed in iterable and builds n-sized tuples as a return."""
    it = iter(it)
    return iter(lambda: tuple(islice(it, size)), ())
