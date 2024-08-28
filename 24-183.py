def read_file(file_name) -> str:
    with open(file_name) as file:
        f_content = file.read()
    
    return f_content


def write_file(file_name) -> None:
    with open(file_name, mode='w') as file:
        file.write(f'This is a new text\n')
        
        
def add_to_file(file_name) -> None:
    with open(file_name, mode='a') as file:
        file.write(f'This is an added text\n')


def main():
    file_content = read_file(FILE_NAME)
    print(file_content)

    write_file(FILE_NAME)
    add_to_file(FILE_NAME)
    

if __name__ == '__main__':
    FILE_NAME = '24-183.txt'
    
    main()
