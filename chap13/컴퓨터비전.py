import sys
from PyQt5.QtWidgets import QApplication, QMainWindow, QLabel, QPushButton, QVBoxLayout, QWidget, QFileDialog, QTextEdit
from PyQt5.QtGui import QPixmap
from PyQt5.QtCore import Qt
import openai
from PIL import Image
import base64
from io import BytesIO
import requests

# OpenAI API 키 설정
openai.api_key = '본인키로 변경한다'

class ImageDescriptionApp(QMainWindow):
    def __init__(self):
        super().__init__()

        self.initUI()

    def initUI(self):
        self.setWindowTitle('컴퓨터비전으로 이미지 분석하는 앱')

        central_widget = QWidget()
        self.setCentralWidget(central_widget)

        self.layout = QVBoxLayout()

        self.image_label = QLabel('이미지 분석에 필요한 사진을 업로드하세요.')
        self.image_label.setAlignment(Qt.AlignCenter)
        self.image_label.setFixedSize(480, 300)
        self.image_label.setStyleSheet("border: 1px solid black;")
        self.layout.addWidget(self.image_label)

        self.upload_button = QPushButton('이미지 업로드')
        self.upload_button.clicked.connect(self.upload_image)
        self.layout.addWidget(self.upload_button)

        self.description_edit = QTextEdit()
        self.layout.addWidget(self.description_edit)

        central_widget.setLayout(self.layout)

    def upload_image(self):
        options = QFileDialog.Options()
        file_name, _ = QFileDialog.getOpenFileName(self, 'Open Image File', '', 'Images (*.png *.xpm *.jpg *.jpeg)', options=options)
        if file_name:
            self.display_image(file_name)
            self.get_image_description(file_name)

    def display_image(self, file_name):
        pixmap = QPixmap(file_name)
        pixmap = pixmap.scaled(480, 300, Qt.KeepAspectRatio, Qt.SmoothTransformation)
        self.image_label.setPixmap(pixmap)
        self.image_label.setScaledContents(False)

    def encode_image(self, image_path):
        with open(image_path, "rb") as image_file:
            return base64.b64encode(image_file.read()).decode('utf-8')

    def get_image_description(self, file_name):
        base64_image = self.encode_image(file_name)

        headers = {
            "Content-Type": "application/json",
            "Authorization": f"Bearer {openai.api_key}"
        }

        payload = {
            "model": "gpt-4o",
            "messages": [
                {
                    "role": "user",
                    "content": [
                        {
                            "type": "text",
                            "text": "이 이미지에 무엇이 있는지 한글로 설명해줘?"
                        },
                        {
                            "type": "image_url",
                            "image_url": {
                                "url": f"data:image/jpeg;base64,{base64_image}"
                            }
                        }
                    ]
                }
            ],
            "max_tokens": 300
        }

        response = requests.post("https://api.openai.com/v1/chat/completions", headers=headers, json=payload)

        data = response.json() 
        print(data['choices'][0]['message']['content'])
        self.description_edit.setPlainText(data['choices'][0]['message']['content'])

if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = ImageDescriptionApp()
    ex.show()
    sys.exit(app.exec_())
