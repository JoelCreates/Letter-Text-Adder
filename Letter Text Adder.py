import sys
import os
import pyqtgraph as pg
from PIL import Image
from PIL import ImageDraw
from PIL import ImageFont
from PIL.ImageQt import ImageQt
from datetime import datetime
from PyQt6 import *
from PyQt6 import QtCore
from PyQt6.QtGui import *
from PyQt6.QtCore import * 
from PyQt6.QtWidgets import *
from PyQt6.QtPrintSupport import QPrintDialog, QPrinter, QPrintPreviewDialog


class LetterTextAdder(QWidget):
    
    def __init__(self):
        super().__init__()

        #name definition
        self.full_name = ""
        
        # set the window title and size
        self.setWindowTitle("Letter Text Adder")
        self.setGeometry(100, 100, 400, 200)

        # set the window icon
        self.setWindowIcon(QIcon("Crest.png"))
        
        # set the font for the labels
        font = QFont()
        font.setPointSize(12)

        # Date Variables
        self.now = datetime.now()
        self.day = self.now.strftime("%d").lstrip("0")
        self.suffix = "th" if self.day in ["11", "12", "13"] else {"1": "st", "2": "nd", "3": "rd"}.get(self.day[-1], "th")
        self.day = self.day + self.suffix
        self.currentdate = self.now.strftime(f"{self.day} %B %Y")
        print(self.currentdate)

        #Text Font
        fontLetter = ImageFont.truetype("BASKVILL.TTF", 62)

        
        # create the labels and input box
        name_label = QLabel("Name:", self)
        name_label.setFont(font)
        self.name_input = QLineEdit(self)
        self.name_input.setFont(font)
        
        # create the radio buttons
        radio_label = QLabel("Title:", self)
        radio_label.setFont(font)
        self.button_group = QButtonGroup(self)
        titles = ["Mr", "Mrs", "Dr", "Miss", "Ms"]
        for i, title in enumerate(titles):
            radio_button = QRadioButton(title, self)
            radio_button.setFont(font)
            self.button_group.addButton(radio_button, i)
            if i == 0:
                radio_button.setChecked(True)
        
        # create the save and print buttons
        apply_button = QPushButton("Apply Name to Doc", self)
        apply_button.setObjectName("apply_button")
        apply_button.setFont(font)
        save_button = QPushButton("Save", self)
        save_button.setFont(font)
        print_button = QPushButton("Print", self)
        print_button.setFont(font)

        #save the document to a file
        save_button.clicked.connect(self.save_tofile)

        #pop up the printer dialog
        apply_button.clicked.connect(self.apply_changes)

        #pop up the printer dialog
        print_button.clicked.connect(self.print_letter)

        # connect radio buttons to a function that updates the name input
        self.button_group.buttonClicked.connect(self.update_name_input)


        # set the layout for the labels and input box
        name_layout = QHBoxLayout()
        name_layout.addWidget(name_label, alignment=QtCore.Qt.AlignmentFlag.AlignHCenter | QtCore.Qt.AlignmentFlag.AlignHCenter)
        name_layout.addWidget(self.name_input, alignment=QtCore.Qt.AlignmentFlag.AlignHCenter | QtCore.Qt.AlignmentFlag.AlignHCenter)
        name_layout.addStretch()
        
        # set the layout for the radio buttons
        radio_layout = QHBoxLayout()
        radio_layout.addWidget(radio_label, alignment=QtCore.Qt.AlignmentFlag.AlignVCenter | QtCore.Qt.AlignmentFlag.AlignHCenter)
        for radio_button in self.button_group.buttons():
            radio_layout.addWidget(radio_button, alignment=QtCore.Qt.AlignmentFlag.AlignVCenter | QtCore.Qt.AlignmentFlag.AlignHCenter)
        radio_layout.addStretch()
        
        # set the layout for the buttons
        button_layout = QHBoxLayout()
        button_layout.addWidget(apply_button, alignment=QtCore.Qt.AlignmentFlag.AlignVCenter | QtCore.Qt.AlignmentFlag.AlignHCenter)
        button_layout.addWidget(save_button, alignment=QtCore.Qt.AlignmentFlag.AlignVCenter | QtCore.Qt.AlignmentFlag.AlignHCenter)
        button_layout.addWidget(print_button, alignment=QtCore.Qt.AlignmentFlag.AlignVCenter | QtCore.Qt.AlignmentFlag.AlignHCenter)
        button_layout.addStretch()
        
        # set the main layout and add the sub-layouts
        main_layout = QVBoxLayout()
        main_layout.addLayout(name_layout)
        main_layout.addLayout(radio_layout)
        main_layout.addLayout(button_layout)
        main_layout.setAlignment(QtCore.Qt.AlignmentFlag.AlignCenter)
        
        # set the main layout for the window
        self.setLayout(main_layout)




     # set the style sheet for the GUI
        style_sheet = """
        QWidget {
            background-color: #F5F5F5;
            color: #333333;
        }
        
        QLabel {
            color: #333333;
            font-size: 18px;
        }
        
        QLineEdit, QRadioButton, QPushButton {
            font-size: 16px;
            padding: 6px;
            border-radius: 4px;
            border: 2px solid #CCCCCC;
            background-color: #FFFFFF;
        }
        
        QPushButton:hover {
            background-color: #E0E0E0;
        }
        
        QPushButton:pressed {
            background-color: #CCCCCC;
        }
        """
        
        self.setStyleSheet(style_sheet)
    # method to center the window
    def center(self):
        screens = QApplication.screens()
        screen_geometry = screens[0].geometry()

        x = (screen_geometry.width() - self.width()) / 2
        y = (screen_geometry.height() - self.height()) / 2

        self.move(x, y)
        
    def update_name_input(self, radio_button):
        name = self.name_input.text()
        title = radio_button.text()
        if name:
            self.full_name = f"{title} {name}"
            print(self.full_name)
        else:
            self.full_name = title
            print(self.full_name)

    def print_letter(self):
        # Create a high-resolution version of the edited image
        high_res_image = Image.open("edited_image.jpg")
        high_res_image = high_res_image.resize((3000, 4242))  # Adjust the resolution as needed

        # Save the high-resolution image to a temporary file
        temp_image_path = "temp_high_res_image.jpg"
        high_res_image.save(temp_image_path)

        # Create a printer dialog
        dialog = QPrintPreviewDialog()

        # Load the high-resolution image into a QPixmap
        pixmap = QPixmap(temp_image_path)

        # Set the preview pixmap for the print preview dialog
        dialog.paintRequested.connect(self.print_preview)

        # Show the print preview dialog
        dialog.exec()

        # Clean up the temporary high-resolution image file
        os.remove(temp_image_path)
    """
        # define the printer variable before the if block and set it to None
        printer = None

        # if the user accepts, update the printer variable with the selected printer
        if dialog.exec() == QDialog.DialogCode.Accepted:
            printer = dialog.printer()
            # create a QPixmap object from the edited image file
            pixmap = QPixmap("edited_image.jpg")
            # get the printer object from the dialog
            printer = dialog.printer()
            # create a QPainter object and draw the image on it
            painter = QPainter()
            painter.begin(printer)
            painter.drawPixmap(0, 0, pixmap)
            painter.end()
            # set the preview paint device for the dialog
            dialog.setPreviewPixmap(pixmap)

            # set the painter object as the preview paint device for the dialog
            dialog.setPreviewPaintDevice(painter)
    """

    def print_preview(self, printer):
        # create a QPixmap object from the edited image file
        pixmap = QPixmap("temp_high_res_image.jpg")

        # calculate the desired pixel dimensions for A4 paper at 96 DPI
        a4_width_in_pixels = 794
        a4_height_in_pixels = 1123

        # resize the image to fit within the A4 dimensions
        scaled_pixmap = pixmap.scaled(a4_width_in_pixels, a4_height_in_pixels, Qt.AspectRatioMode.KeepAspectRatio)

        # calculate the position to center the image on the page
        x = (printer.width() - scaled_pixmap.width()) / 2
        y = (printer.height() - scaled_pixmap.height()) / 2

        # create a QPainter object and draw the scaled image on it
        painter = QPainter()
        painter.begin(printer)
        painter.drawPixmap(x, y, scaled_pixmap)
        painter.end()




    def apply_changes(self):
        # Disable the apply button to prevent spamming
        #print(self.findChild(QPushButton, "apply_button"))
        print("Changes Applied!")
        apply_button = (self.findChild(QPushButton, "apply_button"))
        apply_button.setEnabled(False)

        #Image access
        print("Accessing Image!")
        image = Image.open("image.jpg")
        draw = ImageDraw.Draw(image)
        fontAdder = ImageFont.truetype("BASKVILL.TTF", 62)
        name = self.full_name
        print(name + "this works")

        # Determine the size of the text
        text_width, text_height = draw.textsize(name, fontAdder)
        text_width2, text_height2 = draw.textsize(self.currentdate, fontAdder)

        # Determine the location to draw the text
        x = 260.66141732283467
        y = 982.3149606299214

        x_date = 1985.4330708661416
        y_date = 780.6299212598426
        
        # Add the text to the image
        draw.text((x, y), name, fill="black", font=fontAdder)
        draw.text((x_date, y_date), self.currentdate, fill="black", font=fontAdder)

        # Save the edited image
        image.save("edited_image.jpg")
        
        # Create a new label widget
        message_label = QLabel("Changes applied", self)

        # Set the font and alignment for the label
        font = QFont()
        font.setPointSize(12)
        message_label.setFont(font)
        message_label.setAlignment(QtCore.Qt.AlignmentFlag.AlignCenter)

        # Add the label widget to the button layout
        button_layout = self.layout().itemAt(2)
        button_layout.addWidget(message_label)

        # Use QTimer to remove the label after 10 seconds
        QTimer.singleShot(1400, lambda: message_label.deleteLater())

        # Re-enable the apply button after the label disappears
        QTimer.singleShot(1400, lambda: apply_button.setEnabled(True))

    def save_tofile(self):
        print("Document saved!")
            

        



if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = LetterTextAdder()
    ex.show()
    sys.exit(app.exec())

