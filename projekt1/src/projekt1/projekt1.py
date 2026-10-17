import requests
from datetime import datetime

def check_time_decorator(func):
    def wrapper(*args, **kwargs):
        start = datetime.now()
        print(f'[{start:%Y-%m-%d %H:%M:%S.%f}] - START')
        result = func(*args, **kwargs)
        end = datetime.now()
        print(f'[{end:%Y-%m-%d %H:%M:%S.%f}] - END')
        return result
    return wrapper

class ExampleOfETL:
    """Class to test ETL"""
    def __init__(self, file_url:str):
        self.file_url = file_url

    def extract(self):
        response = requests.get(self.file_url)
        if response.status_code == 404:
            raise NotFoundError(self.file_url)
        elif response.status_code == 403:
            raise AccessDeniedError(self.file_url)
        else:
            for line in response.text.splitlines():
                yield line

    def transform(self, row_data:list):
        for row in row_data:
            elements = row.split(',')
            rowId = elements[0]
            values = elements[1:]
            numbers = [float(v) for v in values if v != '-']
            missing = [i for i,v in enumerate(values) if v == '-']
            total = sum(numbers)
            mean = total / len(numbers) if numbers else 0
            result_positive = [rowId,total,mean]
            result_missing = []
            if len(missing) > 0:
                result_missing = [rowId, missing]
            yield [result_positive, result_missing]
            
    def load(self, results:list):
        with open("values.csv", "w") as file_positive, open("missing_values.csv", "w") as file_missing:            
            for r in results:
                file_positive.write(f'{r[0][0]},{r[0][1]},{r[0][2]}\n')
                if len(r[1]) > 0:
                    file_missing.write(f'{r[1][0]},{",".join(str(n) for n in r[1][1])}\n')

    @check_time_decorator
    def run(self):
        try:
            self.load(self.transform(self.extract()))
        except HttpAppError as e:
            print(e)
        except requests.RequestException as e:
            print(e)



class HttpAppError(Exception):
    """Main Class to catch HTTP errors"""

class NotFoundError(HttpAppError):
    """Class to catch 404 error"""
    def __init__(self, file_url:str):
        super().__init__(f'File {file_url} not found')

class AccessDeniedError(HttpAppError):
    """Class to catch 403 error"""
    def __init__(self, file_url:str):
            super().__init__(f'Access Denied for file: {file_url}')

###################################################################

file_url = input('Insert URL: ')

# For testing:
# file_url = 'http://oleksandr-fedoruk.com/sggw/podyplomowe/file'
# file_url = 'https://oleksandr-fedoruk.com/sggw/podyplomowe/404'
# file_url = 'https://oleksandr-fedoruk.com/sggw/podyplomowe/403'
# file_url = 'xxxxxxxxxxxxxxxxxxxxxx'

etl = ExampleOfETL(file_url)
etl.run()