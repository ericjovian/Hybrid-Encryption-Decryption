import glob
from Crypto.Cipher import AES
from Crypto.PublicKey import RSA
from Crypto.Random import get_random_bytes
from Crypto.Util.Padding import pad
from Crypto.Cipher import PKCS1_OAEP

#hard-coded IV
IV = "This is IV123456"
IV = IV.encode()
#generate new RSA key
rsakey = RSA.generate(2048)

#export the private and public key to .pem file
privkey = rsakey.exportKey()
pubkey = rsakey.publickey().exportKey()

with open('publickey.pem','wb') as f:
    f.write(pubkey)

with open('privatekey.pem','wb') as f:
    f.write(privkey)

#get the public key from file to encrypt the 256-bits key
with open('publickey.pem','rb') as f:
    pubkey = f.read()

rsakey = RSA.importKey(pubkey)
#encrypting function
cipher = PKCS1_OAEP.new(rsakey)

#generate 32 bytes * 8 = random 256-bits key (1 byte = 8 bits)
key = get_random_bytes(32)
#encrypt the key using rsa public key
encryptedkey = cipher.encrypt(key)
#save the encrypted key to a file
with open('encryptedkey.pem','wb') as f:
    f.write(encryptedkey)

#encrypt function
def encrypt():
    #get all .jpg files in the same folder
    files = (glob.glob('*.jpg'))
    for file in files:
        output_file = 'encrypted'+file.replace(".jpg","")+'.bin' #rename the output file
        k = key
        file_in = open(file, "rb")
        f = file_in.read()
        cipher = AES.new(k, AES.MODE_CBC, IV)
        ciphered_data = cipher.encrypt(pad(f, AES.block_size))
        file_out = open(output_file, "wb") # Open file to write bytes
        file_out.write(ciphered_data)
        file_out.close()

encrypt()