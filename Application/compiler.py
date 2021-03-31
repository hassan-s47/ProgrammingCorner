

import sys, os, getopt,subprocess,shlex,tempfile,time

class Compiler:
    
    def __init__(self, code, ins):
        filedir = tempfile.getttempdir()
        filename = str(time.time()).replace('.','_')
        code_file = os.path.join(filedir, filename+'.cpp')
        exe_file = os.path.join(filedir, filename+'.exe')
        in_file = os.path.join(filedir, filename+'_input.txt')
        print(code_file,exe_file)

        with open(code_file, 'w') as f:
            f.write(code)
        
        with open(in_file, 'w') as f:
            f.write(ins)
        
        self.run(code_file,exe_file,in_file)
            

    def run(self,cpp_file, exe_file,in_file):
        compile_str = "g++ " + shlex.quote(cpp_file) + " -o " + shlex.quote(exe_file)
        proc = subprocess.Popen(compile_str, stdout = subprocess.PIPE, stderr=subprocess.PIPE, shell = True)
        (out,err) = proc.communicate(timeout=15)
        if err == b'':
            print("Compilation Succeeded.")
            exec_str = "./" + shlex.quote(exe_file) + " "+ shlex.quote(in_file)
            proc1 =  proc = subprocess.Popen( exec_str, stdout = subprocess.PIPE, stderr=subprocess.PIPE, shell = True)
            try:
                (out1,err1) = proc1.communicate(timeout=15)
            except:
                out1 = ''
                err1 = b'Timeout Error'
            if err1 == b'':
                print(out1.decode())
            else:
                print(err1.decode())
        else:
            print(err.decode())
        
