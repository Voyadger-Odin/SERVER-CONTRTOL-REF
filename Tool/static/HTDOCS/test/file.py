

def formatCarriage(data):
    data_lines = data.split('\n')

    result = ''
    for i in range(len(data_lines)):
        data_s = data_lines[i].split('\r')

        result_line = ''
        for line in data_s[::-1]:
            if len(line) > len(result_line):
                result_line += line[len(result_line):]

        if (i > 0):
            result += '\n'
        result += result_line

    return result


with open('file.txt', 'w') as file:
    data = '12345\rabc\n123'
    print(data)
    data = f'{data}'
    print([data])
    data = formatCarriage(data)
    print('-'*5)
    print(data)
    file.write(data)