import pdf_attachments_download as pad

import pdf_password_removal as ppr


def main():
    try:
        if pad.main():
            ret_val = ppr.main()
    except Exception as e:
        print(e)
        return False
    return ret_val


if __name__ == '__main__':
    if main():
        print('Process Complete')
    else:
        print('Process Incomplete')
