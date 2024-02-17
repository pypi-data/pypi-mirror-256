import base64
import getpass
import os
import secrets
import sys
from base64 import urlsafe_b64decode as b64d
from base64 import urlsafe_b64encode as b64e

import sss
from cryptography.fernet import Fernet
from cryptography.hazmat.backends import default_backend
from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.primitives.kdf.pbkdf2 import PBKDF2HMAC
from cryptography.hazmat.primitives import serialization

backend = default_backend()
iterations = 100_000

def str_to_int(x) -> int:
    """
    Converts a string to int using byte encoding since the sss algorithm only works with numbers.
    """
    return int.from_bytes(str(x).encode("utf-8"), byteorder="big")

def int_to_str(x) -> str:
    """
    Converts an integer to a string using byte decoding.
    """
    return (int(x).to_bytes(((x.bit_length() + 7) // 8), byteorder='big')).decode("utf-8")

def _derive_key(password: bytes, salt: bytes, iterations: int = iterations) -> bytes:
    """Derive a secret key from a given password and salt"""
    kdf = PBKDF2HMAC(
        algorithm=hashes.SHA256(), length=32, salt=salt,
        iterations=iterations, backend=backend)
    return b64e(kdf.derive(password))

def password_encrypt(message: bytes, password: str, iterations: int = iterations) -> bytes:
    salt = secrets.token_bytes(16)
    key = _derive_key(password.encode(), salt, iterations)
    return b64e(
        b'%b%b%b' % (
            salt,
            iterations.to_bytes(4, 'big'),
            b64d(Fernet(key).encrypt(message)),
        )
    )

def password_decrypt(token: bytes, password: str) -> bytes:
    decoded = b64d(token)
    salt, iter, token = decoded[:16], decoded[16:20], b64e(decoded[20:])
    iterations = int.from_bytes(iter, 'big')
    key = _derive_key(password.encode(), salt, iterations)
    return Fernet(key).decrypt(token)
            

def split(args):
    chunks = []
    with open(args['f'], "rb") as in_file:
        print(f" getting 8 byte chunks from '{args['f']}'")
        while True:
            chunk = in_file.read(8)
            if chunk == b'':
                break
            else:
                shares = sss.generate_shares(int(args['n']), int(args['m']), str_to_int(chunk.decode("utf-8")))
                chunks.append(shares)

    path = args['f']
    directory_path = os.path.dirname(path)

    path_name_with_extension = os.path.basename(path) 
    name = os.path.splitext(path_name_with_extension)[0]

    sharefiles = []
    for chunk in chunks:
        i = 0
        for share in chunk:
            file_path = os.path.join(directory_path, f"{name}{i}.share")
            if f"{file_path}" not in sharefiles:
                sharefiles.append(f"{file_path}")
            with open(f"{file_path}", "a") as out_file:
                out_file.write(f"{share[0]} {share[1]}\n")
            i += 1
    for sf in sharefiles:
        if not args['e']:
            print(f" created '{sf}'")
        else:
            with open(f"{sf}", "rb") as file:
                data = file.read()
            with open(f"{sf}", "wb") as file:
                print(f"\n Please enter a password for {sf}")
                print(f"  • Password should have at least one number")
                print(f"  • Password should have at least one uppercase letter")
                print(f"  • Password should have at least one lowercase letter")
                print(f"  • Password should have at least one special character")
                print(f"  • Password should have at least 8 characters or more")
                match = False
                while not match:
                    password = getpass.getpass(f"\n Password for '{sf}':")
                    val = validate_password(password)
                    if len(val) > 0:
                        print(val)
                    else:
                        confirm = getpass.getpass(f" Please confirm password: ")
                        if password == confirm:
                            file.write(password_encrypt(data, password))
                            print(f" created '{sf}'")
                            break
                        print ("\n Passwords dont match")
    print ("\n Split complete!")

def join(args):
    shares = []
    decrypt_enabled = args['d']
    for share_file in args['s']:
        i = 0
        if not decrypt_enabled:
            with open(share_file, "r") as file:
                lines = file.readlines()
                for line in lines:
                    if line.strip() != "":
                        if share_file == args['s'][0]:
                            shares.append([])
                        shares[i].append([
                            int(line.strip().split(' ')[0]) if line.strip().split(' ')[0].isdecimal() else 0,
                            int(line.strip().split(' ')[1]) if line.strip().split(' ')[1].isdecimal() else 0,
                        ])
                        if len(shares[i]) == len(args['s']):
                            shares[i] = int_to_str(sss.reconstruct_secret(shares[i]))
                        i += 1  
        else:
            with open(share_file, "rb") as file:
                decrypted = False
                while not decrypted:
                    try:
                        lines = ((password_decrypt(file.read(), getpass.getpass(f"\n Password for '{share_file}':")).decode()).split("\r\n"))
                        decrypted = True
                    except Exception as error:
                        stacktrace = f"{sys.exc_info()}"
                        if "cryptography.fernet.InvalidToken" in stacktrace:
                            print(f"\n Invalid password")
                        else:
                            raise Exception(error)

                for line in lines:
                    if line.strip() != "":
                        if share_file == args['s'][0]:
                            shares.append([])
                        shares[i].append([
                            int(line.strip().split(' ')[0]) if line.strip().split(' ')[0].isdecimal() else 0,
                            int(line.strip().split(' ')[1]) if line.strip().split(' ')[1].isdecimal() else 0,
                        ])
                        if len(shares[i]) == len(args['s']):
                            shares[i] = int_to_str(sss.reconstruct_secret(shares[i]))
                        i += 1
    reconstructed_key = ''.join(shares)
    if decrypt_enabled == True or args['o'] == None:
        print(f"\n Reconstructed Key:\n\n{reconstructed_key}")
    else:
        file_path = args['o']
        save_key_as_pem(reconstructed_key,file_path)

def save_key_as_pem(recon_key, pem_file_path):
    try:
        # Deserialize the key string back to an RSAPrivateKey object
        key = serialization.load_pem_private_key(
            recon_key.encode(),
            password=None,
            backend=default_backend()
        )
    
        # Convert the private key to bytes
        key_bytes = key.private_bytes(
            encoding=serialization.Encoding.PEM,
            format=serialization.PrivateFormat.TraditionalOpenSSL,
            encryption_algorithm=serialization.NoEncryption()
        )

        # Save as PEM
        print(f"file path: {pem_file_path}")
        with open(pem_file_path, 'wb') as file:
            file.write(key_bytes)

        print(f"The reconstructed key has been saved as PEM to {pem_file_path}")
        

    except Exception as e:
        print(f"Failed to reconstruct the key: {e}")

def validate_password(password) -> str:
    has_digit = False
    has_upper = False
    has_lower = False
    has_sym = False
    has_len = False

    for char in password:
        if ord(char) >= 48 and ord(char) <= 57:
            has_digit = True
        elif ord(char) >= 65 and ord(char) <= 90:
            has_upper = True
        elif ord(char) >= 97 and ord(char) <= 122:
            has_lower = True
        elif not str(char).isalnum():
            has_sym = True

    if not len(password) < 8:
        has_len = True
        
    if not has_digit:
        return' Password should have at least one numeral'
    if not has_upper:
        return' Password should have at least one uppercase letter'
    if not has_lower:
        return' Password should have at least one lowercase letter'
    if not has_sym:
        return' Password should have at least one special character'
    if not has_len:
        return' Password cannot be less than 8 characters'
    return ""