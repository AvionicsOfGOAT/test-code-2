import datetime

class DataFile:
    def __init__(self, file_name):
        file_name_with_date = self.add_date_to_file_name(file_name)
        self.file = open(file_name_with_date, 'w')

    def add_date_to_file_name(self, filename):
        now_date = str(datetime.datetime.now())
        return now_date[:21]+" "+filename
    
    def save(self, data):
        try:
            now_date = str(datetime.datetime.now())
            self.file.write("timestamp: " + now_date + " data: " + str(data) + '\n')
        except IOError as e:
            print(f"Error saving data: {e}")
    
