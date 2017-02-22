
# Description

This is a short python utility for exporting variables to certain frames. It
was designed to do the same as `from module import *` for variables.

### Usage

``` python
from exporter import Export
export = Export()

# export to the top frame the variable 'a' with a value of 123.
export.top().val('a',123)

# export to the calling function the variable names and corresponding values.
export.calling().val({'a':123, 'b':321})
```






