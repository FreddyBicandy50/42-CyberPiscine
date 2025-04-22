import time
import hmac
import hashlib
from cryptography.fernet import Fernet
from urllib.parse import urljoin, urlparse
import argparse

hexa_decimal=["0","1","2","3","4","6","7","8","9","a","b","c","d","e","f"]

'''
    generate ft_otp.key file based on SECERT and key file:
        @PARAM SECRET is the genrate fernet key #Line 78
        @PARAM key:str is a string of hexadecimal key
        
        encrypt the hexadecimal key using the SECRET
        save both keys into ft_otp.key
'''
def generate_key(SECRET ,key:str):
    
    # encrypting provided key
    print(f"encrypting key  = {key}")
    fernet = Fernet(SECRET)
    encrypted_key=fernet.encrypt(key.encode())
    print(f"Success=>:{encrypted_key}")
    
    with open("ft_otp.key","wb") as f:
        f.write(SECRET + b"\n" + encrypted_key) # writing the SECRET key and the encrypted key
 
'''
    generate and returns a OTP (HOTP):
        @PARAM filepath to read the keys from
            key file should be 2 lines containing SECRET and Encrypted_KEY
        @PARAM key:str is a string of hexadecimal key
        
        decrypt the key using app SECRET
        generating time and returning and otp code
'''   
def generate_otp(filepath):
    with open(filepath, "rb") as f:
        key = f.read().splitlines()
        if len(key) != 2:
            raise ValueError("Invalid key file format")

    fernet = Fernet(key[0])
    decrypted_key = fernet.decrypt(key[1]).decode()

    current_time = int(time.time())
    counter = current_time // 60
    
    hmac_result = hmac.new(bytes.fromhex(decrypted_key), counter.to_bytes(8,'big'), hashlib.sha1).digest()
    offset = hmac_result[-1] & 0x0F
    truncated = hmac_result[offset:offset + 4]
    code = int.from_bytes(truncated, 'big') & 0x7FFFFFFF
    otp = str(code % 10**6).zfill(6)
    return otp

def main ():
    ''' 
        parsing input from user :
            -g user provides hexadecimal key
                out: program encrypts and dump the key in ft_opt.key (keeping old key safely)
            -k


    
    '''
    parser = argparse.ArgumentParser(description="one time password")
    parser.add_argument("-g", help="key filename in hexadecimal")
    parser.add_argument("-k", help="generates a one time password key")
    args = parser.parse_args() 
    
    
    # check for provided arguments
    if not args.g and not args.k:
        parser.error("You must provide either -g or -k option.")
        return




    if args.g:
        print(f"Generating key from file: {args.g}")
        with open(args.g,"r") as f:
            key = f.read().strip().lower()
        if(len(key)!=64 and not all(c in hexa_decimal for c in key)):
            print(f"error generating key should be in hexadecimal")
            return
        SECRET = Fernet.generate_key()  # This is our app secret
        generate_key(SECRET,key)
    elif args.k:
        print(f"Generating OTP using key file: {args.k}")
        try:
            otp=generate_otp(args.k)
            print(f"Your OTP is: {otp}")
        except Exception as e:
            print(f"Error reading key: {e}")
            

if __name__ == "__main__":
    main()

