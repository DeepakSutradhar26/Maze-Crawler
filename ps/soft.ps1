param(
    [string]$Message
)

git reset --soft HEAD~1
git add .
git commit -m $Message
git push origin main --force