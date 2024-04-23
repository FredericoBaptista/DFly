def convert_hex_to_int(hex_num):
    return int(hex_num, 16)


def convert_file():
    try:
        with open('merkle_tree/cache/MerkleTree.txt', 'r') as input_file:
            with open('merkle_tree/cache/ConvertedTree.txt', 'w') as output_file:
                for line in input_file:
                    hex_nums = line.strip().split(',')
                    int_nums = [convert_hex_to_int(
                        hex_num) for hex_num in hex_nums]
                    output_file.write(','.join(map(str, int_nums)))
                    output_file.write('\n')
    except FileNotFoundError:
        print('File not found. Please make sure the input file exists and its name is correctly spelled.')
    except Exception as e:
        print('An error occurred: ', str(e))


convert_file()
