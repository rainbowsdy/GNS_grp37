# AGENTS.md

## Build Commands
- Install dependencies: `pip install -r requirements.txt`
- Create virtual environment: `python3 -m venv venv`
- Activate virtual environment: `source venv/bin/activate` (Linux/Mac) or `venv\Scripts\activate` (Windows)
- Install in development mode: `pip install -e .`
- Install with development dependencies: `pip install -r requirements.txt && pip install pytest black flake8 mypy`

## Test Commands
- Run all tests: `pytest`
- Run single test file: `pytest tests/test_filename.py`
- Run single test method: `pytest tests/test_filename.py::TestClass::test_method`
- Run tests with coverage: `pytest --cov=src --cov-report=html`
- Run tests in verbose mode: `pytest -v`
- Run tests matching pattern: `pytest -k "test_pattern"`
- Generate test report: `pytest --html=report.html`

## Linting and Code Quality
- Code formatting with Black: `black .`
- Check formatting: `black --check .`
- Lint with flake8: `flake8 src/`
- Type checking with mypy: `mypy src/`
- Run all quality checks: `black --check . && flake8 src/ && mypy src/`

## Development Workflow
- Run pipeline with default config: `python pipeline.py`
- Run pipeline with custom config: `python pipeline.py -f templates/my_config.yaml`
- Run in verbose mode: `python pipeline.py -v`
- Dry run (no output files): `python pipeline.py -n`
- Show help: `python pipeline.py --help`

## Code Style Guidelines

### General Principles
- Code should be self-explanatory; avoid unnecessary comments
- Follow the principle of "one responsibility per function"
- Use descriptive variable and function names
- Prefer readability over cleverness
- Write code that is easy to test and maintain

### Python Version and Imports
- Target Python 3.8+ (current minimum based on codebase patterns)
- Standard library imports first, then blank line, then third-party imports
- Group imports alphabetically within each group
- Use absolute imports for intra-package references
- Avoid wildcard imports (`from module import *`)

### Naming Conventions
- **Functions and variables**: snake_case (`process_data`, `config_file`)
- **Classes**: PascalCase (`RouterConfig`, `NetworkInterface`)
- **Constants**: UPPER_SNAKE_CASE (`DEFAULT_TIMEOUT`, `CONFIG_PATH`)
- **Private methods/functions**: prefix with single underscore (`_parse_config`)
- **Dunder methods**: use double underscores appropriately (`__init__`, `__repr__`)

### Type Hints
- Use type hints for all function parameters and return types
- Use `typing` module for complex types (List, Dict, Optional, etc.)
- Example: `def process_router(router: Dict[str, Any]) -> RouterConfig:`
- Use Union types for multiple possible types
- Use Optional for parameters that can be None

### String Formatting
- Use f-strings for string interpolation: `f"Router {router_id} configured"`
- Use .format() for complex formatting or when f-strings are not suitable
- Avoid % formatting except for logging compatibility

### Data Structures
- Initialize lists as `[]` instead of `None` in `__init__` methods
- Initialize dicts as `{}` instead of `None`
- Use list/dict/set comprehensions for simple transformations
- Prefer dataclasses or named tuples for structured data over plain dicts when appropriate

### Error Handling
- Raise descriptive exceptions with meaningful messages
- Use custom exception classes for domain-specific errors
- Catch specific exceptions rather than broad `Exception`
- Use context managers (`with` statements) for resource management
- Prefer `ValueError` and `AttributeError` for validation errors
- Use `LookupError` for missing data scenarios

### File and Path Handling
- Use `pathlib.Path` instead of `os.path` for path operations
- Use context managers for file operations (`with open(...) as f:`)
- Handle encoding explicitly when reading/writing text files
- Validate file existence before operations

### Functions and Methods
- Keep functions focused on single responsibility (max 30-50 lines)
- Use early returns to reduce nesting
- Document complex logic with clear variable names
- Use default arguments sparingly and carefully
- Return meaningful values or raise exceptions, avoid side effects

### Classes and Objects
- Implement `__repr__` methods for debugging: `def __repr__(self) -> str: return f"{self.__class__.__name__}(...)"`
- Use properties for computed attributes
- Keep `__init__` methods simple; move complex setup to separate methods
- Use class methods for alternative constructors

### Constants and Configuration
- Define constants at module level
- Use environment variables for runtime configuration
- Avoid hardcoding values in business logic
- Group related constants in classes or enums

### Testing Guidelines
- Write tests for all public functions and methods
- Use descriptive test names: `test_process_router_with_valid_config`
- Test both success and failure cases
- Use fixtures for common test setup
- Mock external dependencies
- Test edge cases and boundary conditions

### Documentation
- Use docstrings for all public functions, classes, and modules
- Follow Google/NumPy docstring format
- Document parameters, return values, and raised exceptions
- Keep docstrings concise but informative

### Logging
- Use the `logging` module instead of `print` statements
- Configure appropriate log levels (DEBUG, INFO, WARNING, ERROR)
- Include relevant context in log messages
- Avoid logging sensitive information

### Security Considerations
- Validate all input data from external sources
- Use safe YAML loading (`yaml.safe_load`)
- Avoid shell injection by using subprocess with lists instead of strings
- Handle secrets securely (environment variables, not hardcoded)
- Validate file paths to prevent directory traversal

### Performance
- Use generators for large data processing
- Avoid unnecessary list comprehensions when iteration is sufficient
- Profile code before optimizing
- Consider memory usage for large configurations

### YAML Configuration Handling
- Use consistent key naming (snake_case for YAML keys)
- Validate configuration structure before processing
- Provide clear error messages for invalid configurations
- Support both single AS and multi-AS formats as documented in README

### Template Management (Jinja2)
- Keep templates readable and well-formatted
- Use meaningful variable names in templates
- Escape variables appropriately for Cisco config context
- Test templates with various data scenarios

### Output Generation
- Ensure atomic writes (write to temp file, then rename)
- Create directory structure as needed
- Validate output before writing to disk
- Provide progress feedback for long operations

## Project-Specific Patterns

### Router Processing Pipeline
- Follow the established step pattern (step1, step2, etc.)
- Each step should be idempotent and testable independently
- Pass data structures between steps cleanly
- Use consistent data formats within the pipeline

### AS and Router Data Structures
- Use dict-based structures for flexibility
- Include hostname as "AS:Router" format
- Maintain interface lists with consistent naming
- Preserve original YAML data for debugging

### BGP Configuration
- Handle peer, client, provider relationships correctly
- Implement iBGP and eBGP configurations
- Validate BGP neighbor relationships
- Support route reflection and confederations

## Tool Integration

### Git Workflow
- Use feature branches for development
- Write clear commit messages
- Include tests with new features
- Run quality checks before committing

### IDE/Editor Setup
- Configure Black as the formatter
- Enable flake8/mypy in IDE
- Use Python type checking in editor
- Configure line length to 88 (Black default)

## Troubleshooting
- Check Python version compatibility
- Verify virtual environment activation
- Ensure all dependencies are installed
- Validate YAML syntax before processing
- Check file permissions for output directories</content>
<parameter name="filePath">AGENTS.md