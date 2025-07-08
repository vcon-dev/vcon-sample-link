# vcon-sample-link

A sample external vcon link that adds custom attachments to vcon objects.

## About vcon-server

This package demonstrates how to create external links for the [vcon-server](https://github.com/vcon-dev/vcon-server) - a comprehensive conversation processing platform that:

- **Processes Conversations**: Handles audio, video, and text conversations with advanced AI analysis
- **Flexible Pipelines**: Supports configurable processing chains with built-in and external links
- **Storage Adapters**: Multiple storage backends (Redis, PostgreSQL, S3, etc.)
- **AI Integration**: Built-in support for transcription, analysis, and labeling services
- **Extensible**: Supports external links like this one for custom processing

This sample link demonstrates the extensibility pattern for adding custom functionality to vcon-server deployments.

## Usage

```python
from vcon_sample_link import run

# Add default attachment {"foo": "bar"}
result = run("vcon-uuid", "sample_link")

# Add custom data
result = run("vcon-uuid", "sample_link", {
    "custom_data": {"hello": "world"},
    "attachment_type": "custom_data"
})
```

## Installation

### From PyPI (for public links)

```bash
pip install vcon-sample-link
```

### From Repository (for private/custom links)

```bash
# Install directly from GitHub repository
pip install git+https://github.com/vcon-dev/vcon-sample-link.git

# Install from a specific branch
pip install git+https://github.com/vcon-dev/vcon-sample-link.git@main

# Install from a specific tag/version
pip install git+https://github.com/vcon-dev/vcon-sample-link.git@v0.1.0

# Install from a private repository (requires authentication)
pip install git+https://github.com/vcon-dev/private-vcon-link.git

# Install in development mode from local clone
git clone https://github.com/vcon-dev/vcon-sample-link.git
cd vcon-sample-link
pip install -e .
```

## Development & Deployment

### Publishing to PyPI

This project uses GitHub Actions for automatic deployment to PyPI.

#### Setup:

1. **Get PyPI API Token**:
   - Go to [PyPI Account Settings](https://pypi.org/manage/account/)
   - Generate an API token with "Entire account" scope

2. **Add GitHub Secret**:
   - Go to your GitHub repository → Settings → Secrets and variables → Actions
   - Add a new secret named `PYPI_TOKEN` with your PyPI API token

3. **Create Release**:
   ```bash
   # Tag and push a version
   git tag v0.1.0
   git push origin v0.1.0
   
   # Or create a GitHub release
   # The workflow will automatically build and publish to PyPI
   ```

#### Manual Publishing:

```bash
# Build and publish manually
poetry build
poetry publish
```

## Integration with vcon-server

### 1. Install the package in your conserver environment

```bash
# From PyPI (for public links)
pip install vcon-sample-link

# From repository (for private/custom links)
pip install git+https://github.com/vcon-dev/vcon-sample-link.git

# For private repositories with authentication
pip install git+https://github.com/vcon-dev/private-vcon-link.git
```

### 2. Use in processing chains

You can use this external link in your conserver chains by importing and calling it:

```python
# In your chain configuration
from vcon_sample_link import run as sample_link_run

def my_processing_chain(vcon_uuid):
    # ... other processing steps ...
    
    # Add sample data attachment
    vcon_uuid = sample_link_run(
        vcon_uuid=vcon_uuid,
        link_name="sample_attachment",
        opts={
            "custom_data": {"source": "external_link"},
            "attachment_type": "sample_data"
        }
    )
    
    # ... continue with other processing steps ...
    return vcon_uuid
```

### 3. Configuration in chain definitions

Add to your chain configuration file:

```yaml
chains:
  my_chain:
    steps:
      - name: "transcribe"
        link: "deepgram_link"
        options:
          api_key: "${DEEPGRAM_API_KEY}"
      
      - name: "add_sample_data"
        link: "vcon_sample_link"  # External link
        options:
          custom_data:
            processed_by: "my_chain"
            version: "1.0"
          attachment_type: "processing_metadata"
      
      - name: "analyze"
        link: "analyze_and_label"
        options:
          OPENAI_API_KEY: "${OPENAI_API_KEY}"
```

### 4. Dynamic import in chain runner

For dynamic loading of external links:

```python
import importlib

def load_external_link(link_name):
    """Dynamically load external link"""
    try:
        module = importlib.import_module(link_name)
        return getattr(module, 'run')
    except ImportError:
        raise Exception(f"External link {link_name} not found")

# Usage in chain processor
def process_chain_step(vcon_uuid, step_config):
    link_name = step_config['link']
    
    if link_name.startswith('vcon_'):  # External link
        link_func = load_external_link(link_name)
    else:  # Built-in link
        link_func = load_builtin_link(link_name)
    
         return link_func(vcon_uuid, step_config['name'], step_config.get('options', {}))
```

## Creating Private/Custom Links

This sample serves as a template for creating your own private vcon links:

### 1. Fork or Clone This Repository

```bash
# Create your own repository based on this template
git clone https://github.com/vcon-dev/vcon-sample-link.git my-custom-link
cd my-custom-link

# Update package name in pyproject.toml
# Update the package directory name from vcon_sample_link to your_custom_link
```

### 2. Customize Your Link

```python
# In your_custom_link/custom_link.py
def run(vcon_uuid, link_name, opts=default_options):
    """Your custom vcon processing logic"""
    vcon_redis = VconRedis()
    vcon = vcon_redis.get_vcon(vcon_uuid)
    
    # Add your custom processing here
    # Example: sentiment analysis, custom tagging, external API calls, etc.
    
    vcon.add_attachment(
        body=your_custom_data,
        type="your_custom_type",
        encoding="none"
    )
    
    vcon_redis.store_vcon(vcon)
    return vcon_uuid
```

### 3. Install Your Private Link

```bash
# Install directly from your private repository
pip install git+https://github.com/vcon-dev/my-custom-link.git

# Use in your vcon-server chains
from my_custom_link import run as my_custom_run
```

### 4. Benefits of Private Links

- **Proprietary Logic**: Keep your custom processing logic private
- **Internal APIs**: Integrate with internal systems without exposing credentials
- **Custom Models**: Use proprietary AI models or algorithms
- **Compliance**: Meet specific regulatory or security requirements
- **No PyPI Dependency**: Install directly from your private repositories 