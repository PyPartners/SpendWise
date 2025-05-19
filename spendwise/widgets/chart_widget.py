
from PyQt5.QtWidgets import QWidget, QVBoxLayout, QLabel, QApplication, QSizePolicy
from PyQt5.QtChart import QChart, QChartView, QPieSeries, QPieSlice, QLegend
from PyQt5.QtGui import QPainter, QColor, QFont, QBrush, QPen
from PyQt5.QtCore import Qt
from collections import defaultdict

class SpendChartWidget(QWidget):
    def __init__(self, data_manager, translator, parent=None):
        super().__init__(parent)
        self.data_manager = data_manager
        self.translator = translator
        self.current_filters = None

        self.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)
        self.setMinimumHeight(200) 

        self._init_ui()

    def _init_ui(self):
        layout = QVBoxLayout(self)
        layout.setContentsMargins(0,0,0,0) 

        self.chart = QChart()
        self.chart.setAnimationOptions(QChart.SeriesAnimations)

        self.chart_view = QChartView(self.chart)
        self.chart_view.setRenderHint(QPainter.Antialiasing)

        layout.addWidget(self.chart_view)
        self.update_chart_theme() 

    def update_chart(self, filters=None):
        self.current_filters = filters
        self.chart.removeAllSeries() 
        self.chart.setTitle("") 

        self.chart.setTitle(self.translator.translate("expense_summary_chart_title", "Expense Summary"))

        transactions_to_chart = self.data_manager.get_transactions(self.current_filters)

        expenses_by_category = defaultdict(float)
        total_filtered_expenses = 0.0
        for t in transactions_to_chart:
            if t.type == "expense":
                expenses_by_category[t.category] += t.amount
                total_filtered_expenses += t.amount

        if not expenses_by_category:
            self.chart.setTitle(self.translator.translate("no_data_for_chart", "No expense data to display for current filters."))
            if self.chart.legend():
                self.chart.legend().setVisible(False)
            if self.chart.series(): self.chart.removeAllSeries()
            self.chart_view.update()
            return

        series = QPieSeries()
        series.setHoleSize(0.35) 

        palette = [
            QColor("#4d99a6"), QColor("#69c0d1"), QColor("#ffb74d"),  
            QColor("#e57373"), QColor("#ba68c8"), QColor("#fff176"),  
            QColor("#7986cb"), QColor("#4dd0e1"), QColor("#aed581")   
        ]

        sorted_categories = sorted(expenses_by_category.items(), key=lambda item: item[1], reverse=True)

        slice_count = 0
        for category_key, total_amount in sorted_categories:
            if total_amount <= 0: continue 

            percentage = (total_amount / total_filtered_expenses) * 100 if total_filtered_expenses > 0 else 0

            amount_str = f"{total_amount:.2f}"
            translated_category = self.translator.translate(category_key)
            currency_sym = self.data_manager.get_display_currency_symbol()

            if QApplication.instance().layoutDirection() == Qt.RightToLeft:
                 slice_label_text = f"{translated_category}: {amount_str} {currency_sym} ({percentage:.1f}%)"
            else:
                 slice_label_text = f"{translated_category}: {currency_sym}{amount_str} ({percentage:.1f}%)"

            pie_slice = QPieSlice(slice_label_text, total_amount)
            pie_slice.setLabelVisible(True) 
            pie_slice.setColor(palette[slice_count % len(palette)])
            series.append(pie_slice)
            slice_count += 1

        self.chart.addSeries(series)

        if self.chart.legend() is None: # Check if legend needs to be created
            self.chart.createDefaultAxes() # For some chart types, not pie typically
            legend = self.chart.legend() # Get the legend
            if legend:
                 legend.setVisible(True)
                 legend.setAlignment(Qt.AlignBottom)
        else: # Legend exists
            self.chart.legend().setVisible(True)
            self.chart.legend().setAlignment(Qt.AlignBottom)

        self.update_chart_theme() 

    def update_chart_theme(self):
        theme_manager = QApplication.instance().theme_manager
        is_dark_theme = theme_manager.current_theme == "dark"

        app_font_family = QApplication.font().family()
        title_font = QFont(app_font_family, 11, QFont.Bold)
        legend_font = QFont(app_font_family, 9)
        slice_label_font = QFont(app_font_family, 8)

        text_color = QColor("#e0e0e0") if is_dark_theme else QColor("#333333")
        background_color = QColor("#262626") if is_dark_theme else QColor("#fafafa")
        slice_label_text_color = QColor(Qt.white) if is_dark_theme else QColor(Qt.black)

        self.chart.setTheme(QChart.ChartThemeDark if is_dark_theme else QChart.ChartThemeLight)
        self.chart.setBackgroundBrush(QBrush(background_color))
        self.chart.setTitleBrush(QBrush(text_color))
        self.chart.setTitleFont(title_font)

        if self.chart.legend(): 
            self.chart.legend().setLabelColor(text_color)
            self.chart.legend().setFont(legend_font)

        current_series_list = self.chart.series() 
        if current_series_list: 
            for s in current_series_list: 
                if isinstance(s, QPieSeries):
                    for pie_slice in s.slices():
                        pie_slice.setLabelBrush(QBrush(slice_label_text_color))
                        pie_slice.setLabelFont(slice_label_font)

        try:
            if self.chart.layout(): 
                 self.chart.layout().activate() 
        except AttributeError: 
            pass
        self.chart_view.update() 
