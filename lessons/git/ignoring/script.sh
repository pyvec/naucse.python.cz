git init

cat > obrazek.py << END
from turtle import forward, left, right, getcanvas

forward(50)
left(60)
forward(50)
right(60)
forward(50)

getcanvas().postscript(file='obrazek.ps')
END

cat > poznamky.txt << END
Tajné!
END

cat > Autofile.tmp << END
Blablabla
END

python obrazek.py
git status

cat > .gitignore << END
__pycache__/
*.pyc

obrazek.ps
END

git status
git add .gitignore obrazek.py
git status


cat > .git/info/exclude << END
/poznamky.txt
END

git status

cat > ~/.gitignore_global << END
Autofile.tmp
END

git config --global core.excludesfile ~/.gitignore_global

git status


GIT_EDITOR='echo "První revize" >' git commit
git status
