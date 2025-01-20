input_file_path = r'e:\UNI\HW Proje\sensor_data.txt'
output_file_path = r'e:\UNI\HW Proje\reformatted_sensor_data.txt'

def rewrite_data_frames(input_file, output_file):
    with open(input_file, 'r') as infile, open(output_file, 'w') as outfile:
        data = infile.read()
        frames = data.split('AA FF 03 00')[1:]  # Split and ignore the first empty element
        for frame in frames:
            frame = 'AA FF 03 00 ' + frame.strip()
            print(frame)
            outfile.write(frame + '\n')

rewrite_data_frames(input_file_path, output_file_path)