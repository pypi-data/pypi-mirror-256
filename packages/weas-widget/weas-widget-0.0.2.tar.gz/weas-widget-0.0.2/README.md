
# Welcome to WEAS Widget!
[![PyPI version](https://badge.fury.io/py/weas-widget.svg)](https://badge.fury.io/py/weas-widget)
[![Docs status](https://readthedocs.org/projects/weas-widget/badge)](http://weas-widget.readthedocs.io/)


A widget to visualize and edit with atomistic structures in Jupyter Notebook. It uses [WEAS](https://github.com/superstar54/weas) (Web Environment For Atomistic Structure) in the backend.

## Installation

```console
    pip install weas-widget
```

## Edit the structure with mouse and keyboard
WEAS supports editing the atoms directly in the GUI and synchronizing with the structure of the Python object.

### Select Atoms
There are two methods for selecting atoms:
- Pick Selection: Click directly on an atom to select it.
- Range Selection: Hold the `Shift` key and drag the right mouse button to select a group of atoms.



### Move, Rotate selected atoms

Press the transform shortcut, and move your mouse.

|Operation | Shortcut|
|----------|---------|
| Move     | `g`   |
| Rotate   | `r`   |


### Delete selected atoms
Press the ``Delete`` key to delete the selected atoms


### Export edited atoms
One can export the edited atoms to ASE or Pymatgen

## Example

### Load structure
One can load a structure from ASE or Pymatgen
```
from ase.build import molecule
from weas_widget import WeasWidget
atoms = molecule("C2H6SO")
viewer = WeasWidget()
viewer.from_ase(atoms)
viewer
```

<img src="docs/source/_static/images/example-c2h6so.png"  width="300px"/>



### Crystal view
For a nice visualization of a crystal, one usually shows the polyhedra and the atoms on the unit cell boundary, as well as the bonded atoms outside the cell.

<img src="docs/source/_static/images/example-tio2.png"  width="300px"/>

### How to use

Please vist: https://weas-widget.readthedocs.io/en/latest/index.html



## Contact
* Xing Wang  <xingwang1991@gmail.com>

## License
[MIT](http://opensource.org/licenses/MIT)
