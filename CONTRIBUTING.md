# Contributing to Text2SQL

Thank you for your interest in contributing to Text2SQL! This document provides guidelines for contributing to the project.

## Code of Conduct

Be respectful and inclusive. We welcome contributions from everyone.

## How to Contribute

### Reporting Bugs

1. Check if the bug has already been reported in Issues
2. If not, create a new issue with:
   - Clear title and description
   - Steps to reproduce
   - Expected vs actual behavior
   - Environment details (OS, Python version, etc.)

### Suggesting Enhancements

1. Check if the enhancement has been suggested
2. Create a new issue with:
   - Clear description of the enhancement
   - Use cases and benefits
   - Possible implementation approach

### Pull Requests

1. **Fork the repository**
2. **Create a feature branch**
   ```bash
   git checkout -b feature/your-feature-name
   ```

3. **Make your changes**
   - Follow the code style (black, isort)
   - Add tests for new functionality
   - Update documentation as needed

4. **Test your changes**
   ```bash
   make test
   make lint
   ```

5. **Commit your changes**
   ```bash
   git commit -m "Add feature: description"
   ```

6. **Push to your fork**
   ```bash
   git push origin feature/your-feature-name
   ```

7. **Create a Pull Request**
   - Provide a clear description
   - Reference related issues
   - Wait for review

## Development Setup

```bash
# Clone your fork
git clone https://github.com/yourusername/LLM-Finetuning.git
cd LLM-Finetuning

# Install development dependencies
make install-dev

# Run tests
make test
```

## Code Style

We use:
- **black** for code formatting
- **isort** for import sorting
- **flake8** for linting
- **mypy** for type checking

Run formatters before committing:
```bash
make format
make lint
```

## Testing

- Write tests for new features
- Ensure all tests pass before submitting PR
- Aim for >80% code coverage

```bash
pytest tests/ --cov=src/text2sql
```

## Documentation

- Update README.md for user-facing changes
- Add docstrings to new functions/classes
- Update relevant documentation in docs/

## Questions?

Feel free to open an issue for questions or clarifications.

Thank you for contributing! 🎉
