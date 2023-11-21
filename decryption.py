import tkinter as tk
from Crypto.Cipher import DES3
from tkinter import filedialog
from tkinter import messagebox

def decrypt_image():
    encrypted_image_path = image_path_entry.get()
    key_file_path = key_path_entry.get()

    if not encrypted_image_path or not key_file_path:
        messagebox.showerror("Error", "Please enter both image and key paths.")
        return

    try:
        with open(key_file_path, 'rb') as key_file:
            tdes_key = key_file.read()

        cipher = DES3.new(tdes_key, DES3.MODE_EAX, nonce=b'0')

        with open(encrypted_image_path, 'rb') as input_file:
            encrypted_image_bytes = input_file.read()

        decrypted_image_bytes = cipher.decrypt(encrypted_image_bytes)

        with open("decrypted_image.png", 'wb') as output_file:
            output_file.write(decrypted_image_bytes)

        messagebox.showinfo("Success", "Decryption Done! Decrypted image saved as decrypted_image.png")
    except Exception as e:
        messagebox.showerror("Error", str(e))

def browse_image_path():
    image_path = filedialog.askopenfilename()
    if image_path:
        image_path_entry.delete(0, tk.END)
        image_path_entry.insert(0, image_path)

def browse_key_path():
    key_path = filedialog.askopenfilename()
    if key_path:
        key_path_entry.delete(0, tk.END)
        key_path_entry.insert(0, key_path)

def exit_app():
    root.destroy()

# Create the main window
root = tk.Tk()
root.title("Image Decryption Tool")
root.geometry("600x400")

# Background Image
background_image = tk.PhotoImage(file="background.png")
background_label = tk.Label(root, image=background_image)
background_label.place(relwidth=1, relheight=1)

# Create and arrange widgets
image_path_label = tk.Label(root, text="Image Path:", bg="Yellow")
image_path_entry = tk.Entry(root, width=40)
image_browse_button = tk.Button(root, text="Browse", command=browse_image_path, bg="orange")

key_path_label = tk.Label(root, text="Private Key Path:", bg="yellow")
key_path_entry = tk.Entry(root, width=40)
key_browse_button = tk.Button(root, text="Browse", command=browse_key_path, bg="orange")

decrypt_button = tk.Button(root, text="Decrypt", command=decrypt_image, bg="green", fg="white")
save_button = tk.Button(root, text="Save Decrypted Image", bg="blue", fg="white")
exit_button = tk.Button(root, text="Exit", command=exit_app, bg="red", fg="white")

# Arrange widgets in the grid
image_path_label.grid(row=0, column=0, padx=10, pady=5, sticky="e")
image_path_entry.grid(row=0, column=1, padx=10, pady=5)
image_browse_button.grid(row=0, column=2, padx=10, pady=5)

key_path_label.grid(row=1, column=0, padx=10, pady=5, sticky="e")
key_path_entry.grid(row=1, column=1, padx=10, pady=5)
key_browse_button.grid(row=1, column=2, padx=10, pady=5)

decrypt_button.grid(row=2, column=0, columnspan=3, padx=10, pady=10)
save_button.grid(row=3, column=0, columnspan=3, padx=10, pady=10)
exit_button.grid(row=4, column=0, columnspan=3, padx=10, pady=10)

# Center the buttons
root.grid_columnconfigure(0, weight=1)
root.grid_columnconfigure(1, weight=1)
root.grid_columnconfigure(2, weight=1)

# Start the GUI application
root.mainloop()
