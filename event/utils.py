import base64
import codecs
import uuid


def generate_random_slug_code(length=8):
    """
    generates random code of given length
    """
    return base64.urlsafe_b64encode(codecs.encode(uuid.uuid4().bytes, "base64").rstrip()).decode()[:length].upper()
