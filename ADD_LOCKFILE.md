# Adding a Lock File

CI requires a lock file (yarn.lock, package-lock.json, or npm-shrinkwrap.json). The repository currently lacks one.

## Steps (recommended)

Generate and commit the lock file locally:

**Yarn:**

```bash
yarn install
git add yarn.lock
git commit -m "chore: add yarn.lock"
git push
```

**npm:**

```bash
npm install --package-lock-only
git add package-lock.json
git commit -m "chore: add package-lock.json"
git push
```

Ensure `.gitignore` does not exclude the lockfile.

Re-run CI.

## Notes

- Prefer committing a lock file in source control for reproducible builds.
- Update the CI workflow file at `.github/workflows/ci.yml` to make the install step tolerant of a missing lockfile. Replace the existing install step (the step that runs dependency installation) with the following YAML snippet. This snippet checks for `yarn.lock` and `package-lock.json`, and falls back to `npm install` when no lockfile exists — preventing the job from failing immediately when a lockfile is missing.

```yaml
- name: Install dependencies
  run: |
    if [ -f yarn.lock ]; then
      echo "yarn.lock found — running yarn install"
      yarn install --frozen-lockfile
    elif [ -f package-lock.json ]; then
      echo "package-lock.json found — running npm ci"
      npm ci
    elif [ -f package.json ]; then
      echo "No lockfile found — running npm install (will generate package-lock.json locally)"
      npm install
    else
      echo "No package.json found — skipping install"
    fi
```
