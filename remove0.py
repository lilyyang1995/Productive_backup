with open(r'C:\Users\yuzeyang\Desktop\productive\mat_to_fpga0.txt', 'r') as f_in:
    with open(r'C:\Users\yuzeyang\Desktop\productive\output.txt', 'w') as f_out:
        for line in f_in:
            new_line = ' '.join([num[1:] for num in line.split()])
            f_out.write(new_line + '\n')