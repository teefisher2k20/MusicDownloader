# Contributing to UMDM+

Thank you for your interest in contributing to the Universal Media Downloader, Converter, and Manager Plus (UMDM+)! This document provides guidelines for contributing to the project.

## 🤝 How to Contribute

### Reporting Bugs

1. Check if the bug has already been reported in [Issues](https://github.com/yourusername/umdm-plus/issues)
2. If not, create a new issue with:
   - Clear, descriptive title
   - Steps to reproduce
   - Expected vs actual behavior
   - Screenshots (if applicable)
   - Environment details (OS, browser, version)

### Suggesting Features

1. Check [existing feature requests](https://github.com/yourusername/umdm-plus/issues?q=is%3Aissue+label%3Aenhancement)
2. Create a new issue with:
   - Clear feature description
   - Use case and benefits
   - Potential implementation approach
   - Any mockups or examples

### Code Contributions

#### Prerequisites

- Node.js 18+ installed
- Python 3.11+ installed
- Git installed
- Code editor (VS Code recommended)

#### Setup Development Environment

```bash
# Fork the repository on GitHub
# Clone your fork
git clone https://github.com/YOUR_USERNAME/umdm-plus.git
cd umdm-plus

# Add upstream remote
git remote add upstream https://github.com/original/umdm-plus.git

# Install dependencies
npm install
pip install -r requirements.txt

# Create a branch
git checkout -b feature/your-feature-name
```

#### Coding Standards

**JavaScript/TypeScript:**

- Use ES6+ features
- Follow [Airbnb Style Guide](https://github.com/airbnb/javascript)
- Use meaningful variable names
- Add JSDoc comments for functions
- Keep functions small and focused

**CSS:**

- Use CSS custom properties (variables)
- Follow BEM naming convention
- Mobile-first responsive design
- Use semantic class names

**Python:**

- Follow [PEP 8](https://pep8.org/)
- Use type hints
- Add docstrings for functions/classes
- Keep functions under 50 lines

#### Commit Guidelines

Follow [Conventional Commits](https://www.conventionalcommits.org/):

```text
feat: add video upscaling feature
fix: resolve download queue bug
docs: update API documentation
style: format code with prettier
refactor: restructure download service
test: add unit tests for converter
chore: update dependencies
```

#### Pull Request Process

1. **Update your branch:**

   ```bash
   git fetch upstream
   git rebase upstream/main
   ```

2. **Run tests:**

   ```bash
   npm test
   npm run lint
   ```

3. **Push to your fork:**

   ```bash
   git push origin feature/your-feature-name
   ```

4. **Create Pull Request:**
   - Clear title and description
   - Link related issues
   - Add screenshots for UI changes
   - Request review from maintainers

5. **PR Checklist:**
   - [ ] Code follows style guidelines
   - [ ] Tests added/updated
   - [ ] Documentation updated
   - [ ] No console errors
   - [ ] Passes all CI checks

## 🏗️ Project Structure

```text
umdm-plus/
├── index.html              # Main application
├── manifest.json           # PWA manifest
├── assets/                 # Images, icons
├── css/                    # Stylesheets
│   └── styles.css
├── js/                     # JavaScript
│   └── app.js
├── docs/                   # Documentation
├── tests/                  # Test files
├── server/                 # Backend (future)
└── ai-services/           # AI services (future)
```

## 🧪 Testing

### Running Tests

```bash
# Run all tests
npm test

# Run specific test suite
npm test -- --grep "download"

# Run with coverage
npm run test:coverage
```

### Writing Tests

```javascript
describe('Download Service', () => {
  it('should validate YouTube URLs', () => {
    const url = 'https://youtube.com/watch?v=test';
    expect(validateUrl(url)).toBe(true);
  });
  
  it('should detect video source', () => {
    const url = 'https://youtube.com/watch?v=test';
    expect(detectVideoSource(url)).toBe('youtube');
  });
});
```

## 📝 Documentation

### Code Documentation

Add JSDoc comments to all functions:

```javascript
/**
 * Downloads a video from the specified URL
 * @param {string} url - The video URL
 * @param {Object} options - Download options
 * @param {string} options.quality - Video quality (e.g., '1080p')
 * @param {string} options.format - Output format (e.g., 'mp4')
 * @returns {Promise<Object>} Download result
 * @throws {Error} If URL is invalid or download fails
 */
async function downloadVideo(url, options) {
  // Implementation
}
```

### README Updates

When adding features, update:

- Feature list
- Usage examples
- Configuration options
- Screenshots/GIFs

## 🎨 Design Guidelines

### UI/UX Principles

1. **Simplicity:** Keep interface clean and intuitive
2. **Consistency:** Use existing components and patterns
3. **Accessibility:** Follow WCAG 2.1 AA standards
4. **Responsiveness:** Mobile-first design
5. **Performance:** Optimize for speed

### Color Palette

```css
Primary Blue:    #2563eb
Primary Purple:  #7c3aed
Success Green:   #10b981
Warning Amber:   #f59e0b
Error Red:       #ef4444
```

## 🔒 Security

### Reporting Security Issues

**DO NOT** open a public issue for security vulnerabilities.

Email security concerns to: <security@umdm.app>

Include:

- Description of vulnerability
- Steps to reproduce
- Potential impact
- Suggested fix (if any)

### Security Best Practices

- Never commit API keys or secrets
- Validate all user inputs
- Sanitize data before rendering
- Use HTTPS everywhere
- Keep dependencies updated

## 📜 Code of Conduct

### Our Pledge

We pledge to make participation in our project a harassment-free experience for everyone, regardless of:

- Age, body size, disability
- Ethnicity, gender identity
- Experience level
- Nationality, personal appearance
- Race, religion, sexual identity

### Our Standards

**Positive behavior:**

- Using welcoming language
- Being respectful of differing viewpoints
- Accepting constructive criticism
- Focusing on what's best for the community
- Showing empathy towards others

**Unacceptable behavior:**

- Trolling, insulting, or derogatory comments
- Public or private harassment
- Publishing others' private information
- Any conduct inappropriate in a professional setting

### Enforcement

Project maintainers will:

- Remove, edit, or reject contributions that violate this code
- Communicate reasons for moderation decisions
- Ban contributors for serious or repeated violations

## 🎓 Learning Resources

### For New Contributors

- [Git Basics](https://git-scm.com/book/en/v2/Getting-Started-Git-Basics)
- [JavaScript MDN Docs](https://developer.mozilla.org/en-US/docs/Web/JavaScript)
- [React Documentation](https://react.dev/)
- [Node.js Guides](https://nodejs.org/en/docs/guides/)

### Project-Specific

- [UMDM+ Specification](UMDM_PLUS_SPECIFICATION.md)
- [Development Roadmap](docs/PROJECT_ROADMAP.md)
- [API Documentation](API.md)

## 💬 Communication

### Channels

- **GitHub Issues:** Bug reports, feature requests
- **GitHub Discussions:** Q&A, ideas, general discussion
- **Discord:** Real-time chat (invite link)
- **Email:** <contact@umdm.app>

### Getting Help

1. Check existing documentation
2. Search closed issues
3. Ask in GitHub Discussions
4. Join Discord for real-time help

## 🏆 Recognition

### Contributors

All contributors are recognized in:

- README Contributors section
- Release notes
- Project website

### Levels of Contribution

- **Contributor:** 1+ merged PR
- **Regular Contributor:** 5+ merged PRs
- **Core Contributor:** Consistent contributions, code reviews
- **Maintainer:** Invited by project leads

## 📅 Release Cycle

- **Major releases (v1.0, v2.0):** Every 6-12 months
- **Minor releases (v1.1, v1.2):** Every 1-2 months
- **Patch releases (v1.1.1):** As needed for bug fixes

## ✅ Checklist for First-Time Contributors

- [ ] Read this contributing guide
- [ ] Read the Code of Conduct
- [ ] Set up development environment
- [ ] Find an issue labeled "good first issue"
- [ ] Comment on the issue expressing interest
- [ ] Fork the repository
- [ ] Create a feature branch
- [ ] Make your changes
- [ ] Write/update tests
- [ ] Update documentation
- [ ] Commit with conventional commits
- [ ] Push to your fork
- [ ] Create a pull request
- [ ] Respond to review feedback

## 🙏 Thank You

Every contribution, no matter how small, is valued and appreciated. Whether it's:

- Code contributions
- Bug reports
- Feature suggestions
- Documentation improvements
- Helping other users
- Spreading the word

**You make UMDM+ better for everyone!**

---

Questions? Reach out to the maintainers or ask in GitHub Discussions.
