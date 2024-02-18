# watch_import
Watch_import uses `watchfiles` to observe a file or folder. When a file is saved it will re/import that file into the watch_import context.


# Using as a file/folder watcher
```sh
> watch_import PATH/TO_PYTHON_FILES
```

# Using as an import
```python
from watch_import import watch_me

print('hello')
watch_me()
```

# Example use-case OCP CAD Viewer

```python
import cadquery as cq
from ocp_vscode import show
from watch_import import watch_me

body = cq.Workplane("XY").box(5, 10, 15)
show(body)

watch_me()
```

Run this file once and it will start watching and "re-run" once saved.