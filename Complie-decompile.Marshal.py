
def Py3():
	c=input("[*] decompile marshal python 3.7.X\n[?] File output: ")
	x=marshal.loads(marcode.py3)
	xx=decompile(3.7,x,sys.stdout)
	xxx="# Success decompile marshal python 3.7.X\n# At: "+time.ctime()+"\n# By KANG-NEWBIE\n"+xx.text
	with open(c+".py","w") as f:
		f.write(xxx)
	print("\n\n[result] Saved as \033[95m%s.py"%(c))

def Py2():


def Py2():
	c=raw_input("[*]decompile marshal python 2.7.X\n[?] File output: ")
	x=marshal.loads(marcode.py2)
	xx=decompile(2.7,x,sys.stdout)
	xxx="# Success decompile marshal python 2.7.X\n# At: "+time.ctime()+"\n# By KANG-NEWBIE\n"+xx.text
	with open(c+".py","w") as f:
		f.write(xxx)
	print("\n\n[result] Saved as \033[95m%s.py"%(c))

try:

def map_source(code: CodeType, context: Context) -> CodeType:
    # Trick uncompyle6 into generating parse-able code
    # for impossible constructs (e.g. constant funtions)
    class CallableMock:
        def __init__(self, name: str):
            self.name = name

        def __repr__(self):
            return self.name

    wrapped_const_code = CodeType(
        code.co_argcount,
        code.co_kwonlyargcount,
        code.co_nlocals,
        code.co_stacksize,
        code.co_flags,
        code.co_code,
        tuple(
            (
                CallableMock(
                    const.__name__
                    if not const.__name__.startswith("  <  ")
                    else f"anonymous_func_{abs(hash(const))}"
                )
                if callable(const)
                else const
                for const in code.co_consts
            )
        ),
        code.co_names,
        code.co_varnames,
        code.co_filename,
        code.co_name,
        code.co_firstlineno,
        code.co_lnotab,
        code.co_freevars,
        code.co_cellvars,
    )

    fn_name = (
        code.co_name
        if not code.co_name.startswith(" < ")
        else f"anonymous_func_{abs(hash(code))}"
    )
    tmp_file = NamedTemporaryFile(prefix=f"{fn_name}__", suffix="__.py", delete=False)

    raw_buf = StringIo()
    decompile(None, wrapped_const_code, out=raw_buf)
    raw_buf.flush()

    buf = []
    # There doesn't appear to be an easy way to silence startup prints.
    # Luckily, the are all prefixed with a '# '.
    other_than_pound = False
    for line in raw_buf.getvalue().split("\n"):
        if not line.startswith("# "):
            other_than_pound = True
        if other_than_pound:
            # Indent by one level
            buf.append(f"{' ' * INDENTATION_SIZE}{line}")

    # Define a dummy function
    fn_code = "\n".join(buf)
    # To-Do: Use real function signature
    wrapped_fn_code = format_str(f"def {fn_name}():\n{fn_code}", LINE_LENGTH)

    tmp_file.write(wrapped_fn_code.encode())

    # Compile code to obtain line-to-op mapping (co_lnotab)
    tmp_code = compile(wrapped_fn_code, tmp_file.name, "exec").co_consts[0]

    return CodeType(
        code.co_argcount,
        code.co_kwonlyargcount,
        code.co_nlocals,
        code.co_stacksize,
        code.co_flags,
        code.co_code,
        code.co_consts,
        code.co_names,
        code.co_varnames,
        tmp_file.name,
        code.co_name,
        1,
        tmp_code.co_lnotab,
        code.co_freevars,
        code.co_cellvars,
    )


EXTENSION = map_source