def _get_headers(header_file='headers'):
    headers = {}
    with open(header_file)as opener:
        header_line = opener.readlines()
        for header in header_line:
            header = ''.join(header.split(' '))
            item = header.strip().split(':')
            print(item)
            headers[item[0]] = item[1]
    return headers