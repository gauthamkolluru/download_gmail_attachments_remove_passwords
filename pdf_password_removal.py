import os
from file_utils import *

import PyPDF4 as pp4


root_dir, passwords = read_json()


def get_files(directory=root_dir, file_type=".pdf") -> str:

    if os.path.exists(directory):

        for f in os.listdir(directory):

            if f.endswith(file_type):
                yield os.path.join(directory, f)


def get_password() -> str:

    for pwd in passwords:

        if pwd.isnumeric():
            yield pwd
        else:
            for p in (pwd.lower(), pwd.upper()):
                yield p


def read_pdf(file_name: str):
    return pp4.PdfFileReader(file_name, strict=False)


def write_pdf(file_name: str, read_pdf_obj: str):
    writer = pp4.PdfFileWriter()
    writer.appendPagesFromReader(read_pdf_obj)

    with open(file_name, "wb") as fp:
        writer.write(fp)

    return file_name


def is_encrypted(ro):
    return ro.isEncrypted


def pdf_rm_pwd(ro, pwd):
    """
    ro : PyPDF4.PdfFileReader() Object
    pdw : Password
    """
    return ro.decrypt(pwd)


def main():

    decrypted_files = []

    for f in get_files():

        fro = read_pdf(f)

        if is_encrypted(fro):

            for password in get_password():

                try:
                    if pdf_rm_pwd(fro, password) != 0:
                        decrypted_files.append(f)
                        write_pdf(file_name=f, read_pdf_obj=fro)
                        break
                except Exception as e:
                    print(e, f)

    return decrypted_files


if __name__ == '__main__':

    decrypted_files_list = main()

    print(decrypted_files_list)
