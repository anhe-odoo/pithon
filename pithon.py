import os, sys
file_1 = sys.argv[1]
file_i = file_1.replace(".ipynb", ".pi")
file_o = file_i.replace(".pi", ".py")

LIMT = 10000
with open('numbered.mac', 'w') as f :
    for i in range(LIMT) :
        f.write('#define dec_%d %d\n#define inc_%d %d\n' % (i+1, i, i, i+1))
    f.write('#define dec_0 %d\n#define inc_%d 0\n' % (LIMT, LIMT))
    f.write('#define dec(x) dec_ ## x\n#define inc(x) inc_ ## x')
os.system("python3 ./convert.py {}".format(file_1))

w='a-zA-Z0-9_';

os.system('cp "{}" "{}"'.format(file_i, file_o + ".tmp"))
os.system("sed -i '1ifrom minlib import *' '{}'".format(file_o+".tmp"));
os.system("sed -i '1i#include \"macroDef.mac\"' '{}'".format(file_o+".tmp"))
os.system("sed -i -e \"s/( *\\(.*\\) * ? *\\(.*\\) *: *\\(.*\\) *)/(\\2 if \\1 else \\3)/g\" \"{}\"".format(file_o + ".tmp"))

os.system(
  """sed -e 's/\\xe2\\x88\\x9a/sqrt/g' -e 's/\\xe2\\x88\\x87/nabla/g;s/\\xe2\\x88\\x80/for/g' \
    -e 's/\\xe2\\x88\\x88/in/g;s/\\xe2\\x88\\x89/not in/g;s/\\xc2\\xb7/<<dot()>>/g' \
    -e 's/\\xe2\\x89\\xa4/<=/g;s/\\xe2\\x89\\xa5/>=/g;s/\\xe2\\x89\\xa0/!=/g' \
    -e 's/\\xe2\\x8c\\x8a/int(floor(/g;s/[\\xe2\\x8c\\x8b\\xe2\\x8c\\x89]/))/g;s/\\xe2\\x8c\\x88/int(ceil(/g' \
    -e 's/\\xe2\\x82\\x80/\\xe2\\x9f\\xa80\\xe2\\x9f\\xa9/g;s/\\xe2\\x82\\x81/\\xe2\\x9f\\xa81\\xe2\\x9f\\xa9/g' \
    -e 's/\\xe2\\x82\\x82/\\xe2\\x9f\\xa82\\xe2\\x9f\\xa9/g;s/\\xe2\\x82\\x83/\\xe2\\x9f\\xa83\\xe2\\x9f\\xa9/g' \
    -e 's/\\xe2\\x82\\x84/\\xe2\\x9f\\xa84\\xe2\\x9f\\xa9/g;s/\\xe2\\x82\\x85/\\xe2\\x9f\\xa85\\xe2\\x9f\\xa9/g' \
    -e 's/\\xe2\\x82\\x86/\\xe2\\x9f\\xa86\\xe2\\x9f\\xa9/g;s/\\xe2\\x82\\x87/\\xe2\\x9f\\xa87\\xe2\\x9f\\xa9/g' \
    -e 's/\\xe2\\x82\\x88/\\xe2\\x9f\\xa88\\xe2\\x9f\\xa9/g;s/\\xe2\\x82\\x89/\\xe2\\x9f\\xa89\\xe2\\x9f\\xa9/g' \
    -e 's/\\xe2\\x82\\x98/\\xe2\\x9f\\xa8m\\xe2\\x9f\\xa9/g' \
    -e 's/\\xe2\\x82\\x99/\\xe2\\x9f\\xa8n\\xe2\\x9f\\xa9/g;s/\\xe2\\x82\\x8a/+/g;s/\\xe2\\x82\\x8b/-/g' \
    -e 's/\\xe2\\x81\\xb0/**0/g;s/\\xc2\\xb9/**1/g;s/\\xc2\\xb2/**2/g;s/\\xc2\\xb3/**3/g' \
    -e 's/\\xe2\\x81\\xb4/**4/g;s/\\xe2\\x81\\xb5/**5/g;s/\\xe2\\x81\\xb6/**6/g;s/\\xe2\\x81\\xb7/**7/g' \
    -e 's/\\xe2\\x81\\xb8/**8/g;s/\\xe2\\x81\\xb9/**9/g;s/\\xe2\\x81\\xba//g;s/\\xe2\\x81\\xbb/**-/g' \
    -e 's/\\xe2\\x81\\xb1/**i/g' \
    -e 's/\\xce\\xb1/alpha/g;s/\\xce\\xb2/beta/g;s/\\xce\\xb3/gamma/g;s/\\xce\\xb4/delta/g' \
    -e 's/\\xce\\xb5/epsilon/g;s/\\xce\\xb6/zeta/g;s/\\xce\\xb7/eta/g;s/\\xce\\xb8/theta/g' \
    -e 's/\\xce\\xb9/iota/g;s/\\xce\\xba/kappa/g;s/\\xce\\xbb/lambda/g;s/\\xce\\xbc/mu/g;s/\\xce\\xbd/nu/g' \
    -e 's/\\xce\\xbe/ksi/g;s/\\xce\\xbf/omicron/g;s/\\xcf\\x80/pi/g;s/\\xcf\\x81/rho/g' \
    -e 's/\\xcf\\x82/varsigma/g;s/\\xcf\\x83/sigma/g;s/\\xcf\\x84/tau/g;s/\\xcf\\x85/upsilon/g' \
    -e 's/\\xcf\\x86/phi/g;s/\\xcf\\x95/varphi/g;s/\\xcf\\x87/chi/g;s/\\xcf\\x88/psi/g;s/\\xcf\\x89/omega/g' \
    -e 's/\\xe2\\x88\\x9e/float(\"inf\")/g' \
    -e 's/||/ or /g;s/&&/ and /g;s/~/ not /g;s/++/+=1/g;s/--/-=1/g' \
    -e 's/|/ if /g' \
    \"{}\" > \"{}\""""
    .format(file_o+".tmp", file_o)
)

## f ≡ x → ...   => def f(x) : return ...
os.system(
    "sed -i -e 's/\\([{}]*\\) *\\xe2\\x89\\xa1 *\\([{}]*\\) *\\xe2\\x86\\x92/def \\1(\\2) : return /g' \"{}\""
    .format(w, w, file_o)
)

## f = x → ...   =>  f = lambda x : ...
os.system("sed -i -e 's/\\([{}]*\\) *\\xe2\\x86\\x92/lambda \\1 : /g' \"{}\"".format(w, file_o))

## [x1 .. x2[  =>  range(x1, x2)
os.system("sed -i -e 's/\\[ *\\([{}]*\\) *.. *\\([{}]*\\) *\\[/range(\\1,\\2)/g' \"{}\"".format(w, w, file_o))
## ]x1 .. x2[  =>  range(x1+1, x2)
os.system("sed -i -e 's/\\] *\\([{}]*\\) *.. *\\([{}]*\\) *\\[/range(\\1+1,\\2)/g' \"{}\"".format(w, w, file_o))
## [x1 .. x2]  =>  range(x1, x2+1)
os.system("sed -i -e 's/\\[ *\\([{}]*\\) *.. *\\([{}]*\\) *\\]/range(\\1,\\2+1)/g' \"{}\"".format(w, w, file_o))
## ]x1 .. x2]  =>  range(x1+1, x2+1)
os.system("sed -i -e 's/\\] *\\([{}]*\\) *.. *\\([{}]*\\) *\\]/range(\\1+1,\\2+1)/g' \"{}\"".format(w, w, file_o))

## from x1 to x2  => range(x1, x2+1)
os.system("sed -i -e 's/from *\\([{}]*\\) *to *\\([{}]*\\) *:/in range(\\1,\\2+1) :/g' \"{}\"".format(w, w, file_o))

## repeat ... until cond => while True: ... if cond: break
os.system("sed -i -e 's/repeat/while True/g' \"{}\"".format(file_o))
os.system("sed -i -e 's/until\\(.*\\)/    if(\\1) :break/g' \"{}\"".format(file_o))

os.system("sed -i -e 's/\\( *\\)select *\\(.*\\):/\\1__select_var__ = \\2\\n\\1if False: pass/g' \"{}\"".format(file_o))
os.system("sed -i -e 's/    case/elif __select_var__ ==/g' \"{}\"".format(file_o))
os.system("sed -i -e 's/    default/else/g' \"{}\"".format(file_o))

os.system("cpp '{}' > '{}'".format(file_o, file_o+".tmp"))

os.system("sed '/^#/ d' \"{}\" > \"{}\" && rm \"{}\"".format(file_o+".tmp", file_o, file_o+".tmp"))
os.system("sed -i 's/#.*$//;/^$/d' \"{}\"".format(file_o))
os.system("sed -i 's/; *$//g' \"{}\"".format(file_o))
os.system("sed -i 's/\\xe2\\x9f\\xa9\\([+-]\\)\\xe2\\x9f\\xa8/\\1/g' \"{}\"".format(file_o))
os.system("sed -i 's/\\xe2\\x9f\\xa9\\([+-]\\)\\xe2\\x9f\\xa8/\\1/g' \"{}\"".format(file_o))
os.system("sed -i 's/\\xe2\\x9f\\xa9/]/g;s/\\xe2\\x9f\\xa8/[/g' \"{}\"".format(file_o))

os.system("rm numbered.mac")
if file_1 != file_i :
    os.system("rm \"{}\"".format(file_i))

os.system("python3 \"{}\" > output.txt".format(file_o))

with open("output.txt", "r") as outf :
    for line in outf.readlines():
        print(line)
#
#if !([[ "$*" == *"--save"* ]]); then
#    rm "$o";
#fi
#