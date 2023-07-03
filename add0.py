# 打开原始文件
with open(r'C:\Users\yuzeyang\Desktop\productive\expected_threshold.txt', 'r') as f:
    # 读取每一行数据
    lines = f.readlines()

# 处理每一行数据
new_lines = []
for line in lines:
    # 在每一行数据前面加上00000
    new_line = '00000' + line
    # 添加到处理后的数据列表中
    new_lines.append(new_line)

# 写入新文件
with open(r'C:\Users\yuzeyang\Desktop\productive\output_threshold.txt', 'w') as f:
    for line in new_lines:
        f.write(line)

print("finish")