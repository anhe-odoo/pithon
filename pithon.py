import os, re

def compile_and_run(code) :
    if not code.startswith("//@pi-ignore") :
        file_o = "to_execute.py"
        w      = 'a-zA-Z0-9_'
        
        code = (
            'from minlib import *\n'   +
            'from math   import *\n'   +
            '#include "macroDef.mac"\n'+
            code
        )
        
        code = re.sub(r"\( *(.*) *\? *(.*) *: *(.*) *\)", r"(\2 if \1 else \3)", code)
        code = ( code
            .replace("Α" , "Alpha"       ).replace("Β" , "Beta"      ).replace("Γ" , "Gamma"   ).replace("Δ", "Delta"    )
            .replace("Ε" , "Epsilon"     ).replace("Ζ" , "Zeta"      ).replace("Η" , "Eta"     ).replace("Θ", "Theta"    )
            .replace("Ι" , "Iota"        ).replace("Κ" , "Kappa"     ).replace("Λ" , "Lambda"  ).replace("Μ", "Mu"       )
            .replace("Ν" , "Nu"          ).replace("Ξ" , "Ksi"       ).replace("Ο" , "Omicron" ).replace("Π", "Pi"       )
            .replace("Ρ" , "Rho"         ).replace("Σ" , "Sigma"     ).replace("Τ" , "Tau"     ).replace("Υ", "Upsilon"  )
            .replace("Φ" , "Phi"         ).replace("Χ" , "Chi"       ).replace("Ψ" , "Psi"     ).replace("Ω", "Omega"    )
                
            .replace("α" , "alpha"       ).replace("β" , "beta"      ).replace("γ" , "gamma"   ).replace("δ", "delta"    )
            .replace("ε" , "epsilon"     ).replace("ζ" , "zeta"      ).replace("η" , "eta"     ).replace("θ", "theta"    )
            .replace("ι" , "iota"        ).replace("κ" , "kappa"     ).replace("λ" , "lambda"  ).replace("μ", "mu"       )
            .replace("ν" , "nu"          ).replace("ξ" , "ksi"       ).replace("ο" , "omicron" ).replace("π", "pi"       )
            .replace("ρ" , "rho"         ).replace("σ" , "sigma"     ).replace("ς" , "varsigma").replace("τ", "tau"      )
            .replace("υ" , "upsilon"     ).replace("φ" , "phi"       ).replace("ϕ" , "varphi"  ).replace("χ", "chi"      )
            .replace("ψ" , "psi"         ).replace("ω" , "omega"     )
                
            .replace("∞" , "float('inf')").replace("√" , "sqrt"      )
                
            .replace("≤" , "<="          ).replace("≥" , ">="        ).replace("≠" , "!="      ).replace("∈", "in"       )
            .replace("∉" , "not in"      ).replace("||", " or "      ).replace("&&", " and "   ).replace("~", " not "    )
            .replace("++", "+=1"         ).replace("--", "-=1"       ).replace("∀" , " for "   ).replace("|", " if "     )
            .replace("·" , "<<dot()>>"   ).replace("⌊" , "int(floor(").replace("⌋" , "))"      ).replace("⌈", "int(ceil(")
            .replace("⌉" , "))"          )
                
            .replace("₀" , "⟨0⟩"         ).replace("₁" , "⟨1⟩"       ).replace("₂" , "⟨2⟩"     ).replace("₃", "⟨3⟩"      )
            .replace("₄" , "⟨4⟩"         ).replace("₅" , "⟨5⟩"       ).replace("₆" , "⟨6⟩"     ).replace("₇", "⟨7⟩"      )
            .replace("₈" , "⟨8⟩"         ).replace("₉" , "⟨9⟩"       ).replace("₊" , "+"       ).replace("₋", "-"        )
            .replace("ₐ" , "⟨a⟩"         ).replace("ₑ" , "⟨e⟩"       ).replace("ₒ" , "⟨o⟩"     ).replace("ₓ", "⟨x⟩"      )
            .replace("ₕ" , "⟨h⟩"         ).replace("ₖ" , "⟨k⟩"       ).replace("ₗ" , "⟨l⟩"     ).replace("ₘ", "⟨m⟩"      )
            .replace("ₙ" , "⟨n⟩"         ).replace("ₚ" , "⟨p⟩"       ).replace("ₛ" , "⟨s⟩"     ).replace("ₜ", "⟨t⟩"      )
                
            .replace("⁰" , "**0"         ).replace("¹" , "**1"       ).replace("²" , "**2"     ).replace("³", "**3"      )
            .replace("⁴" , "**4"         ).replace("⁵" , "**5"       ).replace("⁶" , "**6"     ).replace("⁷", "**7"      )
            .replace("⁸" , "**8"         ).replace("⁹" , "**9"       ).replace("ⁱ" , "**i"     )
        )
        
        # f ≡ x → ...   => def f(x) : return ...
        code = re.sub(r"([{}]*) ≡ ([{}]*) *→".format(w,w), r"def \1(\2) : return ", code)
        # f = x → ...   =>  f = lambda x : ...
        code = re.sub(r"([{}]*) *→".format(w), r"lambda \1 : ", code)
        
        # from x1 to x2  => range(x1, x2+1)
        code = re.sub(r"from *([{}]*) *to *([{}]*) *:".format(w,w), r"in range(\1,\2+1) :", code)
        
        # repeat ... until cond => while True: ... if cond: break
        code = code.replace("repeat", "while True")
        code = re.sub(r"until *(.*)".format(w), r"    if(\1):break", code)
        
        # select ... case/default
        code = re.sub(r"( *)select *(.*):", r"\1__select_var__ = \2\n\1if False: pass", code)
        code = code.replace("    case", "elif __select_var__ ==").replace("    default", "else")
        
        # [x1 .. x2[  =>  range(x1, x2)
        code = re.sub(r"\[ *([{}]*) *.. *([{}]*) *\[".format(w,w), r"range(\1,\2)", code)
        # ]x1 .. x2[  =>  range(x1+1, x2)
        code = re.sub(r"\] *([{}]*) *.. *([{}]*) *\[".format(w,w), r"range(\1+1,\2)", code)
        # [x1 .. x2]  =>  range(x1, x2+1)
        code = re.sub(r"\[ *([{}]*) *.. *([{}]*) *\]".format(w,w), r"range(\1,\2+1)", code)
        # ]x1 .. x2]  =>  range(x1+1, x2+1)
        code = re.sub(r"\] *([{}]*) *.. *([{}]*) *\]".format(w,w), r"range(\1+1,\2+1)", code)
        
        with open(file_o, "w") as f:
            f.write(code)

        LIMT = 10000
        with open('numbered.mac', 'w') as f :
            for i in range(LIMT) :
                f.write('#define dec_%d %d\n#define inc_%d %d\n' % (i+1, i, i, i+1))
            f.write('#define dec_0 %d\n#define inc_%d 0\n' % (LIMT, LIMT))
            f.write('#define dec(x) dec_ ## x\n#define inc(x) inc_ ## x')

        # Lancement du preproc g++ et nettoyage
        os.system("cpp '{}' > '{}'".format(file_o, file_o+".tmp"))
        os.system("sed '/^#/ d' \"{}\" > \"{}\"".format(file_o+".tmp", file_o))
        os.remove(file_o+".tmp")

        os.system("sed -i 's/#.*$//;/^$/d' \"{}\"".format(file_o))
        os.system("sed -i 's/; *$//g' \"{}\"".format(file_o))
        os.system("sed -i 's/\\xe2\\x9f\\xa9\\([+-]\\)\\xe2\\x9f\\xa8/\\1/g' \"{}\"".format(file_o))
        os.system("sed -i 's/\\xe2\\x9f\\xa9\\([+-]\\)\\xe2\\x9f\\xa8/\\1/g' \"{}\"".format(file_o))
        os.system("sed -i 's/\\xe2\\x9f\\xa9/]/g;s/\\xe2\\x9f\\xa8/[/g' \"{}\"".format(file_o))
        os.system("sed -i 's/\\*\\*\\(.*\\)\\*\\*/\\**1/g' \"{}\"".format(file_o))

        os.remove("numbered.mac")

        os.system("python3 \"{}\" > output.txt".format(file_o))
        #os.remove(file_o)
    else :
        with open("to_execute.py", "w") as f:
            f.write(code.replace("//@", "#"))
        os.system("python3 to_execute.py > output.txt")

    with open("output.txt", "r") as outf :
        result = "".join(outf.readlines())
    return result
