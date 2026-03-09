# Contributing to MagLogic

This project follows the [alawein org contributing standards](https://github.com/alawein/alawein/blob/main/CONTRIBUTING.md). Guidelines for contributing to MagLogic.

## Table of Contents
- [Code of Conduct](#code-of-conduct)
- [Getting Started](#getting-started)
- [Development Setup](#development-setup)
- [Contributing Guidelines](#contributing-guidelines)
- [Pull Request Process](#pull-request-process)
- [Coding Standards](#coding-standards)
- [Testing](#testing)
- [Documentation](#documentation)
- [Community](#community)

## Code of Conduct

Be respectful in discussions. Focus on constructive feedback. Help others learn.

## Getting Started

### Prerequisites
- Python 3.8 or higher
- Git for version control
- Basic understanding of micromagnetism and computational physics
- Familiarity with OOMMF and/or MuMax3 (helpful but not required)

### Ways to help
- Report bugs and suggest features
- Submit code fixes and new functionality  
- Improve documentation and examples
- Add test cases

## Development Setup

### 1. Fork and Clone
```bash
# Fork the repository on GitHub, then clone your fork
git clone https://github.com/YOUR_USERNAME/MagLogic.git
cd MagLogic

# Add upstream remote
git remote add upstream https://github.com/alawein/maglogic.git
```

### 2. Environment Setup
```bash
# Create virtual environment
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate

# Install development dependencies
pip install -e python/[dev]
```

### 3. Pre-commit Hooks
```bash
# Install pre-commit hooks
pre-commit install

# Test the hooks
pre-commit run --all-files
```

### 4. Verify Installation
```bash
# Run tests to ensure everything works
cd python
pytest tests/ -v

# Check code formatting
black --check maglogic/
flake8 maglogic/
```

## Contributing Guidelines

### Bug reports
Search existing issues first. Include:
- MagLogic version
- Python version and OS  
- Steps to reproduce
- Expected vs actual behavior
- Error messages

### Feature requests
Explain the use case and benefit. Consider backwards compatibility.

## Pull Request Process

### 1. Preparation
```bash
# Update your fork
git fetch upstream
git checkout main
git merge upstream/main

# Create feature branch
git checkout -b feature/descriptive-name
```

### 2. Development
- Make focused, atomic commits
- Write clear commit messages
- Follow coding standards (see below)
- Add/update tests for new functionality
- Update documentation as needed

### 3. Testing
```bash
# Run full test suite
pytest tests/ -v

# Check code coverage
pytest tests/ --cov=maglogic --cov-report=html

# Run linting
black maglogic/
flake8 maglogic/
mypy maglogic/
```

### 4. Submission
```bash
# Push to your fork
git push origin feature/descriptive-name

# Create pull request on GitHub
```

### 5. Review Process
- Automated checks must pass (CI/CD pipeline)
- Code review by maintainers
- Address feedback and update as needed
- Maintainer approval required for merge

## Coding Standards

### Python Style
- Follow **PEP 8** with line length limit of 88 characters
- Use **Black** for automatic code formatting
- Use **isort** for import sorting
- Type hints required for all public functions

### Code Organization
```python
"""Module docstring.

Brief description of the module's purpose and functionality.

Author: Your Name
Email: your.email@example.com
License: MIT
"""

import standard_library
import third_party_packages

from maglogic import local_imports


class ExampleClass:
    """Class docstring following Google style."""
    
    def __init__(self, param: str) -> None:
        """Initialize the class."""
        self.param = param
    
    def public_method(self, arg: int) -> bool:
        """
        Public method with comprehensive docstring.
        
        Args:
            arg: Description of argument
            
        Returns:
            Description of return value
            
        Raises:
            ValueError: When arg is invalid
        """
        return self._private_method(arg)
    
    def _private_method(self, arg: int) -> bool:
        """Private method (brief docstring acceptable)."""
        return arg > 0
```

### Docstring Standards
Use **Google-style docstrings** for all public methods:

```python
def analyze_magnetization(data: np.ndarray, threshold: float = 0.1) -> Dict[str, Any]:
    """
    Analyze magnetization patterns in simulation data.
    
    This function performs comprehensive analysis of magnetization data,
    including domain detection, energy calculations, and topological
    characterization.
    
    Args:
        data: Magnetization data array with shape (nx, ny, nz, 3)
        threshold: Threshold for domain detection (default: 0.1)
        
    Returns:
        Dictionary containing analysis results:
        - 'domains': Number of magnetic domains detected
        - 'energy': Total magnetic energy
        - 'topology': Topological charge
        
    Raises:
        ValueError: If data has invalid shape
        TypeError: If data is not a numpy array
        
    Example:
        >>> import numpy as np
        >>> data = np.random.rand(10, 10, 1, 3)
        >>> results = analyze_magnetization(data)
        >>> print(f"Found {results['domains']} domains")
    """
```

### Error Handling
- Use specific exception types
- Provide helpful error messages
- Include context in error messages
- Handle edge cases gracefully

```python
def parse_ovf_file(filepath: Path) -> Dict[str, Any]:
    """Parse OVF file with comprehensive error handling."""
    if not filepath.exists():
        raise FileNotFoundError(f"OVF file not found: {filepath}")
    
    if filepath.suffix.lower() != '.ovf':
        raise ValueError(f"Expected .ovf file, got: {filepath.suffix}")
    
    try:
        with open(filepath, 'r') as f:
            content = f.read()
    except PermissionError:
        raise PermissionError(f"Cannot read OVF file: {filepath}")
    except UnicodeDecodeError:
        # Try binary mode for binary OVF files
        pass
```

## Testing

### Test Structure
```
tests/
├── test_parsers.py       # Parser functionality tests
├── test_analysis.py      # Analysis module tests  
├── test_simulation.py    # Simulation runner tests
├── test_integration.py   # Integration tests
├── conftest.py          # Shared fixtures
└── benchmarks/          # Performance tests
    └── test_performance.py
```

### Writing Tests
```python
import pytest
import numpy as np
from maglogic.parsers import OOMMFParser


class TestOOMMFParser:
    """Test OOMMF parser functionality."""
    
    @pytest.fixture
    def parser(self):
        """Create parser instance."""
        return OOMMFParser()
    
    @pytest.fixture
    def sample_ovf_content(self):
        """Create sample OVF file content."""
        return """# OOMMF OVF 2.0
# ... OVF content ...
"""
    
    def test_parse_ovf_valid_file(self, parser, tmp_path, sample_ovf_content):
        """Test parsing valid OVF file."""
        ovf_file = tmp_path / "test.ovf"
        ovf_file.write_text(sample_ovf_content)
        
        result = parser.parse_ovf(ovf_file)
        
        assert 'magnetization' in result
        assert 'metadata' in result
        # More specific assertions...
    
    def test_parse_ovf_invalid_file(self, parser, tmp_path):
        """Test error handling for invalid files."""
        invalid_file = tmp_path / "invalid.ovf"
        invalid_file.write_text("not an ovf file")
        
        with pytest.raises(ParseError):
            parser.parse_ovf(invalid_file)
    
    @pytest.mark.benchmark
    def test_parse_large_ovf_performance(self, benchmark, parser, large_ovf_file):
        """Test parsing performance on large files."""
        result = benchmark(parser.parse_ovf, large_ovf_file)
        assert result is not None
```

### Test Categories
- **Unit Tests**: Test individual functions and methods
- **Integration Tests**: Test component interactions
- **Performance Tests**: Benchmark critical operations
- **Regression Tests**: Prevent known issues from reoccurring

### Test Markers
```python
@pytest.mark.slow           # Long-running tests
@pytest.mark.gpu            # Requires GPU hardware
@pytest.mark.oommf         # Requires OOMMF installation
@pytest.mark.mumax3        # Requires MuMax3 installation
@pytest.mark.integration   # Integration tests
@pytest.mark.benchmark     # Performance benchmarks
```

## Documentation

### Building Documentation
```bash
# Install documentation dependencies
pip install -e python/[docs]

# Build HTML documentation
cd docs
sphinx-build -b html . _build/html

# Live documentation server
sphinx-autobuild . _build/html --port 8080
```

### Documentation Types
- **API Documentation**: Auto-generated from docstrings
- **User Guide**: Conceptual explanations and workflows
- **Tutorials**: Step-by-step instructions
- **Examples**: Practical usage scenarios

### Writing Guidelines
- Use clear, concise language
- Include working code examples
- Add diagrams and figures when helpful
- Cross-reference related sections
- Keep documentation synchronized with code

## Community

### Communication Channels
- **GitHub Issues**: Bug reports and feature requests
- **GitHub Discussions**: General questions and ideas
- **Pull Requests**: Code contributions and reviews

### Getting Help
- Check existing documentation and examples
- Search closed issues for similar problems
- Ask specific questions with code examples
- Be patient and respectful when requesting help

Contributors are listed in CONTRIBUTORS.md and release notes.

## Release Process

### Version Numbering
MagLogic follows [Semantic Versioning](https://semver.org/):
- **MAJOR**: Incompatible API changes
- **MINOR**: New functionality (backwards compatible)
- **PATCH**: Bug fixes (backwards compatible)

### Release Checklist
- [ ] All tests pass
- [ ] Documentation updated
- [ ] CHANGELOG.md updated
- [ ] Version bumped in relevant files
- [ ] Git tag created
- [ ] PyPI package published
- [ ] Docker images updated
- [ ] GitHub release created

## License

By contributing to MagLogic, you agree that your contributions will be licensed under the MIT License.

## Questions?

If you have questions about contributing, please:
1. Check this document and existing documentation
2. Search existing issues and discussions
3. Open a new discussion on GitHub
4. Contact the maintainers directly

Thank you for contributing to MagLogic! Your efforts help advance the field of nanomagnetic logic and computational magnetism.

---

**MagLogic Development Team**  
UC Berkeley Nanomagnetic Logic Research  
Meshal Alawein