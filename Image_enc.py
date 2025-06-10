from PIL import Image
import shutil
import os
import sys

# Define the ImageEncryptor class
class ImageEncryptor:
    # Function to encrypt an image
    def verify_image(self,file1):
        # Open a file dialog to select the image file
        #file1 = filedialog.askopenfile(mode='r', filetypes=[('jpg file', '*.jpg')])
        if file1 is not None:
            file_name = file1.name
                # Check if the image is already encrypted
            if self._is_encrypted(file_name):
                print("Error", "Selected image is already Encrypted or Corrupted.")
                return False
                #sys.exit(0)
            else:
                return file_name
        else:
            print("Error", "Please Select an image")
            sys.exit(0)

    # Function to decrypt an image
    def check_image(self,file1):
        #file1 = filedialog.askopenfile(mode='r', filetypes=[('jpg file', '*.jpg')])
        if file1 is not None:
            file_name = file1.name
            # Check if the image is encrypted
            if self._is_encrypted(file_name):
                return file_name
            else:
                print("Error", "Selected image is not encrypted.")
                return False
                #sys.exit(0)
        else:
            print("Error", "Please Select an image")
            sys.exit(0)
                
    # Function to check if an image is encrypted
    def _is_encrypted(self,file_name):
        try:
            # Try to open and verify the image
            img = Image.open(file_name)
            img.verify()
            return False
        except Exception:
            # If an error occurs, the image is encrypted
            return True

    # Function to encrypt a file
    def _encrypt_file(self, file_name, key):
        # Define a function to encrypt a file
        def encrypt_file(file_name, key):
            try:
                # Open the file in binary mode and read its contents
                with open(file_name, 'rb') as fi:
                    image = bytearray(fi.read())
                # For each byte in the image
                for index, values in enumerate(image):
                    # XOR the byte with the key and take the modulus 256
                    image[index] = (values ^ int(key)) % 256
                # Write the encrypted image back to the file
                with open(file_name, 'wb') as fi1:
                    fi1.write(image)
                print("Saved image as : ", file_name)
                return True
            except Exception as e:
                print(f"An error occurred: {e}")
                #sys.exit(0)
                return False
        return encrypt_file(file_name, key)

        # Function to decrypt a file
    def _decrypt_file(self, file_name, key):
        # Define a function to decrypt a file
        def decrypt_file(file_name, key):
            try:
                # Get the base name of the file
                fname = os.path.basename(file_name)
                # Create a temporary file name
                file_name1 = file_name.strip(fname)+'temp.jpg'
                # Copy the file to the temporary file
                shutil.copy2(file_name, file_name1)
                # Open the temporary file in binary mode and read its contents
                with open(file_name1, 'rb') as fi:
                    image = bytearray(fi.read())
                # For each byte in the image
                for index, values in enumerate(image):
                    # XOR the byte with the key and take the modulus 256
                    image[index] = (values ^ int(key)) % 256
                # Write the decrypted image back to the temporary file
                with open(file_name1, 'wb') as fi1:
                    fi1.write(image)
                # Check if the temporary file is encrypted
                assert not self._is_encrypted(file_name1)
                # Remove the original file
                os.remove(file_name)
                # Rename the temporary file to the original file name
                os.rename(file_name1, file_name)
                print("Saved image as : ", file_name)
                return True
            except Exception as e:
                # Show an error message if the key is invalid
                print("Error", "Key is Invalid.")
                # Remove the temporary file
                os.remove(file_name1)
                print(e)
                #sys.exit(0)
                return False
        return decrypt_file(file_name, key)