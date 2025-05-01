# Perplexity Core Framework

<p align="center">
  <img src="https://cdn.prod.website-files.com/5da60b8bfc98fdf11111b791/667d8a67dcf144284eeb44a5_What%20is%20Perplexity%20AI%20and%20How%20to%20Use%20It.webp" alt="Perplexity Core Logo" width="400" height="200">
</p>

<p align="center">
  <strong>A professional framework for building intelligent applications with Perplexity AI</strong>
</p>

<p align="center">
  <a href="#installation">Installation</a> •
  <a href="#virtual-environment">Virtual Environment</a> •
  <a href="#quickstart">Quickstart</a> •
  <a href="#features">Features</a> •
  <a href="#examples">Examples</a> •
  <a href="#contributing">Contributing</a> •
  <a href="#license">License</a>
</p>

<p align="center">
  <img src="https://img.shields.io/github/license/holasoymalva/perplexity-core" alt="License">
  <img src="https://img.shields.io/github/stars/holasoymalva/perplexity-core" alt="Stars">
  <img src="https://img.shields.io/github/forks/holasoymalva/perplexity-core" alt="Forks">
  <img src="https://img.shields.io/github/issues/holasoymalva/perplexity-core" alt="Issues">
</p>

## 🚀 Overview

Perplexity Core is an enterprise-grade Python framework designed to accelerate development of AI applications using the Perplexity API. Built with flexibility, scalability, and developer experience in mind, it provides a robust foundation for everything from simple prototypes to production-ready AI systems.

The framework abstracts away the complexities of working with Perplexity's sophisticated AI models, allowing developers to focus on building innovative features rather than managing API interactions.

## ✨ Features

- **Comprehensive Client**: Full support for all Perplexity API capabilities with an elegant, Pythonic interface
- **Flexible Configuration System**: Environment variables, JSON files, and programmatic options for seamless integration in any environment
- **Enterprise-Ready Logging**: Robust logging system ready for production deployments
- **Structured Data Models**: Type-hinted models for responses and reliable data handling
- **Response Processing Tools**: Ready-to-use utilities for format conversion, citation extraction, and more
- **Streaming Support**: Built-in handling for streaming responses
- **Full Test Coverage**: Comprehensive test suite ensuring reliability
- **Extensive Documentation**: Complete references and examples for rapid onboarding

## 🛠️ Installation

## 🔮 Virtual Environment

### Setting up a Virtual Environment

We strongly recommend using a virtual environment for development:

```bash
# Clone the repository
git clone https://github.com/holasoymalva/perplexity-core.git
cd perplexity-core

# Create a virtual environment
python -m venv venv

# Activate the virtual environment
# On Windows:
venv\Scripts\activate
# On macOS/Linux:
source venv/bin/activate

# Install dependencies
pip install -r requirements.txt

# Or install in development mode
pip install -e .[dev]
```

You'll know your virtual environment is active when you see `(venv)` prefixed to your command prompt.

To deactivate the virtual environment when you're done:

```bash
deactivate
```

## 🧩 Quickstart

Set up your API key:

```bash
export PERPLEXITY_API_KEY="your-api-key-here"
```

Then in your code:

```python
from src.perplexity_client import PerplexityClient

# Initialize the client
client = PerplexityClient()

# Simple query
response = client.query(
    "What are the potential applications of AI in healthcare?",
    model="sonar-medium-online"
)

# Print the response
print(response.content)

# Use the search capability
search_results = client.search("latest advancements in quantum computing")
print(search_results.content)
```

## 🔍 Examples

The repository includes complete examples to jumpstart your development:

### Basic Usage

```bash
python examples/basic_example.py
```

This demonstrates fundamental query operations with the API.

### Advanced Features

```bash
python examples/advanced_example.py
```

Covers advanced usage including streaming responses, custom parameters, search functionality, and context handling.

## 📚 Documentation

Find comprehensive documentation in the code or visit our [documentation site](#) (coming soon).

Each module and function includes detailed docstrings explaining parameters, return values, and examples.

### Managing Your Environment

For team collaboration and deployment consistency, we recommend:

```bash
# Save your current environment dependencies
pip freeze > requirements-lock.txt

# Create an environment from a requirements file
pip install -r requirements-lock.txt
```

This ensures all team members and deployment environments have identical dependencies.

## 🧠 Architecture

Perplexity Core follows a modular design to maximize flexibility:

```
perplexity-core/
├── src/                   # Core source code
│   ├── perplexity_client.py   # Main client interface
│   ├── models/            # Data models
│   ├── utils/             # Utilities (config, logging)
│   └── handlers/          # Response processors
├── examples/              # Example implementations
├── tests/                 # Test suite
```

## 🔧 Configuration

Perplexity Core offers multiple configuration methods:

- **Environment Variables**: `PERPLEXITY_API_KEY`, `PERPLEXITY_ENV`, etc.
- **Configuration Files**: JSON files in standard locations
- **Programmatic Configuration**: Directly via the `Config` class

Example configuration file:

```json
{
  "api_key": "your-api-key",
  "model": "sonar-medium-online",
  "temperature": 0.7
}
```

## 🤝 Contributing

Contributions are welcome! Please feel free to submit a Pull Request.

1. Fork the repository
2. Create your feature branch (`git checkout -b feature/amazing-feature`)
3. Commit your changes (`git commit -m 'Add some amazing feature'`)
4. Push to the branch (`git push origin feature/amazing-feature`)
5. Open a Pull Request

## 📄 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## 🙏 Acknowledgements

- [Perplexity AI](https://perplexity.ai) for their powerful AI models and API
- Contributors and early adopters

---

<p align="center">
  Made with ❤️ in San Francisco
</p>

<p align="center">
  <strong>Perplexity Core</strong> • Elevating AI Development
</p>
