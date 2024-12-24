import cv2
import pytesseract
from tkinter import Tk, Label, Button, filedialog
from PIL import Image, ImageTk

# Configure Tesseract path if necessary
pytesseract.pytesseract.tesseract_cmd = r'C:\Program Files\Tesseract-OCR	esseract.exe'

class PokerRecognitionApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Poker Card Recognition")
        
        self.label = Label(root, text="Upload an image of a poker table")
        self.label.pack()

        self.upload_button = Button(root, text="Upload Image", command=self.upload_image)
        self.upload_button.pack()

        self.process_button = Button(root, text="Process Image", command=self.process_image)
        self.process_button.pack()

        self.result_label = Label(root, text="")
        self.result_label.pack()

        self.image_label = Label(root)
        self.image_label.pack()

        self.image_path = None

    def upload_image(self):
        self.image_path = filedialog.askopenfilename()
        if self.image_path:
            img = Image.open(self.image_path)
            img = img.resize((400, 300), Image.ANTIALIAS)
            img = ImageTk.PhotoImage(img)
            self.image_label.config(image=img)
            self.image_label.image = img

    def process_image(self):
        if not self.image_path:
            self.result_label.config(text="Please upload an image first.")
            return

        # Load image using OpenCV
        image = cv2.imread(self.image_path)
        gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
        # Preprocess image for better OCR results
        gray = cv2.GaussianBlur(gray, (5, 5), 0)
        edged = cv2.Canny(gray, 75, 200)

        # Use Tesseract to do OCR on the image
        text = pytesseract.image_to_string(gray)
        self.result_label.config(text=f"Recognized Text: {text}")

        # Here you can add more processing to detect cards and table info

if __name__ == "__main__":
    root = Tk()
    app = PokerRecognitionApp(root)
    root.mainloop()
