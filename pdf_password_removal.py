import os
from file_utils import *

import PyPDF4 as pp4


root_dir, passwords = read_json()


def get_files(directory=root_dir) -> str:

    if os.path.exists(directory):

        for f in os.listdir(directory):
            yield os.path.join(directory, f)


def get_password() -> str:

    for v in passwords:
        yield v


def read_pdf(file_name: str):
    return pp4.PdfFileReader(file_name, strict=False)


def write_pdf(file_name: str, read_pdf_obj: str):
    writer = pp4.PdfFileWriter()
    writer.appendPagesFromReader(read_pdf_obj)

    with open(file_name, "wb") as fp:
        writer.write(fp)

    return file_name


def pdf_rm_pwd() -> bool:

    for f in get_files():

        if f.endswith(".pdf"):

            read_obj = read_pdf(f)

            if read_obj.isEncrypted:

                for password in get_password():

                    if read_obj.decrypt(password.lower()) in (1, 2):

                        print(write_pdf(file_name=f, read_pdf_obj=read_obj))
                        break

                    elif read_obj.decrypt(password.upper()) in (1, 2):

                        print(write_pdf(file_name=f, read_pdf_obj=read_obj))
                        break

    return True


def main():

    return pdf_rm_pwd()


if __name__ == '__main__':

    if main():

        print("Process Completed")
    else:
        print("Process Incompleted")
