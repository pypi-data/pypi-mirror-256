def write_to_csv(data, output):
    delimiter = '\t'
    with open(output, 'w') as file:
        # Write CSV header
        header = delimiter.join("No. PosX PosY PosZ FrontX FrontY FrontZ LeftX LeftY LeftZ UpX UpY UpZ".split())
        file.write(header + '\n')

        for index, node in enumerate(data):
            pos = delimiter.join(str(i) for i in node['pos'])
            front = delimiter.join(str(i) for i in node['front'])
            left = delimiter.join(str(i) for i in node['left'])
            up = delimiter.join(str(i) for i in node['up'])
            line = delimiter.join([str(index + 1), pos, front, left, up])
            if index < len(data) - 1:
                line += '\n'

            file.write(line)
