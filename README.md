# How to use

- Install python requirements.
    ```sh
    python3 -m pip install -r requirements.txt
    ```
- Install MCL VSCode Extension.
- Run language server

    ```sh
    python3 -m mclc serve
    ```
- Generate C code and build `.elf` file.

    ```sh
    python3 -m mclc build-elf
    ```

- Upload `.elf` file and debug.

    ```sh
    python3 -m mclc debug
    ```

# Internals

- Lexer is defined in `mclc/Atributaries/modules/lexcial_analyser.py`
- Grammar is defined in `mclc/Atributaries/modules/grammar.py`

# Dependencies

## Used with modifications

- [Github: dabeaz/ply](https://github.com/dabeaz/ply)
- [Github: pyocd/pyOCD](https://github.com/pyocd/pyOCD)

## Used as libraries

- [Github: pallets/flask](https://github.com/pallets/flask)
- [Github: pyusb/pyusb](https://github.com/pyusb/pyusb)
- [Github: pyocd/pyOCD](https://github.com/pyocd/pyOCD)