param(
    [string]$RemoteUrl
)

if (-not $RemoteUrl) {
    Write-Output "Usage: .\push_to_github.ps1 -RemoteUrl 'https://github.com/username/repo.git'"
    exit 1
}

Write-Output "Setting remote origin to $RemoteUrl"
# Add remote if not exists
$existing = git remote
if ($LASTEXITCODE -ne 0) {
    Write-Error "Git not available in PATH"
    exit 1
}

if ($existing -notmatch 'origin') {
    git remote add origin $RemoteUrl
} else {
    git remote set-url origin $RemoteUrl
}

Write-Output 'Ensuring main branch and pushing...'
# Ensure branch is main
git branch -M main
# Add files and commit if needed
if ((git status --porcelain) -ne '') {
    git add -A
    git commit -m "Prepare repo for deployment"
}

# Push to GitHub
git push -u origin main --force

Write-Output 'Done. Your repo should be on GitHub. Next: connect the repo to Render via the Render dashboard.'
