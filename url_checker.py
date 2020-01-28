"""Takes a list of DOIs and checks doi.org to see if these return a valid 
HTTP response.  Uses multiprocessing to async the requests and increase speed.
"""


import requests
import sys
import os
import chardet
from tqdm import *
from multiprocessing import Pool, freeze_support
from itertools import repeat


def read_in(filepath, chars=32):
    """
    Reads the first amount of characters in a file to determine encoding, then using that encoding
    to actually read the file with the correct encoding.

    BOMs sometimes make file reading difficult, and this allows the proper encoding of utf-8-sig for files
    with BOMs at their header.

    Args:
        filepath: file where urls/data exists
        chars: amount of characters to read before determining encoding

    Returns: a list of items
    """

    with open(filepath, 'rb') as file:
        print('checking encoding of input file... ')

        # reads 32 characters to determine encoding
        raw = file.read(chars)
        encoding = chardet.detect(raw)['encoding']
        print('encoding is : {}'.format(encoding))

    # read the file again with newly determined encoding
    with open(filepath, encoding=encoding) as file:
        f_lines = [i.strip() for i in file.readlines()]

    return f_lines


def req_head(args):
    """
    Takes a top level url domain and a repeated host and builds a url to be tested.

    Only items that return a 200 code are ignored, everything else is passed through to be
    written to a text file.

    Args:
        args: a two member tuple of a repeated url host and a url suffix

    Returns: a tab delimited string of url suffix, full url, and status code
    """

    r, full_url = args
    req = requests.head(full_url+str(r), allow_redirects=True)
    if req.status_code == 200:
        temp = ''
    else:
        temp = '{0}\t{1}\t{2}'.format(r, req.url, req.status_code)
    return temp


def main():
    # calls the outfile the same name as the input file
    out_file = '{0}_BadUrls.txt'.format(os.path.basename(sys.argv[1]).split('.')[0])

    # args need to be packaged as tuple to pass to imap as single object
    args = zip(URL_LIST, repeat(FULL_URL))

    # this pool can be increased to increase multiprocessing
    with Pool(10) as p:
        res = list(tqdm(p.imap(req_head, args), total=TOTAL))

    with open(out_file, 'w') as out_f:
        for item in res:
            if item:
                out_f.write('{}\n'.format(item))


if __name__ == '__main__':
    # required to make a frozen executable
    freeze_support()

    # Combine URL_DOMAIN and base url to create url for testing
    FULL_URL = 'https://dx.doi.org/'

    # list of domains to test against full url
    URL_LIST = read_in(sys.argv[1])

    # total count of filenames to test
    TOTAL = len(URL_LIST)

    main()


