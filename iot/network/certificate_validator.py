import OpenSSL.crypto
import tempfile


def validate(cert_content, cert_password):

    if cert_content is None or len(cert_content) == 0:
        return True

    fp = tempfile.NamedTemporaryFile()
    fp.write(bytes(cert_content, 'utf-8'))
    fp.seek(0)

    try:
        if cert_password is not None and len(cert_password) > 0:
            OpenSSL.crypto.load_privatekey(OpenSSL.crypto.FILETYPE_PEM, fp.read(), cert_password.encode("utf-8"))
        else:
            OpenSSL.crypto.load_privatekey(OpenSSL.crypto.FILETYPE_PEM, fp.read(), "")
        return True
    except:
        fp.close()
        return False
