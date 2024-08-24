import streamlit as st
import numpy as np
from PIL import Image
from io import BytesIO

# Function to XOR encrypt/decrypt the image
def xor_encrypt_decrypt(data, key):
    return bytes([b ^ key for b in data])

# Function to convert an image to bytes
def image_to_bytes(image):
    buf = BytesIO()
    image.save(buf, format='PNG')
    return buf.getvalue()

# Function to convert bytes to an image
def bytes_to_image(data):
    return Image.open(BytesIO(data))

# Streamlit application
st.set_page_config(page_title="Image Encryption Tool", layout="wide")

# Title and description
st.title("Image Encryption Tool")
st.markdown("""
    Encrypt or decrypt images with a click! Upload, secure, and download your files with ease.
""")

# Dropdown for selecting action
st.markdown("### Choose an action:")
action = st.selectbox(
    "Select option:",  # Dropdown label
    ["Encrypt Image", "Decrypt Image"]  # Options
)

# Key input
key = st.number_input("Enter a key (0-255) [Note:Use this key for both encryption and decryption]:", min_value=0, max_value=255, value=123)

# File uploader and processing for encryption
if action == "Encrypt Image":
    uploaded_file = st.file_uploader("Upload Image", type=["png", "jpg", "jpeg"])
    if uploaded_file is not None:
        st.image(uploaded_file, caption='Uploaded Image', use_column_width=True)
        image = Image.open(uploaded_file).convert("RGB")
        if st.button("Encrypt Image"):
            image_data = image_to_bytes(image)
            encrypted_image = xor_encrypt_decrypt(image_data, key)
            st.download_button(
                label="Download Encrypted Image",
                data=encrypted_image,
                file_name="encrypted_image.bin",
                mime="application/octet-stream"
            )
            st.success("Image encrypted successfully!")

# File uploader and processing for decryption
elif action == "Decrypt Image":
    encrypted_file = st.file_uploader("Upload Encrypted File", type=["bin"])
    if encrypted_file is not None:
        if st.button("Decrypt Image"):
            encrypted_data = encrypted_file.read()
            decrypted_data = xor_encrypt_decrypt(encrypted_data, key)
            decrypted_image = bytes_to_image(decrypted_data)
            st.image(decrypted_image, caption='Decrypted Image', use_column_width=True)
            st.success("Image decrypted successfully!")

# Footer
st.markdown("---")
st.markdown("Made with ❤️ by Maryam Fatima")
