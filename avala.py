from random import SystemRandom
import json
from sre_parse import HEXDIGITS




class TwoFactorAuthentication:
    def __init__(self):
        self.__code__ = None
        self.HEX_DIGITS = 8
        with open('data.json', 'r') as fp:
            self.hexspeaks = json.load(fp)
    @staticmethod
    def generate(random_chars=8 , alphabet="0123456789ABCDEF"):
        r =SystemRandom()
        return ''.join([r.choice(alphabet) for i in range(random_chars)])
    
    @staticmethod
    def get_linear_equation(y1: int, y2: int):
        return (y2-y1), (2*y1-y2) #return m, c
    
    @staticmethod
    def get_frequency(array : list):
        res = {}  
        for keys in array:
            res[keys] = res.get(keys, 0) + 1
        return res
    
    def set_code(self):
        self.__code__ = TwoFactorAuthentication.generate()
    
    def check_patterns(self):
        for i in range(5):
            count = 0
            m, c = TwoFactorAuthentication.get_linear_equation(ord(self.__code__[i]), ord(self.__code__[i+1]))
            for j in range(4):
                if ( ord(self.__code__[i+j]) == m*(j+1) + c ):
                    count += 1
            if (count == 4):
                return False
        return True
    
    def check_window_of_2(self):
        for i in range(2):
            summed_array = []
            for j in range(0+i, 8-i, 2):
                summed_array.append(sum([ord(self.__code__[j])+ord(self.__code__[j+1])]))
            freq = TwoFactorAuthentication.get_frequency(summed_array)
            if (freq[max(freq, key=freq.get)] == 3):
                return False
        return True
     
    def check_window_of_3(self):
        for i in range(3):
            summed_array = []
            for j in range(0+i, 6, 3):
                summed_array.append(sum([ord(self.__code__[j])+ord(self.__code__[j+1])+ord(self.__code__[j+2])]))
            freq = TwoFactorAuthentication.get_frequency(summed_array)
            if (freq[max(freq, key=freq.get)] == 2):
                return False
        return True
    
    def check_window_of_4(self):
        
        summed_array = []
        for j in range(0, 8, 4):
            summed_array.append(sum([ord(self.__code__[j])+\
                                    ord(self.__code__[j+1])+\
                                    ord(self.__code__[j+2])+\
                                    ord(self.__code__[j+3])]))
        freq = TwoFactorAuthentication.get_frequency(summed_array)
        if (freq[max(freq, key=freq.get)] == 2):
            return False
        return True
    
    def check_hexspeak(self):
        for i in range(self.hexspeaks["total_count"]):
            if (self.hexspeaks["hexspeak"][i] in self.__code__):
                return False
        return True
    
    def get_code(self):
        result = False
        while( not result):
            self.set_code()
            if (self.check_hexspeak()):
                result = self.check_patterns() and\
                self.check_window_of_2() and \
                self.check_window_of_3() and \
                self.check_window_of_4()
        return hex(int(self.__code__, 16))
    
    def check_code(self, given_code : str):
        try:
            self.__code__ = given_code
            if (self.check_hexspeak()):
                    return self.check_patterns() and self.check_window_of_2() and \
                    self.check_window_of_3() and self.check_window_of_4()
            return False
        except:
            print("For checking you can give input in string format like '763AC21D' ")
            
if __name__  == "__main__":
    two_factor_auth = TwoFactorAuthentication()
    print("============================\n RANDOMLY GENERATED HEX CODES \n ==================================\n\n")
    for i in range(50):
        print(two_factor_auth.get_code(), end = " | ")
    
    print("\n\n============================\n TESTING SOME FAMOUS HEXSPEAKS \n================================\n\n")
    
    for hexspeak in ["DEADBEAF", "BI9B00B5", "AAAAAAA8", "12345678", "13579ABC"]:
        print(hexspeak, end= ": ")
        if (not two_factor_auth.check_code(hexspeak)):
            print("Cannot generate code.")
        else:
            print("Valid code")
    
            
                