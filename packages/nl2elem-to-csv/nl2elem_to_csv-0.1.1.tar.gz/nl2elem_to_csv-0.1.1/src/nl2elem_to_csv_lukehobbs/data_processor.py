import math


def normalize_vector(vector):
    norm = math.sqrt(sum(i ** 2 for i in vector))
    return tuple(i / norm for i in vector)


def calculate_front_vector(point1, point2):
    return normalize_vector((point2['x'] - point1['x'], point2['y'] - point1['y'], point2['z'] - point1['z']))


def process_data(data):
    processed_data = []
    for i in range(len(data) - 1):
        roll = data[i]['roll']
        front = calculate_front_vector(data[i], data[i + 1])
        up = normalize_vector((roll['ux'], roll['uy'], roll['uz']))
        left = normalize_vector((roll['rx'], -roll['ry'], roll['rz']))
        processed_data.append({
            'pos': tuple([data[i]['x'], data[i]['y'], data[i]['z']]),
            'front': front,
            'up': up,
            'left': left,
        })

    processed_data.append({
        'pos': tuple([data[-1]['x'], data[-1]['y'], data[-1]['z']]),
        'front': processed_data[-2]['front'],
        'up': processed_data[-2]['up'],
        'left': processed_data[-2]['left'],
    })

    return processed_data
