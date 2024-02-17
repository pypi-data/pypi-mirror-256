<p align="center">
    <a href="https://github.com/fairnlp/incognito/releases">
        <img alt="GitHub release" src="https://img.shields.io/github/release/fairnlp/incognito.svg">
    </a>
</p>

# Description

Out-of-the-box anonymization.

# Installation

```bash
pip install incognito
```

# Usage

```python
from incognito import Incognito

incognito = Incognito()
incognito("John Doe is a data scientist at Google.")
# Output: "[PERSON] is a data scientist at [ORGANIZATION]."
```