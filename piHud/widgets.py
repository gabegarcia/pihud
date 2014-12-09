import pygal
from pygal.style import Style
from SVGWidget import SVGWidget
from PyQt4 import QtCore, QtGui


class Gauge(SVGWidget):
    def __init__(self, parent, config):
        super(Gauge, self).__init__(parent, config)

        self.style = Style(
            stroke_width=3.0,
            background='transparent',
            plot_background='transparent',
            foreground=config.color,
            foreground_light=config.color,
            foreground_dark='transparent',
            colors=(config.color,))


    def default_dimensions(self):
        """ override default size, called by superclass """
        super(Gauge, self).setFixedWidth(375)
        super(Gauge, self).setFixedHeight(400)


    def render(self, response):
        """ function called by python-OBD with new data to be rendered """
        
        chart = pygal.Gauge()
        
        # styling
        chart.style = self.style
        chart.margin = 20
        chart.show_legend = False
        chart.print_values = False # the value number on top of the needle
        chart.title = self.config.title
        chart.range = [self.config.min, self.config.max]

        value = 0
        if not response.is_null():
            value = response.value

        chart.add(self.command.name, value)

        self.showChart(chart)



class Bar_h(SVGWidget):
    def __init__(self, parent, config):
        super(Bar_h, self).__init__(parent, config)

        self.style = Style(
            stroke_width=1.0,
            background='transparent',
            plot_background='transparent',
            foreground=config.color,
            foreground_light=config.color,
            foreground_dark='transparent',
            colors=(config.color,))


    def default_dimensions(self):
        """ override default size, called by superclass """
        super(Bar_h, self).setFixedWidth(100)
        super(Bar_h, self).setFixedHeight(400)


    def render(self, response):
        """ function called by python-OBD with new data to be rendered """
        
        chart = pygal.Bar()
        
        # styling
        chart.style = self.style

        chart.margin = 30

        #chart.print_values = False # the value number on top of the needle
        chart.title = self.config.title
        chart.range = [self.config.min, self.config.max]

        value = 0
        if not response.is_null():
            value = response.value

        chart.add(self.command.name, value)

        self.showChart(chart)





class Graph(SVGWidget):
    def __init__(self, parent, config):
        super(Graph, self).__init__(parent, config)

        self.buffer = [0] * config.buffer_size

        self.style = Style(
            stroke_width=3.0,
            background='transparent',
            plot_background='transparent',
            foreground=config.color,
            foreground_light=config.color,
            foreground_dark='transparent',
            colors=(config.color,))


    def default_dimensions(self):
        """ override default size, called by superclass """
        super(Graph, self).setFixedWidth(400)
        super(Graph, self).setFixedHeight(300)


    def render(self, response):
        """ function called by python-OBD with new data to be rendered """
        

        chart = pygal.Line(fill=False)
        
        # styling
        chart.style = self.style
        chart.show_dots = False
        # chart.y_labels = [0,50,100,150]
        chart.fill = False
        chart.title = self.config.title
        chart.range = [self.config.min, self.config.max]

        value = 0
        if not response.is_null():
            value = response.value

        # add the new data to the buffer
        self.buffer = [value] + self.buffer[:-1]

        chart.add(self.command.name, self.buffer)

        self.showChart(chart)





class Text(SVGWidget):
    def __init__(self, parent, config):
        super(Text, self).__init__(parent, config)

        self.label = QtGui.QLabel(self)
        self.label.setText("Label")

        css = """
            font-size: %ipt;
            color: %s;
        """ % (config.label_font_size, config.color)

        self.label.setStyleSheet(css)


    def default_dimensions(self):
        """ override default size, called by superclass """
        super(Text, self).setFixedWidth(200)
        super(Text, self).setFixedHeight(75)


    def render(self, response):
        """ function called by python-OBD with new data to be rendered """

        value = 0
        if not response.is_null():
            value = response.value

        self.label.setText(str(value) + str(response.unit))

