from cryptography import x509
from cryptography.hazmat.backends import default_backend
from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.primitives.asymmetric import rsa
from cryptography.hazmat.primitives import serialization
import os
import datetime

def generate_self_signed_cert(cert_file='selfsigned_cert.pem', key_file='private_key.pem'):
    # Generate a private key
    private_key = rsa.generate_private_key(
        public_exponent=65537,
        key_size=2048,
        backend=default_backend()
    )

    # Create a self-signed certificate
    subject = x509.Name([
        x509.NameAttribute(x509.NameOID.COUNTRY_NAME, u"US"),
        x509.NameAttribute(x509.NameOID.STATE_OR_PROVINCE_NAME, u"California"),
        x509.NameAttribute(x509.NameOID.LOCALITY_NAME, u"San Francisco"),
        x509.NameAttribute(x509.NameOID.ORGANIZATION_NAME, u"My Company"),
        x509.NameAttribute(x509.NameOID.COMMON_NAME, u"localhost"),
    ])
    issuer = subject

    cert = x509.CertificateBuilder().subject_name(
        subject
    ).issuer_name(
        issuer
    ).public_key(
        private_key.public_key()
    ).serial_number(
        x509.random_serial_number()
    ).not_valid_before(
        datetime.datetime.utcnow()
    ).not_valid_after(
        datetime.datetime.utcnow() + datetime.timedelta(days=365)
    ).add_extension(
        x509.BasicConstraints(ca=True, path_length=None), critical=True,
    ).sign(private_key, hashes.SHA256(), default_backend())

    # Write the private key and certificate to files
    with open(key_file, 'wb') as f:
        f.write(private_key.private_bytes(
            encoding=serialization.Encoding.PEM,
            format=serialization.PrivateFormat.TraditionalOpenSSL,
            encryption_algorithm=serialization.NoEncryption()
        ))

    with open(cert_file, 'wb') as f:
        f.write(cert.public_bytes(serialization.Encoding.PEM))

def load_certificate(cert_file='selfsigned_cert.pem'):
    with open(cert_file, 'rb') as f:
        return x509.load_pem_x509_certificate(f.read(), default_backend())

def load_private_key(key_file='private_key.pem'):
    with open(key_file, 'rb') as f:
        return serialization.load_pem_private_key(f.read(), password=None, backend=default_backend())