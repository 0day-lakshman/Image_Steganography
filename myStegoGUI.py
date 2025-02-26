import cv2
import numpy as np
import os
import tkinter as tk
from tkinter import filedialog, messagebox

# Encrypt Message Into Image
def encrypt_image():
    image_path = filedialog.askopenfilename(title="Select Image")
    if not image_path:
        return
    
    secret_message = message_entry.get()
    passcode = password_entry.get()
    output_path = "encryptedImage.png"
    
    img = cv2.imread(image_path)
    if img is None:
        messagebox.showerror("Error", "Unable to load image.")
        return
    
    message = passcode + '::' + secret_message  # Embed Password With Msg
    message += chr(0)  # Null Character As Delimiter
    
    d = {chr(i): i for i in range(256)}
    
    n, m, z = 0, 0, 0
    for char in message:
        img[n, m, z] = d[char]
        n += 1
        m += 1
        z = (z + 1) % 3
        if n >= img.shape[0] or m >= img.shape[1]:
            messagebox.showerror("Error", "Message is too large for the image.")
            return
    
    cv2.imwrite(output_path, img)
    messagebox.showinfo("Success", f"Message encrypted and saved as {output_path}")
    
    message_entry.delete(0, tk.END)
    password_entry.delete(0, tk.END)

# Decrypt Message From Image
def decrypt_image():
    image_path = filedialog.askopenfilename(title="Select Encrypted Image")
    if not image_path:
        return
    
    img = cv2.imread(image_path)
    if img is None:
        messagebox.showerror("Error", "Unable to load image.")
        return
    
    c = {i: chr(i) for i in range(256)}
    
    message = ""
    n, m, z = 0, 0, 0
    while True:
        try:
            char = c[img[n, m, z]]
            if char == chr(0):  # Null Character Indicates End Of Msg
                break
            message += char
            n += 1
            m += 1
            z = (z + 1) % 3
            if n >= img.shape[0] or m >= img.shape[1]:
                break
        except IndexError:
            break
    
    try:
        stored_password, extracted_message = message.split('::', 1)
    except ValueError:
        messagebox.showerror("Error", "Invalid data in image.")
        return
    
    entered_password = password_entry.get()
    if stored_password == entered_password:
        messagebox.showinfo("Decryption Successful", f"Secret Message: {extracted_message}")
    else:
        messagebox.showerror("Error", "Incorrect Password! Access Denied.")
    
    message_entry.delete(0, tk.END)
    password_entry.delete(0, tk.END)

# GUI Setup
root = tk.Tk()
root.title("Image Steganography")
root.geometry("400x300")

tk.Label(root, text="Secret Message:").pack()
message_entry = tk.Entry(root, width=50)
message_entry.pack()

tk.Label(root, text="Password:").pack()
password_entry = tk.Entry(root, width=50, show="*")
password_entry.pack()

tk.Button(root, text="Encrypt Image", command=encrypt_image).pack(pady=10)
tk.Button(root, text="Decrypt Image", command=decrypt_image).pack(pady=10)

root.mainloop()