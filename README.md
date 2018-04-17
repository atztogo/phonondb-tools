# Toolbox to create phonondb web site

## How to create sphinx document

### Directory structure to create sphinx files

```
.
├── about.rst
├── citation.rst
├── conf.py
├── index.rst
├── make_index.zsh
├── move_phonon.sh
├── ph20151124
├── ph20180417
│   ├── d000
│   ├── d001
│   ├── ...
│   ├── d999
│   ├── index.rst
│   ├── create_sphinx_files.sh
│   ├── make_index.zsh
│   └── make_rst.py
├── run_sphinx.zsh
└── webserver.jpg
```

### Data should be stored in each directory of `phonon-run/mp-xxx`

```
% ls
band.png  dos.png  mp-5046-20180417.tar.lzma  POSCAR-unitcell.yaml  tprops.png
```

where `mp-5046-20180417.tar.lzma` contains the raw data.

### Steps

```
.
├── about.rst
├── citation.rst
├── conf.py
├── index.rst
├── ph20180417
│   ├── copy_png_lzam.sh
│   ├── create_sphinx_files.sh
│   ├── index.rst
│   ├── make_index.zsh
│   └── make_rst.py
├── run_sphinx.zsh
├── _templates
│   └── globaltoc.html
└── webserver.jpg
```

1. `cd ph20180417`
2. Run `create_sphinx_files.sh`.
   - Directories from `d000` to `d999` are created.
   - `make_rst.py` is executed in each `dxxx` directory to create
     `mp-xxx.rst` files
3. Run copy_png_lzma.sh
   - Copy necessary data in dxxx.
3. Run `make_index.zsh` to add links to each `mp-xxx.rst` to `index.rst`
4. `cd ..`
5. Run `sphinx-build -j 10 -b html . _build |& tee sphinx.log`
