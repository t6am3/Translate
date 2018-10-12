import compileall
import py_compile

def compile(dir):
    if dir.rfind('.py') != -1:
        py_compile.compile(dir)
    else:
        compileall.compile_dir(dir)

if __name__ == '__main__':
    compile(input("请输入你要编译的文件/路径"))