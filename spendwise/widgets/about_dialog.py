
import base64
from PyQt5.QtWidgets import QDialog, QVBoxLayout, QLabel, QPushButton, QHBoxLayout, QApplication
from PyQt5.QtGui import QPixmap, QPainter 
from PyQt5.QtCore import Qt, QSize

class AboutDialog(QDialog):
    def __init__(self, translator, logo_pixmap, parent=None): 
        super().__init__(parent)
        self.translator = translator
        self.logo_pixmap = logo_pixmap 
        self.setMinimumWidth(380) 
        self.setWindowFlags(self.windowFlags() & ~Qt.WindowContextHelpButtonHint) 
        self._init_ui()
        self.retranslate_ui() 

    def _init_ui(self):
        main_layout = QVBoxLayout(self)
        main_layout.setSpacing(15) 
        main_layout.setContentsMargins(20, 20, 20, 20) 

        self.logo_label = QLabel()
        if self.logo_pixmap and not self.logo_pixmap.isNull():
            scaled_logo = self.logo_pixmap.scaled(QSize(80,80), Qt.KeepAspectRatio, Qt.SmoothTransformation) 
        else: 
            scaled_logo = QPixmap(80,80)
            scaled_logo.fill(Qt.gray)
            p = QPainter(scaled_logo)
            p.drawText(scaled_logo.rect(), Qt.AlignCenter, "Logo")
            p.end()
        self.logo_label.setPixmap(scaled_logo)
        self.logo_label.setAlignment(Qt.AlignCenter)
        main_layout.addWidget(self.logo_label)

        self.app_name_label = QLabel() 
        font = self.app_name_label.font()
        font.setPointSize(font.pointSize() + 5) 
        font.setBold(True)
        self.app_name_label.setFont(font)
        self.app_name_label.setAlignment(Qt.AlignCenter)
        self.app_name_label.setObjectName("AboutAppNameLabel") 
        main_layout.addWidget(self.app_name_label)

        self.description_label = QLabel() 
        self.description_label.setWordWrap(True)
        self.description_label.setAlignment(Qt.AlignCenter)
        main_layout.addWidget(self.description_label)

        self.dev_info_label = QLabel() 
        self.dev_info_label.setAlignment(Qt.AlignCenter)
        main_layout.addWidget(self.dev_info_label)

        self.website_label = QLabel() 
        self.website_label.setOpenExternalLinks(True)
        self.website_label.setAlignment(Qt.AlignCenter)
        self.website_label.setObjectName("Link") 
        main_layout.addWidget(self.website_label)

        button_layout = QHBoxLayout()
        button_layout.addStretch()
        self.ok_button = QPushButton() 
        self.ok_button.setDefault(True) 
        self.ok_button.clicked.connect(self.accept)
        button_layout.addWidget(self.ok_button)
        button_layout.addStretch()
        main_layout.addLayout(button_layout)

    def retranslate_ui(self):
        self.setWindowTitle(self.translator.translate("about_dialog_title", "About SpendWise"))
        self.app_name_label.setText(f"{QApplication.applicationName()} {self.translator.translate('version_prefix','v')}{QApplication.applicationVersion()}")
        self.description_label.setText(self.translator.translate("app_description", "SpendWise is a personal expense tracking application designed to help you manage your finances effectively."))
        self.dev_info_label.setText(self.translator.translate("developed_by", "Developed by: PyPartners"))
        self.website_label.setText(f"<a href='https://github.com/PyPartners/'>{self.translator.translate('developer_website', 'Developer Website')}</a>")
        self.ok_button.setText(self.translator.translate("ok_button"))
