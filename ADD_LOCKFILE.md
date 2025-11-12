# How to fix "Dependencies lock file is not found" in CI

Cause
- CI requires a lock file (yarn.lock, package-lock.json, or npm-shrinkwrap.json). The repository currently lacks one.

Steps (recommended)

1. Generate and commit the lock file locally:

- Yarn:
```
yarn install
git add yarn.lock
git commit -m "chore: add yarn.lock"
git push
```

- npm:
```
npm install --package-lock-only
git add package-lock.json
git commit -m "chore: add package-lock.json"
git push
```

2. Ensure .gitignore does not exclude the lockfile.
3. Re-run CI.

Notes
- Prefer committing a lock file in source control for reproducible builds.
