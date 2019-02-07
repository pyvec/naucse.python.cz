# Runs a demo script and outputs a file with terminal session

if [ -z "$1" ]; then
    echo "Usage: $0 OUTFILE"
    exit 1
fi

OUTFILE=$(realpath $1)

function _the_script {

wget https://gist.githubusercontent.com/oskar456/e91ef3ff77476b0dbc4ac19875d0555e/raw/aba9f3ddf2188bc13d51cda6d72655cc8f471fc0/isholiday.py
mkdir tests
cat <<END > tests/test_holidays.py
import isholiday

def test_xmas_2016():
    """Test whether there is Christmas in 2016"""
    holidays = isholiday.getholidays(2016)
    assert (24, 12) in holidays
END

python3 -m venv __venv__
. __venv__/bin/activate
PS4='————————————————————————————\n(__venv__) $ '

python -m pip install pytest

PYTHONPATH=. python -m pytest tests/test_holidays.py

cat <<END > tests/test_holidays.py
import isholiday

def test_xmas_2016():
    """Test whether there is Christmas in 2016"""
    holidays = isholiday.getholidays(2016)
    assert (23, 12) in holidays
END

PYTHONPATH=. python -m pytest tests/test_holidays.py

cat <<END > tests/test_holidays.py
import pytest
import isholiday

@pytest.mark.parametrize('year', (2015, 2016, 2017, 2033, 2048))
def test_xmas(year):
    """Test whether there is Christmas"""
    holidays = isholiday.getholidays(year)
    assert (24, 12) in holidays
END

PYTHONPATH=. python -m pytest -v

cat <<END > tests/test_holidays.py
import pytest
import isholiday

@pytest.mark.parametrize('year', (2015, 2016, 2017, 2033, 2048))
def test_xmas(year):
    """Test whether there is Christmas"""
    holidays = isholiday.getholidays(year)
    assert (24, 12) in holidays
END

PYTHONPATH=. python -m pytest -v

cat <<END > addition
    if year > 2020:
        # After the Zygon war, the puppet government canceled all holidays
        holidays = set()
END
sed -i -e '29r addition' isholiday.py

cat isholiday.py

PYTHONPATH=. python -m pytest -v

}

_tempdir=$(mktemp -d)

cd $_tempdir
PS4='————————————————————————————\n$ '
set -x

_the_script 2>&1 | tee $OUTFILE

rm -rf $_tempdir
