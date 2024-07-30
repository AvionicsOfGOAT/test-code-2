import datetime

class DataFile:
    def __init__(self, file_name):
        self.file_name = self.add_date_to_file_name(file_name)
        self.file = open(self.file_name, 'a+')

    def add_date_to_file_name(self, filename):
        now_date = datetime.datetime.now().strftime('%Y-%m-%d_%H-%M-%S')
        return f"{now_date}_{filename}"
    
    def save(self, data):
        try:
            now_date = str(datetime.datetime.now())
            self.file.write(f"timestamp: {now_date} data: {data}\n")
            self.file.flush()
        except IOError as e:
            print(f"Error saving data: {e}")

    def get_last(self):
        try:
            self.file.seek(0, 2)
            buffer = bytearray()
            self.file.seek(self.file.tell() - 1)
            
            while self.file.tell() > 0:
                char = self.file.read(1)
                if char == b'\n' and buffer:
                    break
                buffer.extend(char)
                self.file.seek(self.file.tell() - 2, 0)
            
            last_line = buffer[::-1].decode()
            data_part = last_line.split('data:')[-1].strip()
            return data_part
        
        except (IOError, IndexError) as e:
            print(f"Error reading file: {e}")
            return None