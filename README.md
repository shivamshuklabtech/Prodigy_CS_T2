# Prodigy_CS_T2
PixelManipulation
# Pixel Lock - Image Encryption via Pixel Manipulation

A Flask-based web application that demonstrates image encryption using pixel-level XOR manipulation. This project allows users to upload an image, apply a numeric key to encrypt it, and use the same key again to decrypt it.

## 📌 Project Information

**Repository Name:** Prodigy_CS_T2

**GitHub Repository:**
https://github.com/shivamshuklabtech/Prodigy_CS_T2

## 🚀 Features

* Upload any image file
* Encrypt images using XOR pixel manipulation
* Decrypt encrypted images using the same key
* Modern and responsive user interface
* Real-time image preview
* Download encrypted/decrypted results
* Supports PNG, JPG, JPEG, and other Pillow-compatible formats

## 🔐 How It Works

The application uses the XOR (Exclusive OR) operation on each RGB pixel channel.

```python
encrypted_pixel = original_pixel ^ key
```

Since XOR is reversible:

```python
(original_pixel ^ key) ^ key = original_pixel
```

Applying the same key twice restores the original image.

## 🛠️ Technologies Used

* Python 3
* Flask
* Pillow (PIL)
* HTML5
* CSS3
* JavaScript

## 📂 Project Structure

```text
Prodigy_CS_T2/
│
├── pixel_lock_app.py
├── README.md
└── requirements.txt
```

## ⚙️ Installation

### 1. Clone the Repository

```bash
git clone https://github.com/shivamshuklabtech/Prodigy_CS_T2.git
cd Prodigy_CS_T2
```

### 2. Create a Virtual Environment (Optional)

```bash
python -m venv venv
```

Activate the environment:

#### Windows

```bash
venv\Scripts\activate
```

#### Linux/macOS

```bash
source venv/bin/activate
```

### 3. Install Dependencies

```bash
pip install flask pillow
```

or

```bash
pip install -r requirements.txt
```

## ▶️ Running the Application

Start the Flask server:

```bash
python pixel_lock_app.py
```

Open your browser and visit:

```text
http://127.0.0.1:5000
```

## 📸 Usage

1. Launch the application.
2. Upload an image.
3. Enter an encryption key (0–255).
4. Click **Apply Key**.
5. View the encrypted image.
6. Download the result.
7. To decrypt, upload the encrypted image and use the same key again.

## 🧪 Example

| Operation     | Key |
| ------------- | --- |
| Encrypt Image | 42  |
| Decrypt Image | 42  |

Using the same key twice restores the original image.

## 🎯 Learning Outcomes

This project demonstrates:

* Image processing with Pillow
* XOR-based encryption techniques
* Flask web application development
* REST API handling
* File uploads in Flask
* Frontend and backend integration

## 🔒 Security Note

This project is intended for educational purposes and demonstrates the concept of reversible image encryption using XOR operations. It should not be used as a replacement for modern cryptographic standards in production environments.

## 🤝 Contributing

Contributions, suggestions, and improvements are welcome.

1. Fork the repository
2. Create a feature branch
3. Commit your changes
4. Open a Pull Request

## 📄 License

This project is licensed under the MIT License.

## 👨‍💻 Author

**Shivam Shukla**

GitHub: https://github.com/shivamshuklabtech

---

⭐ If you found this project useful, please consider starring the repository.

