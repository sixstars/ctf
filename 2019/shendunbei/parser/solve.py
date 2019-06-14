from parse import *
import re

with open("./exp.js") as f:
	code = f.read()
code = code.replace(" ","").replace("\t","")
lines = code.split("\n")
"""
fmt = "{:d}:Stmt_Expression(expr:Expr_Assign(var:Expr_Variable(name:{})expr:Scalar_String(value:{})))"
begin = 270
for i in range(100):
	data = "".join(lines[i*10+begin:(i+1)*10+begin])
	r=parse(fmt,data)
	print "%s=\"%s\""%(r[1],r[2])
"""

exp_ass_fmt=re.compile("^Expr_Assign\(var:Expr_Variable\(name:(.*)\)expr:(.*)\)$")
op_concat_fmt=re.compile("^Expr_BinaryOp_Concat\(left:(.*)right:(.*)\)$")
str_fmt = re.compile("^Scalar_String\(value:(.*)\)$")
exp_var_fmt= re.compile("^Expr_Variable\(name:(.*)\)$")
stm_fmt = re.compile("^[0-9]*:Stmt_Expression\(expr:(.*)\)$")


def get_stm_end(i):
    i=i+1
    while True:
        begin_fmt="{:d}:Stmt_Expression("
        r=parse(begin_fmt,lines[i])
        if r != None:
            break
        i+=1
    return i

def show_code(ast):
    r = exp_ass_fmt.match(ast)
    if r != None:
        name = r.groups()[0]
        data = show_code(r.groups()[1])
        return "%s = %s"%(name,data)
    else:
        r = op_concat_fmt.match(ast)
        if r != None:
            left = show_code(r.groups()[0])
            right = show_code(r.groups()[1])
            return "%s + %s"%(left,right)
        else:
            r = exp_var_fmt.match(ast)
            if r!=None:
                var = r.groups()[0]
                return var
            else:
                r = str_fmt.match(ast)
                if r!=None:
                    return "\"%s\""%r.groups()[0]
                else:
                    raise Exception("wtf")


it=1270
cnt=0
while cnt<99:
    end = get_stm_end(it)
    data="".join(lines[it:end]).replace(" ","").replace("\n","")
    it = end
    r=stm_fmt.match(data)
    print show_code(r.groups()[0])
    cnt+=1



# data=data.replace(" ","").replace("\n","")

# # print data
# r= stm_fmt.match(data)
# # op_concat_fmt=re.compile("a:a\(\)a.*bbb$")
# # r= op_concat_fmt.findall("ca:a()aabbbbaaaabbb")
# print r.groups()
