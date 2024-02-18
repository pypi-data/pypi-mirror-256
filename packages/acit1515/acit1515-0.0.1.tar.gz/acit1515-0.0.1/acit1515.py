from colorama import Fore

class Test():
    def __init__(self, f, submission):
        self.f = f
        self.submission = submission

    def returns(self, test_values, marks):
        if test_values != None:
            result = getattr(self.submission, self.f)(test_values)
        else:
            result = getattr(self.submission, self.f)()
        if result == None:
            print(Fore.RED + f"FAIL: {self.f}() does not return a value (-{marks} marks)" + Fore.RESET)
            return False
        print(Fore.GREEN + f"PASS: {self.f}() returns a value" + Fore.RESET)
        return True

    def returns_type(self, test_values, return_type, marks):
        if test_values != None:
            result = getattr(self.submission, self.f)(test_values)
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
            result = getattr(self.submission, self.f)(test_values)
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

    def returns_valid(self, valid_values, valid_response, invalid_values, invalid_response, marks):
        # call f with test_values
        if valid_values != None:
            result1 = getattr(self.submission, self.f)(valid_values)
            result2 = getattr(self.submission, self.f)(invalid_values)
        else:
            result1 = getattr(self.submission, self.f)(valid_values)
            result2 = getattr(self.submission, self.f)(invalid_values)

        if result1 and not result2:
            print(Fore.GREEN + f"PASS: {self.f}() returns a valid value" + Fore.RESET)
            return True
        else:
            print(Fore.RED + f"FAIL: {self.f}() does not return a valid value (-{marks} marks)" + Fore.RESET)
            return False
    
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
