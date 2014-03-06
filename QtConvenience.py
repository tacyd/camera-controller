from PyQt4 import QtGui, QtCore

QtAlignmentLookup = {}
QtAlignmentLookup['top'] = QtCore.Qt.AlignTop
QtAlignmentLookup['bottom'] = QtCore.Qt.AlignBottom

def make_label(text, wordwrap=True, bold=False, height=None,
               align=None):
    label = QtGui.QLabel()
    label.setText(text)
    if wordwrap:
        label.setWordWrap(True)
    if bold:
        label.setStyleSheet('font-weight:bold')
    if height:
        label.setFixedHeight(height)
    if align:
        if not isinstance(align, QtCore.Qt.AlignmentFlag):
            align = QtAlignmentLookup[align]
        label.setAlignment(align)
    return label


def make_VBox(items, parent=None):
    return fill_layout(QtGui.QVBoxLayout(parent), items)


def make_HBox(items, parent=None):
    return fill_layout(QtGui.QHBoxLayout(parent), items)


def fill_layout(layout, items):
    for item in items:
        if isinstance(item, int):
            layout.addStretch(item)
        elif isinstance(item, QtGui.QBoxLayout):
            layout.addLayout(item)
        else:
            if isinstance(item, basestring):
                item = make_label(item)
            layout.addWidget(item)
    return layout

def make_button(label, callback, parent, shortcut=None, height=50, width=100,
                tooltip=None):
    """
    Handle the common boilerplate for creating buttons

    Parameters
    ----------
    label : string
        The label to display on the button
    callback : function
        The function to call when the button is clicked
    parent : QtGui.QWidget
        the parent widget
    height, width : int
        The dimensions of the button
    tooltip : string
        A tooltip for the button
    """
    button = QtGui.QPushButton(label, parent)
    button.clicked.connect(callback)
    if height:
        button.setFixedHeight(height)
    if width:
        button.setFixedWidth(width)
    if shortcut is not None:
        button.setShortcut(shortcut)
    if tooltip is not None:
        button.setToolTip(tooltip)
    return button

def make_checkbox(label, start_checked=False, callback=None):
    checkbox = QtGui.QCheckBox()
    checkbox.setText(label)
    if start_checked:
        checkbox.toggle()
    if callback:
        checkbox.stateChanged.connect(callback)
    return checkbox

def make_combobox(items, callback, width=150, default=None):
    box = QtGui.QComboBox()
    for item in items:
        box.addItem(item)
    if default is not None:
        box.setCurrentIndex(default)
    if width is not None:
        box.setFixedWidth(150)
    if callback is not None:
        box.activated[str].connect(callback)
    return box

def make_control_group(parent, buttons, exclusive=True, default=None):
    controlgroup = QtGui.QButtonGroup(QtGui.QWidget(parent))
    for button in buttons:
        controlgroup.addButton(button)
        button.setCheckable(True)
    if default is not None:
        default.toggle()
    controlgroup.setExclusive(exclusive)
    return controlgroup

def make_LineEdit(starting_text=None, callback=None, width=None):
    line = QtGui.QLineEdit()
    if starting_text:
        line.setText(starting_text)
    if width:
        line.setFixedWidth(width)
    if callback:
        line.textChanged.connect(callback)
    return line

class CheckboxGatedValue(QtGui.QHBoxLayout):
    """A checkbox and value together.

    The value can either be generated by a function, or be the value
    of a text box. This widget acts like a checkbox and a (optionally)
    a line edit together. If the checkbox is not checked, it will
    return an empty string as the text

    """
    def __init__(self, text, value, callback=None,
                 default_checked=False):
        super(CheckboxGatedValue, self).__init__()
        self.checkbox = make_checkbox(text, default_checked, callback=callback)
        self.addWidget(self.checkbox)
        self._value = value
        if isinstance(self._value, QtGui.QLineEdit):
            self.addWidget(self._value)
            if callback:
                self._value.textChanged.connect(callback)

    def setCheckState(self, value):
        self.checkbox.setCheckState(value)

    def text(self):
        if not self.checkbox.isChecked():
            return ""
        if isinstance(self._value, QtGui.QWidget):
            return str(self._value.text())
        else:
            return self.value()

    def setText(self, value):
        self._value.setText(value)

    def isChecked(self):
        return self.checkbox.isChecked()

    def setChecked(self, value):
        self.checkbox.setChecked(value)

def increment_textbox(textbox):
    old = textbox.text()
    digits = len(old)
    textbox.setText(str(int(old)+1).zfill(digits))

def zero_textbox(textbox):
    textbox.setText(str(0).zfill(len(textbox.text())))

def textbox_int(textbox):
    return int(str(textbox.text()))

def textbox_float(textbox):
    return float(str(textbox.text()))
