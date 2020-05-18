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
(Lidová)

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
GIT_EDITOR='echo "Doplnění autora" >' git commit

take_screenshot $OUTFILE.branch1.png gitk --all

git checkout master
git branch doplneni-jmena
git checkout doplneni-jmena
git branch

cat > basnicka.txt << END
Holka Modrooká

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
git status
cat basnicka.txt
git diff

cat > basnicka.txt << END
Holka modrooká
(Lidová)

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
GIT_EDITOR='true' git commit

git branch

take_screenshot $OUTFILE.merge.png gitk --all

git branch -d doplneni-autora
git branch -d doplneni-jmena
git branch
