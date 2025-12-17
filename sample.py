import streamlit as st

# ========== Input Function ==========
def input_var(dataword, generator_polynomial):
    for i in dataword:
        if i not in '01':
            return -1, -1, "Dataword is not correct"
    for i in generator_polynomial:
        if i not in '01':
            return -1, -1, "Generator polynomial is not correct"
    return dataword, generator_polynomial, ""

# ========== Receiver Side ==========
def receiver_side(generator_polynomial, codeword, change, bit_num=0, positions=[]):
    log = "\n----------RECEIVER's SIDE----------\n"

    if change == "y":
        # ---- Fixed corruption logic ----
        codeword_list = list(codeword)
        for pos in positions:
            if 1 <= pos <= len(codeword_list):
                codeword_list[pos - 1] = '1' if codeword_list[pos - 1] == '0' else '0'
        codeword = ''.join(codeword_list)
        log += f"Codeword received by the receiver (corrupted): {codeword}\n"
    else:
        log += f"Codeword received by the receiver: {codeword}\n"

    log += f"Generator Polynomial : {generator_polynomial}\n"
    log += "_"*(len(codeword)+1) + "\n"
    log += codeword + "\n"

    for_range = len(codeword) - len(generator_polynomial) + 1

    for i in range(for_range):
        if i == 0:
            upper_operand = codeword[0:len(generator_polynomial)]
            if upper_operand[0] == '1':
                lower_operand = generator_polynomial
            else:
                lower_operand = len(generator_polynomial)*'0'
        else:
            upper_operand = XOR_output_for_upper_operand
            if XOR_output_for_upper_operand[0] == '1':
                lower_operand = generator_polynomial
            else:
                lower_operand = len(generator_polynomial)*'0'

        log += lower_operand + "\n"
        log += i*' ' + '_'*(len(generator_polynomial)+1) + "\n"
        log += i*' '

        XOR_output = ''
        for j in range(len(generator_polynomial)):
            if j == 0:
                XOR_output += 'X'
            elif upper_operand[j] == lower_operand[j]:
                XOR_output += '0'
            else:
                XOR_output += '1'

        if i < for_range-2:
            XOR_output += codeword[len(generator_polynomial)+i]
            log += XOR_output + "\n"
            log += (i+1)*' '
            XOR_output_for_upper_operand = XOR_output[1:]
        elif i == for_range-2:
            XOR_output += codeword[len(generator_polynomial)+i]
            log += XOR_output + "\n"
            log += (i+1)*' '
            XOR_output_for_upper_operand = XOR_output[1:]
        else:
            log += XOR_output + "\n"

    log += "\n"
    remainder = XOR_output[1:]
    log += f"remainder : {remainder}\n"
    if any(c != '0' for c in remainder):
        log += "Error detected! The remainder is not zero. The data is corrupt.\n"
    else:
        log += "No error detected. The remainder is all zeros.\n"
    return log


# ========== Sender Side ==========
def sender_side(dataword, generator_polynomial, change="n", bit_num=0, positions=[]):
    log = "\n----------SENDER's SIDE----------\n"
    initial_dividend = dataword + ((len(generator_polynomial)-1)*'0')
    log += f"Initial dividend : {initial_dividend}\n"
    log += "_"*(len(initial_dividend)+1) + "\n"
    log += initial_dividend + "\n"

    for_range = len(initial_dividend)-len(generator_polynomial)+1

    for i in range(for_range):
        if i == 0:
            upper_operand = initial_dividend[0:len(generator_polynomial)]
            if upper_operand[0] == '1':
                lower_operand = generator_polynomial
            else:
                lower_operand = len(generator_polynomial)*'0'
        else:
            upper_operand = XOR_output_for_upper_operand
            if XOR_output_for_upper_operand[0] == '1':
                lower_operand = generator_polynomial
            else:
                lower_operand = len(generator_polynomial)*'0'

        log += lower_operand + "\n"
        log += i*' ' + '_'*(len(generator_polynomial)+1) + "\n"
        log += i*' '

        XOR_output = ''
        for j in range(len(generator_polynomial)):
            if j == 0:
                XOR_output += 'X'
            elif upper_operand[j] == lower_operand[j]:
                XOR_output += '0'
            else:
                XOR_output += '1'

        if i < for_range-2:
            XOR_output += initial_dividend[len(generator_polynomial)+i]
            log += XOR_output + "\n"
            log += (i+1)*' '
            XOR_output_for_upper_operand = XOR_output[1:]
        elif i == for_range-2:
            XOR_output += initial_dividend[len(generator_polynomial)+i]
            log += XOR_output + "\n"
            log += (i+1)*' '
            XOR_output_for_upper_operand = XOR_output[1:]
        else:
            log += XOR_output + "\n"

    CRC = XOR_output[1:]
    log += f"\nCRC code : {CRC}\n"
    codeword = dataword+CRC
    log += f"Codeword : {codeword}\n"

    # call receiver side
    log += receiver_side(generator_polynomial, codeword, change, bit_num, positions)
    return log


# ========== STREAMLIT APP ==========
st.title("CRC Simulator")

dataword = st.text_input("Enter Dataword (binary):")
generator = st.text_input("Enter Generator Polynomial (binary):")

change = st.radio("Receiver: Is there any change in received codeword?", ("n", "y"))

bit_num = 0
positions = []
if change == "y":
    bit_num = st.number_input("Enter number of bits to be changed:", min_value=1, step=1)
    pos_str = st.text_input("Enter positions (comma separated):")
    if pos_str:
        positions = [int(x.strip()) for x in pos_str.split(",") if x.strip().isdigit()]

if st.button("Run CRC Simulation"):
    d, g, err = input_var(dataword, generator)
    if d == -1:
        st.error(err)
    else:
        log = sender_side(d, g, change, bit_num, positions)
        st.text(log)
