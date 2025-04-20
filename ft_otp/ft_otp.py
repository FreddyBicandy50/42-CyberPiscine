import os
from cryptography.fernet import Fernet
from urllib.parse import urljoin, urlparse
import argparse

hexa_decimal=["0","1","2","3","4","6","7","8","9","a","b","c","d","e","f"]

# Takes the key stirng and generates an encrypted key based on it
def encrypt_and_save_key(fernet,key:str):
    #hashing the key using fernet
    encrypted_key=fernet.encrypt(key.encode())
    os.rename("ft_otp.key","ft_otp.key.old") #keeping old key
    with open("ft_otp.key","wb") as f:
        f.write(encrypted_key)
    print("key was succesfully saved in ft_opt.key.")
    return

def load_and_dec

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
        fernet = Fernet(SECRET)
        encrypt_and_save_key(fernet,key)

    elif args.k:
        print(f"Generating OTP using key file: {args.k}")
        key_filename= args.k
        
        try:
            key = load_and_decrypt_key(args.k)
            print(f"Decrypted key: {key}")
        except Exception as e:
            print(f"Error reading key: {e}")
            
            

if __name__ == "__main__":
    main()

