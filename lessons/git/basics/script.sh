# Runs a Git demo script and outputs a file with terminal escape sequences
# where \e is substituted for the visible character `␛`.

if [ -z "$1" ]; then
    echo "Usage: $0 OUTFILE"
    exit 1
fi

OUTFILE=$(realpath $1)

export second_msg='
Druhá sloka: Sloučení posledních dvou řádků

Sloučení řádků rozbíjí monotónnost formy básně – nestejný počet
veršů ve sloce je prý moderní. (Ale, co si budeme povídat, hlavní 
důvod je líp ukázat co dělá `git diff`.)

Použití vykřičníku místo čárky zdůrazňuje naléhavost situace.
'

function _the_script {

git init

git status

cat > basnicka.txt << END
Haló haló
co se stalo?
Kolo se mi polámalo

Jaké kolo?
Favoritka,
přeletěl jsem přes řidítka

Co jste dělal?
Blbnul jsem,
do příkopy zahnul jsem
END

git status
git add basnicka.txt
git status
GIT_EDITOR='echo "První revize" >' git commit

git status
git show

cat > basnicka.txt << END
Haló haló
co se stalo?
Kolo se mi polámalo

Jaké kolo?
Favoritka! Přeletěl jsem přes řidítka!

Co jste dělal?
Blbnul jsem,
do příkopy zahnul jsem
END

git status
git diff
git add basnicka.txt
git status

GIT_EDITOR="echo \"$second_msg\" >" git commit

git show
git log

git config -l
}

_tempdir=$(mktemp -d)
_confdir=$(mktemp -d)

export HOME=$_confdir
cat > $_confdir/.gitconfig << END
[user]
    name = Adéla Novotná
    email = adela.novotna@example.cz
[color]
    ui = always
END

cd $_tempdir
PS4='————————————————————————————\n\e[36m$\e[0m '
set -x

_the_script 2>&1 | tee $OUTFILE
sed -i -e's/\x1b/␛/g' $OUTFILE

rm -rf $_tempdir
rm -rf $_confdir
