
from PyQt5.QtWidgets import QSplashScreen, QApplication
from PyQt5.QtGui import QPixmap, QPainter, QColor, QFont
from PyQt5.QtCore import Qt, QTimer, QPropertyAnimation, QEasingCurve

class SplashScreen(QSplashScreen):
    def __init__(self, pixmap):
        base_pixmap = QPixmap(max(256, pixmap.width() + 40), max(128, pixmap.height() + 60)) 
        base_pixmap.fill(Qt.transparent) 

        painter = QPainter(base_pixmap)
        painter.setRenderHint(QPainter.Antialiasing)

        logo_x = (base_pixmap.width() - pixmap.width()) / 2
        logo_y = (base_pixmap.height() - pixmap.height()) / 2 - 15 
        if pixmap.isNull(): 
             painter.setPen(Qt.white)
             painter.setFont(QFont(QApplication.font().family(), 16, QFont.Bold))
             painter.drawText(base_pixmap.rect().adjusted(0,0,0,-30), Qt.AlignCenter, "SpendWise")
        else:
            painter.drawPixmap(int(logo_x), int(logo_y), pixmap)

        painter.setPen(Qt.lightGray) 
        app_font = QFont(QApplication.font().family(), 9)
        painter.setFont(app_font)
        version_text = QApplication.applicationName() + "  " + QApplication.applicationVersion()
        painter.drawText(base_pixmap.rect().adjusted(0,0,0,-10), Qt.AlignBottom | Qt.AlignHCenter, version_text)
        painter.end()

        super().__init__(base_pixmap)
        self.setWindowFlags(Qt.FramelessWindowHint | Qt.WindowStaysOnTopHint | Qt.SplashScreen)
        self.setAttribute(Qt.WA_TranslucentBackground) 

        self.opacity_animation = QPropertyAnimation(self, b"windowOpacity")
        self.opacity_animation.setDuration(700) 
        self.opacity_animation.setStartValue(0.0)
        self.opacity_animation.setEndValue(1.0)
        self.opacity_animation.setEasingCurve(QEasingCurve.InOutCubic)

        QTimer.singleShot(50, self.opacity_animation.start) 

    def finish(self, main_window_instance):
        if self.opacity_animation.state() == QPropertyAnimation.Running and            self.opacity_animation.direction() == QPropertyAnimation.Forward:
            try: self.opacity_animation.finished.disconnect() 
            except TypeError: pass 
            self.opacity_animation.finished.connect(lambda: self._start_fade_out(main_window_instance))
        else: 
            self._start_fade_out(main_window_instance)

    def _start_fade_out(self, main_window_instance):
        self.opacity_animation.setDirection(QPropertyAnimation.Backward) 
        try: self.opacity_animation.finished.disconnect() 
        except TypeError: pass 

        self.opacity_animation.finished.connect(main_window_instance.show_animated)
        self.opacity_animation.finished.connect(self.close) 

        if self.opacity_animation.state() != QPropertyAnimation.Running:
            self.opacity_animation.setStartValue(self.windowOpacity()) 
            self.opacity_animation.setEndValue(0.0)
            self.opacity_animation.start()
        elif self.opacity_animation.direction() == QPropertyAnimation.Forward : 
            pass
