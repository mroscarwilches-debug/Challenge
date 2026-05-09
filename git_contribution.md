# Git Workflow Guidelines

This document defines the branch naming, commit message, and Pull Request structure for the training work between Miguel and Oscar.

## 1. Branch Naming Convention

Use clear, short, and consistent branch names. Format: `type/short-description`.

Common branch types:
- `feature/` for new functionality or app improvements
- `doc/` for documentation only
- `bugfix/` for bug fixes
- `chore/` for maintenance tasks, tooling, or environment updates
- `test/` for test-related work

Examples:
- `feature/gym-calculator`
- `doc/branch-guidelines`
- `bugfix/login-error`
- `chore/update-dependencies`
- `test/add-unit-tests`

### Branch naming rules

- Use lowercase letters and hyphens
- Keep names descriptive but short
- Avoid spaces and special characters
- Include the main purpose of the branch

## 2. Commit Message Structure

Use a consistent commit style to make history readable.

Format:

`<type>(<scope>): <short summary>`

Where:
- `type` is one of: `feat`, `fix`, `docs`, `style`, `refactor`, `perf`, `test`, `chore`
- `scope` is optional and indicates the area affected
- `short summary` is a one-line description

Examples:
- `feat(gym): add kg to lb conversion script`
- `fix(api): correct user validation`
- `docs(workflow): add branch naming guide`
- `test(calc): add unit tests for calculator`
- `chore(deps): update python dependencies`

### Commit body

If more detail is needed, add a body after a blank line:

- Explain why the change was made
- Mention any relevant issue or task
- Note any breaking changes if they exist

Example:

```
fix(gym): correct kg to lb conversion formula

The previous formula used an inaccurate conversion factor.
Updated tests and verified output for common gym weights.
```

## 3. Pull Request Structure

Use the same structure for every PR so the reviewer can understand the change quickly.

### PR title

`<type>: <short description>`

Examples:
- `feat: add kg to lb conversion calculator`
- `docs: add git workflow guidelines`
- `fix: resolve branch naming issue`

### PR description template

1. Summary
   - What changed?
   - Why is this change needed?

2. Scope
   - Which files or feature areas were affected?

3. Checklist
   - [ ] Branch name follows convention
   - [ ] Commit messages follow style
   - [ ] Code has been tested
   - [ ] Documentation updated when necessary

4. Notes
   - Additional context, deployment notes, or follow-up work

### Review and merge

- Use GitHub reviews for comments and approval
- Make small, focused PRs when possible
- Rebase or merge from `main` before final merge
- Ensure the branch is up to date and passes any checks

## 4. Common Scenarios

### 4.1 Creating documentation

Branch type: `doc/`
Commit type: `docs`
PR title example: `docs: add workflow and git rules`

### 4.2 Creating code or a new feature

Branch type: `feature/`
Commit type: `feat`
PR title example: `feat: add gym challenge script`

### 4.3 Fixing bugs

Branch type: `bugfix/`
Commit type: `fix`
PR title example: `fix: correct kg to lb conversion`

### 4.4 Refactoring or cleaning code

Branch type: `refactor/`
Commit type: `refactor`
PR title example: `refactor: improve calculator structure`

### 4.5 Adding tests

Branch type: `test/`
Commit type: `test`
PR title example: `test: add unit tests for gym utilities`

### 4.6 Environment and tooling changes

Branch type: `chore/`
Commit type: `chore`
PR title example: `chore: add docker support for gym app`

## 5. Practical rules for the training series

- Create one branch per task or lesson
- Keep PRs small and reviewable
- Use the PR description to explain the purpose and next step
- Add comments in code for learning and clarity
- Always include one first sentence summary in the PR description
- Keep the developer and reviewer roles clear: you create the branch and PR, Oscar reviews and merges
