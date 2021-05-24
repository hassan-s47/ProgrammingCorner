

import sys, os, getopt,subprocess,shlex,tempfile,time

class Compiler:
    
    def __init__(self, code, ins ):
        filedir = tempfile.gettempdir()
        filename = str(time.time()).replace('.','_')
        self.code_file = os.path.join(filedir, filename+'.cpp')
        self.exe_file = os.path.join(filedir, filename+'.exe')
        self.in_file = os.path.join(filedir, filename+'_input.txt')
        print(self.code_file,self.exe_file)
        with open(self.code_file, 'w') as f:
            f.write(code)
        
        with open(self.in_file, 'w') as f:
            f.write(ins)
        

            

    def run(self,stdin_str):
        compile_str = "g++ " + shlex.quote(self.code_file) + " -o " + shlex.quote(self.exe_file)
        proc = subprocess.Popen(compile_str, stdout = subprocess.PIPE, stderr=subprocess.PIPE, shell = True)
        (out,err) = proc.communicate(timeout=15)
        if err == b'':
            print("Compilation Succeeded.")
            exec_str = "" + shlex.quote(self.exe_file) + " "+ shlex.quote(self.in_file)
            proc1 =  proc = subprocess.Popen( exec_str, stdout = subprocess.PIPE, stderr=subprocess.PIPE, shell = True)
            try:
                (out1,err1) = proc1.communicate(timeout=15,input = stdin_str.encode())
                self.removeFiles()
            except:
                out1 = ''
                err1 = b'Timeout Error'
            if err1 == b'':
               return out1.decode()
            else:
               return err1.decode()
        else:
            return err.decode()
            print("temp")
    
    
    def removeFiles(self):
        if os.path.exists(self.exe_file):
            os.remove(self.exe_file)
        else:
            print("The file does not exist")
        
        if os.path.exists(self.in_file):
            os.remove(self.in_file)
        else:
            print("The file does not exist")
        if os.path.exists(self.code_file):
            os.remove(self.code_file)
        else:
            print("The file does not exist")

    
    def runTestCase(self,testCaseInput, testCaseOutput):
        
        output = self.run(testCaseInput)
        if output == testCaseOutput:
            return True
        else:
            return False

        

        
        





