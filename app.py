import streamlit as st
import math
import re

# Configure the page
st.set_page_config(
    page_title="Full-Fledged Calculator by Hafiz Subhan",
    page_icon="🧮",
    layout="centered",
    initial_sidebar_state="collapsed"
)

# Custom CSS for better styling
st.markdown("""
<style>
    .main-header {
        text-align: center;
        color: #2E86AB;
        font-size: 2.5rem;
        margin-bottom: 2rem;
    }

    .calculator-container {
        background-color: #f8f9fa;
        padding: 2rem;
        border-radius: 15px;
        box-shadow: 0 4px 6px rgba(0, 0, 0, 0.1);
        margin: 1rem 0;
    }

    .display-area {
        background-color: #2c3e50;
        color: #ecf0f1;
        padding: 1rem;
        border-radius: 10px;
        font-family: 'Courier New', monospace;
        font-size: 1.5rem;
        text-align: right;
        margin-bottom: 1rem;
        min-height: 60px;
        display: flex;
        align-items: center;
        justify-content: flex-end;
    }

    .stButton > button {
        width: 100%;
        height: 60px;
        font-size: 1.2rem;
        font-weight: bold;
        border-radius: 10px;
        margin: 2px;
    }

    .operator-btn > button {
        background-color: #e74c3c !important;
        color: white !important;
    }

    .number-btn > button {
        background-color: #3498db !important;
        color: white !important;
    }

    .function-btn > button {
        background-color: #9b59b6 !important;
        color: white !important;
    }

    .special-btn > button {
        background-color: #f39c12 !important;
        color: white !important;
    }
</style>
""", unsafe_allow_html=True)

# Initialize session state
if 'display' not in st.session_state:
    st.session_state.display = "0"
if 'expression' not in st.session_state:
    st.session_state.expression = ""
if 'last_operation' not in st.session_state:
    st.session_state.last_operation = None
if 'memory' not in st.session_state:
    st.session_state.memory = 0

def clear_display():
    st.session_state.display = "0"
    st.session_state.expression = ""

def clear_all():
    clear_display()
    st.session_state.memory = 0

def add_to_expression(value):
    if st.session_state.display == "0" and value.isdigit():
        st.session_state.display = value
        st.session_state.expression = value
    else:
        if st.session_state.display == "0":
            st.session_state.display = value
            st.session_state.expression = value
        else:
            st.session_state.display += value
            st.session_state.expression += value

def calculate_result():
    try:
        # Replace mathematical functions for evaluation
        expression = st.session_state.expression

        # Handle mathematical functions
        expression = expression.replace('sin(', 'math.sin(math.radians(')
        expression = expression.replace('cos(', 'math.cos(math.radians(')
        expression = expression.replace('tan(', 'math.tan(math.radians(')
        expression = expression.replace('log(', 'math.log10(')
        expression = expression.replace('ln(', 'math.log(')
        expression = expression.replace('sqrt(', 'math.sqrt(')
        expression = expression.replace('^', '**')
        expression = expression.replace('π', str(math.pi))
        expression = expression.replace('e', str(math.e))

        # Close any unclosed parentheses for trig functions
        open_parens = expression.count('(')
        close_parens = expression.count(')')
        if open_parens > close_parens:
            expression += ')' * (open_parens - close_parens)

        result = eval(expression)

        # Format the result
        if isinstance(result, float):
            if result.is_integer():
                result = int(result)
            else:
                result = round(result, 10)

        st.session_state.display = str(result)
        st.session_state.expression = str(result)

    except Exception as e:
        st.session_state.display = "Error"
        st.session_state.expression = ""

def add_function(func_name):
    if st.session_state.display == "0":
        st.session_state.display = func_name + "("
        st.session_state.expression = func_name + "("
    else:
        st.session_state.display += func_name + "("
        st.session_state.expression += func_name + "("

def memory_add():
    try:
        current_value = float(st.session_state.display)
        st.session_state.memory += current_value
    except:
        pass

def memory_subtract():
    try:
        current_value = float(st.session_state.display)
        st.session_state.memory -= current_value
    except:
        pass

def memory_recall():
    st.session_state.display = str(st.session_state.memory)
    st.session_state.expression = str(st.session_state.memory)

def memory_clear():
    st.session_state.memory = 0

# Main app
st.markdown('<h1 class="main-header">🧮 Full-Fledged Calculator</h1>', unsafe_allow_html=True)

# Calculator container
with st.container():
    st.markdown('<div class="calculator-container">', unsafe_allow_html=True)

    # Display area
    st.markdown(f'<div class="display-area">{st.session_state.display}</div>', unsafe_allow_html=True)

    # Memory indicator
    if st.session_state.memory != 0:
        st.info(f"Memory: {st.session_state.memory}")

    # Button layout
    col1, col2, col3, col4, col5 = st.columns(5)

    # Row 1: Memory and Clear functions
    with col1:
        if st.button("MC", key="mc", help="Memory Clear"):
            memory_clear()
    with col2:
        if st.button("MR", key="mr", help="Memory Recall"):
            memory_recall()
    with col3:
        if st.button("M+", key="m_add", help="Memory Add"):
            memory_add()
    with col4:
        if st.button("M-", key="m_sub", help="Memory Subtract"):
            memory_subtract()
    with col5:
        if st.button("AC", key="ac", help="All Clear"):
            clear_all()

    # Row 2: Scientific functions
    col1, col2, col3, col4, col5 = st.columns(5)
    with col1:
        if st.button("sin", key="sin"):
            add_function("sin")
    with col2:
        if st.button("cos", key="cos"):
            add_function("cos")
    with col3:
        if st.button("tan", key="tan"):
            add_function("tan")
    with col4:
        if st.button("log", key="log"):
            add_function("log")
    with col5:
        if st.button("ln", key="ln"):
            add_function("ln")

    # Row 3: More functions
    col1, col2, col3, col4, col5 = st.columns(5)
    with col1:
        if st.button("√", key="sqrt"):
            add_function("sqrt")
    with col2:
        if st.button("x²", key="square"):
            add_to_expression("^2")
    with col3:
        if st.button("x^y", key="power"):
            add_to_expression("^")
    with col4:
        if st.button("π", key="pi"):
            add_to_expression("π")
    with col5:
        if st.button("e", key="euler"):
            add_to_expression("e")

    # Row 4: Numbers and operators
    col1, col2, col3, col4, col5 = st.columns(5)
    with col1:
        if st.button("(", key="open_paren"):
            add_to_expression("(")
    with col2:
        if st.button(")", key="close_paren"):
            add_to_expression(")")
    with col3:
        if st.button("C", key="clear"):
            clear_display()
    with col4:
        if st.button("⌫", key="backspace"):
            if len(st.session_state.display) > 1:
                st.session_state.display = st.session_state.display[:-1]
                st.session_state.expression = st.session_state.expression[:-1]
            else:
                st.session_state.display = "0"
                st.session_state.expression = ""
    with col5:
        if st.button("÷", key="divide"):
            add_to_expression("/")

    # Row 5: Numbers 7-9 and multiply
    col1, col2, col3, col4, col5 = st.columns(5)
    with col1:
        if st.button("7", key="7"):
            add_to_expression("7")
    with col2:
        if st.button("8", key="8"):
            add_to_expression("8")
    with col3:
        if st.button("9", key="9"):
            add_to_expression("9")
    with col4:
        if st.button("×", key="multiply"):
            add_to_expression("*")
    with col5:
        if st.button("1/x", key="reciprocal"):
            try:
                current = float(st.session_state.display)
                result = 1 / current
                st.session_state.display = str(result)
                st.session_state.expression = str(result)
            except:
                st.session_state.display = "Error"

    # Row 6: Numbers 4-6 and subtract
    col1, col2, col3, col4, col5 = st.columns(5)
    with col1:
        if st.button("4", key="4"):
            add_to_expression("4")
    with col2:
        if st.button("5", key="5"):
            add_to_expression("5")
    with col3:
        if st.button("6", key="6"):
            add_to_expression("6")
    with col4:
        if st.button("−", key="subtract"):
            add_to_expression("-")
    with col5:
        if st.button("±", key="plus_minus"):
            try:
                current = float(st.session_state.display)
                result = -current
                st.session_state.display = str(result)
                st.session_state.expression = str(result)
            except:
                pass

    # Row 7: Numbers 1-3 and add
    col1, col2, col3, col4, col5 = st.columns(5)
    with col1:
        if st.button("1", key="1"):
            add_to_expression("1")
    with col2:
        if st.button("2", key="2"):
            add_to_expression("2")
    with col3:
        if st.button("3", key="3"):
            add_to_expression("3")
    with col4:
        if st.button("+", key="add"):
            add_to_expression("+")
    with col5:
        if st.button("!", key="factorial"):
            try:
                current = int(float(st.session_state.display))
                result = math.factorial(current)
                st.session_state.display = str(result)
                st.session_state.expression = str(result)
            except:
                st.session_state.display = "Error"

    # Row 8: Zero, decimal, and equals
    col1, col2, col3, col4, col5 = st.columns(5)
    with col1:
        if st.button("0", key="0"):
            add_to_expression("0")
    with col2:
        if st.button("00", key="00"):
            add_to_expression("00")
    with col3:
        if st.button(".", key="decimal"):
            if "." not in st.session_state.display.split()[-1]:
                add_to_expression(".")
    with col4:
        if st.button("=", key="equals"):
            calculate_result()
    with col5:
        if st.button("%", key="percent"):
            try:
                current = float(st.session_state.display)
                result = current / 100
                st.session_state.display = str(result)
                st.session_state.expression = str(result)
            except:
                st.session_state.display = "Error"

    st.markdown('</div>', unsafe_allow_html=True)

# Instructions
with st.expander("📖 How to Use"):
    st.markdown("""
    **Basic Operations:**
    - Use number buttons (0-9) to input numbers
    - Use +, −, ×, ÷ for basic arithmetic
    - Press = to calculate the result
    - Use C to clear current input, AC to clear everything

    **Scientific Functions:**
    - **sin, cos, tan**: Trigonometric functions (input in degrees)
    - **log**: Base-10 logarithm
    - **ln**: Natural logarithm
    - **√**: Square root
    - **x²**: Square the current number
    - **x^y**: Raise x to the power of y
    - **π**: Insert pi (3.14159...)
    - **e**: Insert Euler's number (2.71828...)
    - **!**: Factorial
    - **1/x**: Reciprocal
    - **±**: Change sign
    - **%**: Convert to percentage

    **Memory Functions:**
    - **MC**: Clear memory
    - **MR**: Recall memory value
    - **M+**: Add current display to memory
    - **M-**: Subtract current display from memory

    **Other Features:**
    - Use parentheses ( ) for grouping operations
    - ⌫ for backspace
    - Supports complex mathematical expressions
    """)

# Footer
st.markdown("---")
st.markdown("**Built with Streamlit** | Full-featured calculator with scientific functions")