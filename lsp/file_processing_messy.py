class File:
    def read(self):
        pass


class ReadOnlyFile(File):
    def read(self):
        return "data"

    def write(self):
        raise Exception("Cannot write")


if __name__ == '__main__':
    file = ReadOnlyFile()
    data = file.read()
    print(f"Read data: {data}")
    
    try:
        file.write()
    except Exception as e:
        print(f"Error: {e}")