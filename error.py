def throw_error(cmd: str, invalid: bool):
    if not invalid:
        return (f"""
For help with gitlite {cmd}, try:
\tmain.py {cmd} -h \t[OR] \tmain.py {cmd} --help
""")
    else:
        return (f"""
Invalid use of {cmd} command :( 

For help with gitlite {cmd}, try:
\tmain.py {cmd} -h \t[OR] \tmain.py {cmd} --help
""")