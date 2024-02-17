# YAML-D

**YAMLd** is a tiny subset of *YAML* focuses on representing tabular data similar to *CSV*. The D stands for data!

It is still under development, use it with caution. It is mainly used for reading *Pandas* dataframes, but it comes with extra command line tools.

## Convert CSV to YAMLd and vice versa:
```console
csv2yamld <your-csv-file>
```

```console
yamld2csv <your-yamld-file>
```

For more details use `csv2yamld -h` or `yamld2csv -h`.

## Open CSV files with VIM/NVIM
Reading *CSV* can be annoying, here is a simple solution:

```console
csv2yamld <your-csv-file> --stdout | nvim -c 'set filetype=yaml' -
```

Of course you can save it and convert it back to *CSV* using `yamld2csv`.


## Setup
```console 
pip install -U yamld
```

To use the scripts virtual environments, you can use *pipx*. Another option is to pass `--break-system-packages` to pip, but it's not advisable.
