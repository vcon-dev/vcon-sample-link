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

This external link is designed to be used within vcon-server for custom vCon processing. It automatically adds custom attachments to vCons as they flow through processing chains.

When configured in a vcon-server chain, this link will:
- Receive vCons from the processing pipeline
- Add custom attachment data based on configuration
- Return the processed vCon to continue the chain

The link processes vCons automatically - no direct function calls needed in production.

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

### 2. Testing Your Link

For development and testing, you can call the link function directly:

```python
# For testing/debugging only
from vcon_sample_link import run as sample_link_run

result = sample_link_run(
    vcon_uuid="123e4567-e89b-12d3-a456-426614174000",
    link_name="sample_attachment",
    opts={
        "custom_data": {"source": "test"},
        "attachment_type": "sample_data"
    }
)
```

**Note**: In production, vcon-server automatically executes your link as part of processing chains. Direct function calls are only for testing.

### 3. Configuration in chain definitions

Add to your chain configuration file:

```yaml
links:
  # Your external vcon-sample-link
  sample_link:
    module: vcon_sample_link
    pip_name: vcon-sample-link  # Install from PyPI
    options:
      custom_data:
        processed_by: "my_chain"
        version: "1.0"
      attachment_type: "processing_metadata"
  
  # Example using GitHub repository
  sample_link_from_github:
    module: vcon_sample_link
    pip_name: git+https://github.com/vcon-dev/vcon-sample-link.git
    options:
      custom_data:
        source: "github_install"
      attachment_type: "sample_data"

chains:
  my_chain:
    links:
      - sample_link
    ingress_lists:
      - main_ingress
    storages:
      - redis_storage
    enabled: 1
```

### 4. Advanced Configuration Options

#### Version Management

You can specify exact versions for your external links:

```yaml
links:
  sample_link_pinned:
    module: vcon_sample_link
    pip_name: vcon-sample-link==1.2.3  # Exact version
    options:
      custom_data: {"version": "pinned"}
  
  sample_link_flexible:
    module: vcon_sample_link
    pip_name: vcon-sample-link>=1.0.0,<2.0.0  # Version range
    options:
      custom_data: {"version": "flexible"}
  
  # Install from specific Git tag
  sample_link_git_tag:
    module: vcon_sample_link
    pip_name: git+https://github.com/vcon-dev/vcon-sample-link.git@v1.2.3
    options:
      custom_data: {"source": "git_tag"}
```

#### Dynamic Imports for Global Modules

For modules that need to be available globally (not just as links):

```yaml
imports:
  # External utility module
  custom_utility:
    module: my_custom_utils
    pip_name: custom-utils-package
  
  # GitHub repository
  github_helper:
    module: github_helper
    pip_name: git+https://github.com/username/helper-repo.git
  
  # Module name matches pip package name
  requests_import:
    module: requests
    # pip_name not needed since it matches module name
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
# In your_custom_link/link.py (note: must be named 'link.py')
from server.lib.vcon_redis import VconRedis
from server.lib.logging_utils import init_logger

logger = init_logger(__name__)

default_options = {
    "custom_data": {"processed_by": "my_custom_link"},
    "attachment_type": "custom_analysis",
}

def run(vcon_uuid, link_name, opts=None):
    """Your custom vcon processing logic"""
    logger.debug("Starting %s", link_name)
    
    if opts is None:
        opts = default_options
    
    vcon_redis = VconRedis()
    vcon = vcon_redis.get_vcon(vcon_uuid)
    
    # Add your custom processing here
    # Example: sentiment analysis, custom tagging, external API calls, etc.
    custom_analysis = {
        "sentiment": "positive",
        "keywords": ["customer", "service", "satisfaction"],
        "confidence": 0.85
    }
    
    vcon.add_attachment(
        body=custom_analysis,
        type=opts.get("attachment_type", "custom_analysis"),
        encoding="none"
    )
    
    vcon_redis.store_vcon(vcon)
    
    # Return vcon_uuid to continue chain processing
    # Return None to halt chain processing
    return vcon_uuid
```

### 3. Install Your Private Link

```bash
# Install directly from your private repository
pip install git+https://github.com/vcon-dev/my-custom-link.git
```

Configure in your vcon-server chain:

```yaml
links:
  my_custom_processing:
    module: my_custom_link
    pip_name: git+https://github.com/vcon-dev/my-custom-link.git
    options:
      custom_data:
        api_key: "your-api-key"
        model: "custom-model-v1"
      attachment_type: "custom_analysis"

chains:
  custom_processing_chain:
    links:
      - transcribe  # Built-in link
      - my_custom_processing  # Your custom link
      - webhook  # Built-in link
    ingress_lists:
      - custom_ingress
    storages:
      - redis_storage
    enabled: 1
```

### 4. Benefits of Private Links

- **Proprietary Logic**: Keep your custom processing logic private
- **Internal APIs**: Integrate with internal systems without exposing credentials
- **Custom Models**: Use proprietary AI models or algorithms
- **Compliance**: Meet specific regulatory or security requirements
- **No PyPI Dependency**: Install directly from your private repositories

## Key Implementation Notes

### Required Function Signature

Your link must implement this function:

```python
def run(vcon_uuid: str, link_name: str, opts: dict = None) -> str | None:
    """Process a vCon and return vcon_uuid to continue or None to stop"""
```

### Dependencies

External links run within the vcon-server environment and automatically have access to:
- `server.lib.vcon_redis.VconRedis` - for vCon storage/retrieval
- `server.lib.logging_utils.init_logger` - for logging

Only add dependencies in `pyproject.toml` that are specific to your link's functionality.