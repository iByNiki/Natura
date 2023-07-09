int_raw = ""

def int_process(int_text):
    global int_raw

    int_rawblocks = int_text.split("<?ntr")
    int_codeblocks = []

    int_raw = ""

    for int_block in int_rawblocks:
        if ("?>" in int_block):
            int_codeblocks.append("<?ntr" + int_block.split("?>")[0])
            int_codeblocks.append(int_block.split("?>")[1])
        else:
            int_codeblocks.append(int_block)


    for int_block in int_codeblocks:
        if ("<?ntr" in int_block):
            int_block = int_block.replace("<?ntr", "")
            exec(int_block)
        else:
            int_raw += int_block

    return int_raw

def echo(text, end="\n"):
    global int_raw
    int_raw += str(text) + end