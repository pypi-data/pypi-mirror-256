import sys
import os
import importlib
from colorama import Fore

class Test():
    def __init__(self, f, submission):
        self.f = f
        self.submission = submission

    def returns(self, test_values, marks, *args):
        if test_values != None:
            result = getattr(self.submission, self.f)(*test_values)
        else:
            result = getattr(self.submission, self.f)()
        if result == None:
            print(Fore.RED + f"FAIL: {self.f}() does not return a value (-{marks} marks)" + Fore.RESET)
            return False
        print(Fore.GREEN + f"PASS: {self.f}() returns a value" + Fore.RESET)
        return True

    def returns_type(self, test_values, return_type, marks):
        if test_values != None:
            result = getattr(self.submission, self.f)(*test_values)
        else:
            result = getattr(self.submission, self.f)()
        if type(result) != return_type:
            print(Fore.RED + f"FAIL: {self.f}() does not return a(n) {return_type.__name__} (-{marks} marks)" + Fore.RESET)
            return False
        else:
            print(Fore.GREEN + f"PASS: {self.f}() returns a(n) {return_type.__name__}" + Fore.RESET)
            return True

    def returns_length(self, test_values, return_length, marks):
        if test_values != None:
            result = getattr(self.submission, self.f)(*test_values)
        else:
            result = getattr(self.submission, self.f)()
        if len(result) != return_length:
            print(Fore.RED + f"FAIL: {self.f}() does not return a value of length {return_length} (-{marks} marks)" + Fore.RESET)
            return False
        else:
            print(Fore.GREEN + f"PASS: {self.f}() returns a value of length {return_length}" + Fore.RESET)
            return True
        pass

    def returns_hardcoded(self, test_values: list):
        # call f multiple times with test_values
        # return true if return value is not hardcoded
        pass

    def returns_conditionally_valid(self, test_values, conditions, marks):
        # call f with test_values
        # run return value through conditions (a list of dictionaries with condition name and associated function)
        # return true if all conditions are met
        if test_values != None:
            result = getattr(self.submission, self.f)(*test_values)
        else:
            result = getattr(self.submission, self.f)()

        for i in range(len(conditions)):
            func = conditions[i]
            if not func(result):
                Fore.RED + f"FAIL: {self.f}() does not pass (-{marks} marks)" + Fore.RESET

    def returns_valid(self, valid_values, valid_response, invalid_values, invalid_response, marks):
        # call f with test_values
        pass_str = Fore.GREEN + f"PASS: {self.f}() returns a valid value" + Fore.RESET
        fail_str = Fore.RED + f"FAIL: {self.f}() does not return a valid value (-{marks} marks)" + Fore.RESET

        if valid_values != None and valid_response != None:
            result1 = getattr(self.submission, self.f)(*valid_values)
            
            if result1 != valid_response:
                print(fail_str)
                return False
            
        if valid_values == None and valid_response != None:
            result1 = getattr(self.submission, self.f)()
            
            if result1 != valid_response:
                print(fail_str)
                return False
            
        if invalid_values != None and invalid_response != None:
            result2 = getattr(self.submission, self.f)(*invalid_values)

            if result2 != invalid_response:
                print(fail_str)
                return False    
        
        print(pass_str)
        return True
    
    def run_tests(self):
        tests = [attr for attr in dir(self) if attr.startswith("test")]
        total_marks = len(tests)
        deductions = 0

        for i in range(len(tests)):
            result = getattr(self, tests[i])(len(tests) - i)
            if not result:
                deductions += len(tests) - i
                break

        return (total_marks, deductions)

if __name__ == '__main__':
    if '.py' not in sys.argv[-1]:
        print('Usage: py -m acit1515 <filename.py>')
        sys.exit()

    if not os.path.exists(os.path.join(os.getcwd(), 'tests')):
        print('No /tests directory found')
        sys.exit()

    try:
        submission = __import__(sys.argv[-1][:-3])
    except:
        print(Fore.RED + f'FAIL: script could not be run' + Fore.RESET)
        print(f'Final mark: 0')
        sys.exit()
    else:
        results = []

        for filename in os.listdir(os.path.join(os.getcwd(), 'tests')):
            if filename.startswith('test_'):
                module_name = f'tests.{filename[:-3]}'
                module = importlib.import_module(module_name)
                class_name = filename[5:-3].title()
                results.append(getattr(module, class_name)(submission).run_tests())

        total_marks = sum([total for total, _ in results])
        deductions = sum([deduction for _, deduction in results])

        print(f'Final mark: {total_marks - deductions}/{total_marks}')