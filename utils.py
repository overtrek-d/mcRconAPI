import yaml
import os
from cryptography import x509
from cryptography.x509.oid import NameOID
from cryptography.hazmat.primitives import hashes, serialization
from cryptography.hazmat.primitives.asymmetric import rsa
import datetime

def load_config():
    with open('config.yml', 'r') as f:
        return yaml.load(f, Loader=yaml.SafeLoader)

def ensure_self_signed_cert(cert_file="cert.pem", key_file="key.pem"): # check and create cert
    if os.path.exists(cert_file) and os.path.exists(key_file):
        print("self-signed certificate file exists")
        return

    print("self-signed certificate file does not exist")
    key = rsa.generate_private_key(public_exponent=65537, key_size=2048)

    subject = x509.Name([x509.NameAttribute(NameOID.COMMON_NAME, "localhost")])
    cert = (
        x509.CertificateBuilder()
        .subject_name(subject)
        .issuer_name(subject)
        .public_key(key.public_key())
        .serial_number(x509.random_serial_number())
        .not_valid_before(datetime.datetime.utcnow())
        .not_valid_after(datetime.datetime.utcnow() + datetime.timedelta(days=365))
        .sign(key, hashes.SHA256())
    )

    with open(cert_file, "wb") as cert_f:
        cert_f.write(cert.public_bytes(serialization.Encoding.PEM))

    with open(key_file, "wb") as key_f:
        key_f.write(
            key.private_bytes(
                encoding=serialization.Encoding.PEM,
                format=serialization.PrivateFormat.TraditionalOpenSSL,
                encryption_algorithm=serialization.NoEncryption(),
            )
        )

    print("Done!")
