# Toolbox to create phonondb web site

## How to create sphinx document

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

1. cd ph20180417
2. Run create_sphinx_files.sh.
   - Directories from d000 to d999 are created.
   - make_rst.py is executed in each dxxx directory.
3. Run make_index.zsh to update index.rst
4. Put necessary data, .lzma, .png, POSCAR.yaml, etc, in each directory by using move_phonn.sh.
5. cd ..
5. Run run_sphinx.sh.
