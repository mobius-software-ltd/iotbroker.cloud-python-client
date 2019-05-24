import OpenSSL.crypto
import tempfile
import signal


class TimeoutException(Exception):
    pass


def deadline(timeout, *args):
    """is a the decotator name with the timeout parameter in second"""

    def decorate(f):
        """ the decorator creation """

        def handler(signum, frame):
            """ the handler for the timeout """
            raise TimeoutException()  # when the signal have been handle raise the exception

        def new_f(*args):
            """ the initiation of the handler,
            the lauch of the function and the end of it"""
            signal.signal(signal.SIGALRM, handler)  # link the SIGALRM signal to the handler
            signal.alarm(timeout)  # create an alarm of timeout second
            res = f(*args)  # lauch the decorate function with this parameter
            signal.alarm(0)  # reinitiate the alarm
            return res  # return the return value of the fonction

        new_f.__name__ = f.__name__
        return new_f
    return decorate


def validate(cert_content, cert_password):
    if cert_content is None or len(cert_content) == 0:
        return True

    fp = tempfile.NamedTemporaryFile()
    fp.write(bytes(cert_content, 'utf-8'))
    fp.seek(0)

    thread = None
    try:
        if cert_password is not None and len(cert_password) > 0:
            OpenSSL.crypto.load_privatekey(OpenSSL.crypto.FILETYPE_PEM, fp.read(), cert_password.encode("utf-8"))
        else:
            read_certificate_without_password(fp)
        return True
    except Exception as ex:
        if thread is not None:
            thread.join()
        print("error validating certificate " + str(ex))
        fp.close()
        return False


@deadline(1)
def read_certificate_without_password(fp):
    OpenSSL.crypto.load_privatekey(OpenSSL.crypto.FILETYPE_PEM, fp.read())
