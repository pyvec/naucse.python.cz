# Runs a Git demo script and outputs a file with terminal escape sequences
# where \e is substituted for the visible character `␛`.

if [ -z "$2" ]; then
    echo "Usage: $0 SCRIPT OUTFILE"
    exit 1
fi

THE_SCRIPT=$(realpath $1)
OUTFILE=$(realpath $2)

export second_msg='
Rozdělení dlouhých řádků

Verše básně se většinou píšou na jednotlivé řádky. Myslím, že
takhle se to líp čte. (Ale, co si budeme povídat, hlavní
důvod je ukázat co dělá git diff.)
'

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

cd $_confdir
python3 -m venv env
. env/bin/activate

cd $_tempdir
PS4='————————————————————————————\n\e[36m$\e[0m '
set -x

source $THE_SCRIPT 2>&1 | tee $OUTFILE
sed -i -e's/\x1b/␛/g' $OUTFILE

rm -rf $_tempdir
rm -rf $_confdir
