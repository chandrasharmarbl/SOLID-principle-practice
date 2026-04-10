class Readable:
    def read(self):
        pass


class Writable:
    def write(self, data):
        pass


class ReadOnlyFile(Readable):
    def read(self):
        return "data"


class ReadWriteFile(Readable, Writable):
    def read(self):
        return "data"

    def write(self, data):
        print("Writing:", data)


if __name__ == '__main__':
    read_only = ReadOnlyFile()
    content = read_only.read()
    print(f"Read content: {content}")

    read_write = ReadWriteFile()
    read_write.write("New data")
    content = read_write.read()
    print(f"Read content: {content}")