class Logger:
    def __init__(self):
        pass

    def __enter__(self):
        print('Start sekcji logowania')

    def __exit__(self, exc_type, exc, tb):
        print('Koniec sekcji logowania')

class FileWriter:
    def __init__(self, path:str):
        self.path = path
        self.file = None

    def __enter__(self):
        self.file = open(self.path, 'w')
        return self.file

    def __exit__(self, exc_type, exc, tb):
        if self.file is not None:
            self.file.close()
        
        if exc_type is not None:
            print(f'Błąd podczas zapisu: {exc}')
        
        return False

class SafeDivision:
    def __enter__(self):
        return self

    def divide(self, a, b):
        return a / b

    def __exit__(self, exc_type, exc, tb):
        if exc_type is ZeroDivisionError:
            print('Nie można dzielić przez zero!')
            return True
        return False
        
with Logger() as lg:
    print('czy wszystko ok?')

with  FileWriter('text.txt') as file:
    file.write('First line\n')
    file.write('Second line')

with SafeDivision() as division:
    print(division.divide(10, 2))
    print(division.divide(10, 0))
    print(division.divide(20, 4))

with  FileWriter('text2.txt') as file:
    file.write(123)