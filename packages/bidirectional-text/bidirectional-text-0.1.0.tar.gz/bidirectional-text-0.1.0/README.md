# bidirectional-text

A streamlit component that allows you to get input from a textbox after every key press

## Installation instructions 

```sh
pip install bidirectional-text
```

## Usage instructions

```python
import streamlit as st

from st_bidirectional_text import st_bidirectional_text

value = st_bidirectional_text()

st.write(value)
