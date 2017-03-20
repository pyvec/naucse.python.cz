# Runs a Git demo script and outputs a file with terminal escape sequences
# where \e is substituted for the visible character `␛`.

if [ -z "$1" ]; then
    echo "Usage: $0 OUTFILE"
    exit 1
fi

OUTFILE=$(realpath $1)

export second_msg='
Rozdělení dlouhých řádků

Verše básně se většinou píšou na jednotlivé řádky. Myslím, že
takhle se to líp čte. (Ale, co si budeme povídat, hlavní 
důvod je ukázat co dělá git diff.)
'

function _the_script {

git init

git status

cat > basnicka.txt << END
Holka modrooká, nesedávej u potoka
Holka modrooká, nesedávej tam

V potoce je hastrmánek
Zatahá tě za copánek
Holka modrooká, nesedávej tam
END

git status
git add basnicka.txt
git status
GIT_EDITOR='echo "První revize" >' git commit

git status
git show

cat > basnicka.txt << END
Holka modrooká
Nesedávej u potoka
Holka modrooká
Nesedávej tam

V potoce je hastrmánek
Zatahá tě za copánek
Holka modrooká
Nesedávej tam
END

git status
git diff
git add basnicka.txt
git status

GIT_EDITOR="echo \"$second_msg\" >" git commit

git show
git log

git config -l

take_screenshot $OUTFILE.gitk.png gitk --all

git add basnicka.txt
GIT_EDITOR="echo \"$second_msg\" >" git commit

git branch
git branch doplneni-autora
git branch
git checkout doplneni-autora
git branch

cat > basnicka.txt << END
Holka modrooká
Nesedávej u potoka
Holka modrooká
Nesedávej tam

V potoce je hastrmánek
Zatahá tě za copánek
Holka modrooká
Nesedávej tam

- Lidová
END

git add basnicka.txt
GIT_EDITOR='echo "Doplnění autora" >' git commit

take_screenshot $OUTFILE.branch1.png gitk --all

git checkout master
git branch doplneni-jmena
git checkout doplneni-jmena
git branch

cat > basnicka.txt << END
Holka modrooká
=========

Holka modrooká
Nesedávej u potoka
Holka modrooká
Nesedávej tam

V potoce je hastrmánek
Zatahá tě za copánek
Holka modrooká
Nesedávej tam
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
