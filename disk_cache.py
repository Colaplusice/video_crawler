import os


class DiskCache:
    def __init__(self):
        self.base_dir = 'html'

    def __getitem__(self, item):
        try:
            with open(os.path.join(self.base_dir, item), 'r') as opener:
                html = opener.read()
                return html
        except FileNotFoundError:
            return None

    def __setitem__(self, key, value):
        if not key or not value:
            raise KeyError('key 或者 value 是空的')
        if not isinstance(value, str):
            raise TypeError('数据有错误')
        with open(os.path.join(self.base_dir, key), 'w',encoding='utf-8') as opener:
            opener.write(value)
a = DiskCache()
