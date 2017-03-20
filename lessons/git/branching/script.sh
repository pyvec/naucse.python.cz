# Runs a Git demo script and outputs a file with terminal escape sequences
# where \e is substituted for the visible character `␛`.
# This one also takes some screenshots.

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

git add basnicka.txt
GIT_EDITOR='echo "První revize" >' git commit

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

git add basnicka.txt
GIT_EDITOR="echo \"$second_msg\" >" git commit

git branch
git branch doplneni-autora
git branch
git checkout doplneni-autora
git branch

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

- Jaromír Nohavica
END

git add basnicka.txt
GIT_EDITOR='echo "Doplnění autora" >' git commit

take_screenshot $OUTFILE.branch1.png gitk --all

git checkout master
git branch doplneni-jmena
git checkout doplneni-jmena
git branch

cat > basnicka.txt << END
Haló haló
=========

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

git add basnicka.txt
GIT_EDITOR='echo "Doplnění jména" >' git commit

take_screenshot $OUTFILE.branches.png gitk --all

git checkout master
git merge doplneni-jmena
git merge doplneni-autora
git branch

take_screenshot $OUTFILE.merge.png gitk --all

git branch -d doplneni-autora
git branch -d doplneni-jmena
git branch

}

function take_screenshot {
    screenshot_name=$1
    shift
    $* &
    pid=$!
    sleep 0.5
    /usr/bin/import -window root $screenshot_name
    kill $pid
    wait
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
