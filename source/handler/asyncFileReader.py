def async_get(filepath):
    with open(filepath, 'rb') as f:
        while True:
            chunk = f.read(1)
            if not chunk:
                f.close()
                raise StopIteration
            yield chunk