"""Encrypts a pdf with a supplied password.  Can be used as part of a larger 
operation"""


import pathlib
from pikepdf import Pdf, Encryption


PDF_FILE_IN = ""

def main():
    filename = pathlib.Path(PDF_FILE_IN)
    password = 'password'

    with Pdf.open(filename) as pdf:
        filename_encrypted = filename.parents[0] / f"{filename.stem}_encrypted.pdf"
        pdf.save(filename_encrypted, encryption=Encryption(user=password, owner=password))


if __name__ == '__main__':
    main()
