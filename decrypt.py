import os, glob
from Crypto.Cipher import AES
from Crypto.PublicKey import RSA
from Crypto.Cipher import PKCS1_OAEP

#get the encrypted key from file
file_in = open("encryptedkey.pem", "rb") # Read bytes
key_from_file = file_in.read() # This key should be the same
file_in.close()


#get the RSA private key to decrypt the 256-bits key
with open("privatekey.pem","rb")as f:
    privkey = f.read()

#decrypt the encrypted 256-bits key using private RSA key
rsakey = RSA.importKey(privkey)
cipher = PKCS1_OAEP.new(rsakey)
unencrypedkey = cipher.decrypt(key_from_file)

#hard-coded IV
IV = "This is IV123456"
IV = IV.encode()

def decrypt():
    #get all .bin file in the folder
    files = (glob.glob('*.bin'))
    for file in files:
        input_file = file
        output_file = 'unencrypted'+file.replace("encrypted","").replace(".bin","")+'.jpg' #rename the output file
        k = unencrypedkey
        file_in = open(input_file, "rb")
        f = file_in.read()
        cipher = AES.new(k, AES.MODE_CBC, IV)
        ciphered_data = cipher.decrypt(f)
        file_in.close()
        file_out = open(output_file, "wb") # Open file to write bytes
        file_out.write(ciphered_data.rstrip(b'0'))#remove the previous padding
        file_out.close()
        os.remove(file) #delete the encrypted .jpg files

decrypt()