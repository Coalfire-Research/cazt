class AnimalPen:
    # Could change to NoSQL, SQL, in-memory, etc. data store to facilitate different server/servless architectures

    def __init__(self, config):
        self._config = config  # not actually used, just required for future design
        self._internal_data_store = dict()

    def store(self, key, value, overwrite = True):
        if not overwrite and key in self._internal_data_store:
            raise LookupError(f"{key} already exists and overwrite was {overwrite}")

        self._internal_data_store[key] = value

    # Raises KeyError if not found
    def retrieve(self, key):
        return self._internal_data_store[key]

    # key_starts_with is case sensitive
    def list(self, key_starts_with = None):
        if key_starts_with:
            return [ val for key, val in self._internal_data_store.items() if key.startswith(key_starts_with) ]
        else:
            return list(self._internal_data_store.values())

    # Raises KeyError if not found
    def remove(self, key):
        del self._internal_data_store[key]