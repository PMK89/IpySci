%matplotlib inline
import numpy as np
import sympy as sp
import matplotlib.pyplot as plt
import ipywidgets as widgets
from bqplot import pyplot as bqp
from bqplot.interacts import panzoom
from IPython.core.display import display, HTML
display(HTML("<style>.container { width:100% !important; }.widget-htmlmath-content {width:700px !important;} </style>"))
plt.style.use('ggplot')
sp.init_printing()

# graphing classes

# line class
class is_line:
    def __init__(self, x_data, y_data, expr, x_sc, y_sc):
        self.x_data = x_data
        self.y_data = y_data
        self.x_sc = x_sc
        self.y_sc = y_sc
        self.expr = expr

# graph class
class is_graph:
    active = False
    position = 3
    x_min=-1
    x_max=1
    x_log=False
    y_log=False
    y_grid=False
    x_grid=False
    pi_bool=False
    axes0=False
    x_steps = 100
    def __init__(self, x_label='X', y_label='Y', title_label='Title', pi_bool=pi_bool,\
                 x_min=x_min, x_max=x_max, x_log=x_log, y_log=y_log, x_steps=x_steps,\
                 x_grid=x_grid, y_grid=y_grid, axes0=axes0):
        self.x_label = x_label
        self.y_label = y_label
        self.title_label = title_label
        self.x_min = x_min
        self.x_max = x_max
        self.x_log = x_log
        self.y_log = y_log
        self.x_grid = x_grid
        self.y_grid = y_grid
        self.pi_bool = pi_bool
        self.axes0 = axes0
        selfx_steps = x_steps
        self.lines = []

    def addline(self, x_data, y_data, expr, x_sc, y_sc):
        self.lines.append(is_line(x_data, y_data))

#global variables
x, y, z, t = sp.symbols("x y z t")
ilim_max = sp.oo
ilim_min = -sp.oo
vardif = x
multdif = 1
xpoint = 0
utol = 100
ltol = -100

expr = x
expr_0 = x
expr_1 = x
expr_2 = x
expr_str = str(expr)
expr_array = []
activeexpr = 0
activeexprlist = []
color_array = ['#0033cc', '#ff3300', '#33cc33', '#00ffcc', '#ff66cc', '#ff6600']
matrixinput = []
history_list = widgets.HTMLMath(
    value=r'Equations<br>',
    placeholder='Equations',
    layout = widgets.Layout(flex_wrap='nowrap', min_width='700px', max_height='450px', overflow_y='scroll'),
)
plot_array = []
fig1 = bqp.Figure(title='Graph 1')
fig2 = bqp.Figure(title='Graph 2')
fig3 = bqp.Figure(title='Graph 3')
active_plot = 'fig1'
default_graph_settings = False

# makes a numerical computation of sympy equation
def npfy(x_, x_data, expr_):
    f = sp.lambdify(x_, expr_, 'numpy')
    y_data = f(x_data)
    y_data[y_data>utol] = np.inf
    y_data[y_data<ltol] = -np.inf
    return y_data

# changes variable for differentiation and integration
def setvardif(self):
    global vardif
    if difint_dropdown.value is 'x':
        vardif = x
    elif difint_dropdown.value is 'y':
        vardif = y
    elif difint_dropdown.value is 'z':
        vardif = z
    elif difint_dropdown.value is 't':
        vardif = t

# changes variable for differentiation and integration
def set_vardif(self):
    global vardif
    try:
        vardif0 = sp.simpyfy(difint_input.value)
        vardif = vardif0
    except:
        print('Invalid value: ', difint_input)

# changes variable for differentiation and integration
def setmultdif(self):
    global multdif
    try:
        multdif = int(multdif_input.value)
        if multdif <= 0:
            multdif = 1
            print('Positive integer nedded, got: ', multdif_input.value)
    except:
        multdif = 1
        print('Positive integer nedded, got: ', multdif_input.value)

# convert input to numerical values or sympy
def convertinput(input):
    try:
        return float(input)
    except:
        try:
            return sp.simpify(input)
        except:
            print('No valid input: ', input)
            return False

# changes limits for integration
def setilim(self):
    global ilim_min
    global ilim_max
    ilim_min0 = convertinput(ilim_min_input.value)
    if ilim_min0:
        ilim_min = ilim_min0
    ilim_max0 = convertinput(ilim_max_input.value)
    if ilim_max0:
        ilim_max = ilim_max0

# changes tolerance limits for plotting
def settol(self):
    global ltol
    global utol
    ltol0 = convertinput(ltol_input.value)
    if ltol0:
        if ltol0 == -sp.oo:
            ltol = -np.inf
        else:
            ltol = ltol0
    utol0 = convertinput(utol_input.value)
    if utol0:
        if utol0 == sp.oo:
            utol = np.inf
        else:
            utol = utol0

# set a point for expansion or limit
def setpoint(self):
    global xpoint
    xpoint0 = convertinput(xpoint_input.value)
    if xpoint0:
        xpoint = xpoint0

# shows the equation
def add_history():
    global expr_array
    global history_list
    history_list.value += str(len(expr_array)) + ' \(' + sp.latex(expr_array[-1]) + '\)' '<br>'
    eq_dropdown.options = [i + 1 for i, item in enumerate(expr_array)]
    return history_list

# clears the equations history
def clear_history(self):
    global history_list
    global expr_array
    history_list.value = r'Equations<br>'
    expr_array = []
    eq_dropdown.options = [0]

# sets choosen expresion active
def setactivegraph(self):
    global active_plot
    active_plot = active_dropdown.value
    if active_plot is 'fig1':
        plot = fig_array[0]
    elif active_plot is 'fig2':
        plot = fig_array[1]
    elif active_plot is 'fig3':
        plot = fig_array[2]
    if plot:
        global pi_bool_input
        global title_label_input
        global x_label_input
        global y_label_input
        global x_steps_input
        global x_min_input
        global x_max_input
        pi_bool_input.value = plot.pi_bool
        x_grid_input.value = plot.x_grid
        y_grid_input.value = plot.y_grid
        axes0_input.value = plot.axes0
        title_label_input.value = plot.title_label
        x_label_input.value = plot.x_label
        y_label_input.value = plot.y_label
        x_steps_input.value = str(plot.x_steps)
        x_min_input.value = str(plot.x_min)
        x_max_input.value = str(plot.x_max)

#sets choosen expresion active
def setactiveexpr(self):
    global activeexprlist
    global expr_str
    pos = int(eq_dropdown.value) - 1
    if pos >= 0:
        expr = expr_array[pos]
        expr_str = str(expr)
        expr_input.value = expr_str

#sets choosen expresion active
def setactive(self):
    global expr
    global expr_str
    pos = int(eq_dropdown.value) - 1
    if pos >= 0:
        expr = expr_array[pos]
        expr_str = str(expr)
        expr_input.value = expr_str

#appends expression array and updates output
def expr_array_append(expr0):
    global expr_array
    global expr
    if len(expr_array) > 0:
        if expr_array[-1] is not expr0 and expr_array[0] is not expr0:
            expr_str = str(expr)
            eq_out0.value = r'\(' + sp.latex(expr) + '\)'
            expr_array.append(expr0)
            expr = expr0
            add_history()
    else:
        expr_str = str(expr)
        eq_out0.value = r'\(' + sp.latex(expr) + '\)'
        expr_array.append(expr)
        add_history()

#reads and validates user input
def addexpr(change):
    global expr_str
    global expr
    if expr_input.value is not '' and expr_input.value is not None:
        try:
            addexpr = sp.sympify(expr_input.value)
            expr = expr + addexpr
            expr_array_append(expr)
            return expr
        except:
            eq_out0.value = r'Invalid Expression!'
            return 'Invalid Expression!'

#reads and validates user input
def readexpr(change):
    global expr_str
    global expr
    global expr_array
    if expr_input.value is not '' and expr_input.value is not None:
        try:
            expr = sp.sympify(expr_input.value)
            expr_array_append(expr)
            return expr
        except:
            eq_out0.value = r'Invalid Expression!'
            return 'Invalid Expression!'

#reads and validates user input
def readmatrix(change):
    global matrixinput
    global expr
    global expr_array
    mmax = 0
    nmax = 0
    mlist = []
    spok = True
    for m, m_row in enumerate(matrixinput):
        nlist = []
        for n, m_cell in enumerate(m_row):
            if m_cell.value is not '' and m_cell.value is not None:
                spcell = convertinput(m_cell.value)
                if spcell:
                    mlist.append(spcell)
                else:
                    spok = False
                if (n + 1) > nmax:
                    nmax = n + 1
            else:
                mlist.append(0)
        if nmax > 0:
            mmax = m + 1
        mlist.append(nlist)
    if spok:
        mlist = mlist[:mmax]
        for i in range(mmax):
            mlist[i] = mlist[i][:nmax]
        spmatrix = sp.Matrix(mlist)
        return spmatrix
    else:
        retuurn False

# simplify equation
def simplify(self):
    sexpr = sp.simplify(expr)
    eq_out1.value = r'\(' + sp.latex(sexpr) + '\)'
    expr_array_append(sexpr)

# obtain the expression’s numeric value
def numval(self):
    nexpr = expr.n()
    eq_out1.value = r'\(' + sp.latex(nexpr) + '\)'
    expr_array_append(sexpr)

# solve equation
def solve(self):
    slexpr = sp.solve(expr, vardif)
    eq_out1.value = r'\(' + sp.latex(slexpr) + '\)'
    expr_array_append(sexpr)

    # expands equation
def expand(self):
    eexpr = sp.expand(expr)
    eq_out1.value = r'\(' + sp.latex(eexpr) + '\)'
    expr_array_append(eexpr)

# substitute a variable
def substitute(self):
    subexpr = sp.sympify(expr_input.value)
    pos = int(eq_dropdown.value) - 1
    if pos >= 0:
        expr0 = expr_array[pos]
        exprsub = expr0.subs(vardif, subexpr)
        eq_out1.value = r'\(' + sp.latex(exprsub) + '\)'
        expr_array_append(exprsub)
