#echo "≡" | hexdump -C

if [ $1 = "--help" ]; then
    echo "Aide"
    exit;
fi

if [ $1 = "--eval" ]; then
    python3 ./evaluate.py $2;
    exit;
fi

i="$1";
#i="${1/.ipynb/.pi}";
o="${i/.pi/.py}";

# | ≡ | ≤ | ≥ | ≠ | √ | → | ∞ | · | ∏ | ∑ | ⌊ ⌋ | ⌈ ⌉ | ⟨ ⟩ | ∀ | ∈ | ∉ |
# | ₀ | ₁ | ₂ | ₃ | ₄ | ₅ | ₆ | ₇ | ₈ | ₉ | ₊ | ₋ |   | ₕ | ₖ | ₗ | ₘ | ₙ | ₚ | ₛ | ₜ |
# | ⁰ | ¹ | ² | ³ | ⁴ | ⁵ | ⁶ | ⁷ | ⁸ | ⁹ | ⁺ | ⁻ | ⁱ |
# | Α | Β | Γ | Δ | Ε | Ζ | Η | Θ | Ι | Κ | Λ | Μ | Ν | Ξ | Ο | Π | Ρ |  Σ  | Τ | Υ |  Φ  | Χ | Ψ | Ω
# | α | β | γ | δ | ε | ζ | η | θ | ι | κ | λ | μ | ν | ξ | ο | π | ρ | σ/ς | τ | υ | φ/ϕ | χ | ψ | ω

# TODO :

echo "LIMT = 10000" > generate.py;
echo "with open('numbered.mac', 'w') as f :" >> generate.py;
echo "    for i in range(LIMT) :" >> generate.py;
echo "        f.write('#define dec_%d %d\n#define inc_%d %d\n' % (i+1, i, i, i+1))" >> generate.py;
echo "    f.write('#define dec_0 %d\n#define inc_%d 0\n' % (LIMT, LIMT))" >> generate.py;
echo "    f.write('#define dec(x) dec_ ## x\n#define inc(x) inc_ ## x')" >> generate.py;
python generate.py
rm generate.py

python3 ./convert.py "$1";

w='a-zA-Z0-9_';

cp "$i" "$o.tmp";

sed -i '1ifrom minlib import *' "$o.tmp";
sed -i '1i#include "macroDef.mac"' "$o.tmp";
sed -i -e "s/( *\(.*\) * ? *\(.*\) *: *\(.*\) *)/(\2 if \1 else \3)/g" "$o.tmp";

sed -e 's/\xe2\x88\x9a/sqrt/g' -e 's/\xe2\x88\x87/nabla/g;s/\xe2\x88\x80/for/g'                     \
    -e 's/\xe2\x88\x88/in/g;s/\xe2\x88\x89/not in/g;s/\xc2\xb7/<<dot()>>/g'                         \
    -e 's/\xe2\x89\xa4/<=/g;s/\xe2\x89\xa5/>=/g;s/\xe2\x89\xa0/!=/g'                                \
    -e 's/\xe2\x8c\x8a/int(floor(/g;s/[\xe2\x8c\x8b\xe2\x8c\x89]/))/g;s/\xe2\x8c\x88/int(ceil(/g'   \
    -e 's/\xe2\x82\x80/\xe2\x9f\xa80\xe2\x9f\xa9/g;s/\xe2\x82\x81/\xe2\x9f\xa81\xe2\x9f\xa9/g'      \
    -e 's/\xe2\x82\x82/\xe2\x9f\xa82\xe2\x9f\xa9/g;s/\xe2\x82\x83/\xe2\x9f\xa83\xe2\x9f\xa9/g'      \
    -e 's/\xe2\x82\x84/\xe2\x9f\xa84\xe2\x9f\xa9/g;s/\xe2\x82\x85/\xe2\x9f\xa85\xe2\x9f\xa9/g'      \
    -e 's/\xe2\x82\x86/\xe2\x9f\xa86\xe2\x9f\xa9/g;s/\xe2\x82\x87/\xe2\x9f\xa87\xe2\x9f\xa9/g'      \
    -e 's/\xe2\x82\x88/\xe2\x9f\xa88\xe2\x9f\xa9/g;s/\xe2\x82\x89/\xe2\x9f\xa89\xe2\x9f\xa9/g'      \
    -e 's/\xe2\x82\x98/\xe2\x9f\xa8m\xe2\x9f\xa9/g'                                                 \
    -e 's/\xe2\x82\x99/\xe2\x9f\xa8n\xe2\x9f\xa9/g;s/\xe2\x82\x8a/+/g;s/\xe2\x82\x8b/-/g'           \
    -e 's/\xe2\x81\xb0/**0/g;s/\xc2\xb9/**1/g;s/\xc2\xb2/**2/g;s/\xc2\xb3/**3/g'                    \
    -e 's/\xe2\x81\xb4/**4/g;s/\xe2\x81\xb5/**5/g;s/\xe2\x81\xb6/**6/g;s/\xe2\x81\xb7/**7/g'        \
    -e 's/\xe2\x81\xb8/**8/g;s/\xe2\x81\xb9/**9/g;s/\xe2\x81\xba//g;s/\xe2\x81\xbb/**-/g'           \
    -e 's/\xe2\x81\xb1/**i/g'                                                                       \
    -e 's/\xce\xb1/alpha/g;s/\xce\xb2/beta/g;s/\xce\xb3/gamma/g;s/\xce\xb4/delta/g'                 \
    -e 's/\xce\xb5/epsilon/g;s/\xce\xb6/zeta/g;s/\xce\xb7/eta/g;s/\xce\xb8/theta/g'                 \
    -e 's/\xce\xb9/iota/g;s/\xce\xba/kappa/g;s/\xce\xbb/lambda/g;s/\xce\xbc/mu/g;s/\xce\xbd/nu/g'   \
    -e 's/\xce\xbe/ksi/g;s/\xce\xbf/omicron/g;s/\xcf\x80/pi/g;s/\xcf\x81/rho/g'                     \
    -e 's/\xcf\x82/varsigma/g;s/\xcf\x83/sigma/g;s/\xcf\x84/tau/g;s/\xcf\x85/upsilon/g'             \
    -e 's/\xcf\x86/phi/g;s/\xcf\x95/varphi/g;s/\xcf\x87/chi/g;s/\xcf\x88/psi/g;s/\xcf\x89/omega/g'  \
    -e 's/\xe2\x88\x9e/float("inf")/g'                                                              \
    -e 's/||/ or /g;s/&&/ and /g;s/~/ not /g;s/++/+=1/g;s/--/-=1/g'                                 \
    -e 's/|/ if /g'                                                                                 \
    "$o.tmp" > "$o";

# f ≡ x → ...   => def f(x) : return ...
sed -i -e "s/\([$w]*\) *\xe2\x89\xa1 *\([$w]*\) *\xe2\x86\x92/def \1(\2) : return /g" "$o";

# f = x → ...   =>  f = lambda x : ...
sed -i -e "s/\([$w]*\) *\xe2\x86\x92/lambda \1 : /g" "$o";

# [x1 .. x2[  =>  range(x1, x2)
sed -i -e "s/\[ *\([$w]*\) *.. *\([$w]*\) *\[/range(\1,\2)/g" "$o";
# ]x1 .. x2[  =>  range(x1+1, x2)
sed -i -e "s/\] *\([$w]*\) *.. *\([$w]*\) *\[/range(\1+1,\2)/g" "$o";
# [x1 .. x2]  =>  range(x1, x2+1)
sed -i -e "s/\[ *\([$w]*\) *.. *\([$w]*\) *\]/range(\1,\2+1)/g" "$o";
# ]x1 .. x2]  =>  range(x1+1, x2+1)
sed -i -e "s/\] *\([$w]*\) *.. *\([$w]*\) *\]/range(\1+1,\2+1)/g" "$o";

# from x1 to x2  => range(x1, x2+1)
sed -i -e "s/from *\([$w]*\) *to *\([$w]*\) *:/in range(\1,\2+1) :/g" "$o";

# repeat ... until cond => while True: ... if cond: break
sed -i -e "s/repeat/while True/g" "$o";
sed -i -e "s/until\(.*\)/    if(\1) :break/g" "$o";

sed -i -e "s/\( *\)select *\(.*\):/\1__select_var__ = \2\n\1if False: pass/g" "$o";
sed -i -e "s/    case/elif __select_var__ ==/g" "$o";
sed -i -e "s/    default/else/g" "$o";

cpp "$o" > "$o.tmp";

sed '/^#/ d' "$o.tmp" > "$o" && rm "$o.tmp";
sed -i 's/#.*$//;/^$/d' "$o";
sed -i 's/; *$//g' "$o";
sed -i 's/\xe2\x9f\xa9\([+-]\)\xe2\x9f\xa8/\1/g' "$o";
sed -i 's/\xe2\x9f\xa9\([+-]\)\xe2\x9f\xa8/\1/g' "$o";
sed -i 's/\xe2\x9f\xa9/]/g;s/\xe2\x9f\xa8/[/g' "$o";

rm numbered.mac
if [ "$1" != "$i" ]; then
    rm "$i";
fi

python3 "$o";

if !([[ "$*" == *"--save"* ]]); then
    rm "$o";
fi
