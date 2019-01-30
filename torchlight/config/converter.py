import pyhocon


def compact_keys(config: pyhocon.ConfigTree):
    key_stack = []

    def walk(tree: pyhocon.ConfigTree):
        for key, value in tree.items():
            key_stack.append(key)
            if isinstance(value, pyhocon.ConfigTree):
                if len(value) == 0:
                    key_str = '.'.join(key_stack)
                    yield key_str
                else:
                    yield from walk(value)
            else:
                key_str = '.'.join(key_stack)
                yield key_str
            key_stack.pop()

    yield from walk(config)
