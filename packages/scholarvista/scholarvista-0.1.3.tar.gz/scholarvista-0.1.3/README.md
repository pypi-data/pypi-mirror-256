[![PyPI version](https://badge.fury.io/py/scholarvista.svg)](https://pypi.org/project/scholarvista)
[![Documentation Status](https://readthedocs.org/projects/scholarvista/badge/?version=latest)](https://scholarvista.readthedocs.io/en/latest/?badge=latest)
[![zenodo](https://zenodo.org/badge/DOI/10.5281/zenodo.10654761.svg)](https://zenodo.org/doi/10.5281/zenodo.10654760)
![publish workflow](https://github.com/mciccale/ScholarVista/actions/workflows/publish.yml/badge.svg)
![test workflow](https://github.com/mciccale/ScholarVista/actions/workflows/test.yml/badge.svg)
![lint workflow](https://github.com/mciccale/ScholarVista/actions/workflows/lint.yml/badge.svg)

# ScholarVista

**ScholarVista** is a tool that extracts and plots information from a set of Academic Research Papers in PDF / TEI XML format. To process PDFs, it utilizes [Grobid](https://github.com/kermitt2/grobid/) to generate the TEI XML files, then **ScholarVista** extracts the relevant information from the TEI XML files and generates the following data:

1. **Keyword Cloud** for each of the paper's abstract and for the total of all abstracts.
2. **Links List** for each one of the links found in the paper.
3. **Figures Histogram** comparing the number of figures per paper.

## Table of Contents:

- **[Requirements](#requirements)**
- **[Install ScholarVista](#install-scholarvista)**
- **[Using ScholarVista](#using-scholarvista)**
- **[Execution Instructions](#execution-instructions)**
- **[Running Example](#running-example)**
- **[Where to Get Help](#where-to-get-help)**

## Requirements

If you want to generate the results from a set of PDF academic papers, you must ensure that the **Grobid Service** to be installed and running in your machine. See Grobid Installation Instrucions [here](https://grobid.readthedocs.io/en/latest/Run-Grobid/).

If you already have the TEI XML files generated, you can directly generate the information from them.

## Install ScholarVista

### PIP

```bash
$ pip install scholarvista
```

When using **_pip_** it is a good practice to use virtual environments. Check out the official documentation on virtual envornments [here](https://docs.python.org/3/library/venv.html).

## Using ScholarVista

### CLI Tool

The most convenient way of using **ScholarVista** is by using its CLI.

The CLI Tool will generate and save to a directory a **keyword cloud** and a **list of URLs** for each PDF analyzed, together with a **histogram** comparing the numer of figures of each PDF.

```
Usage: scholarvista [OPTIONS] COMMAND [ARGS]...

  ScholarVista's CLI main entry point.

Options:
  --input-dir PATH   Directory containing PDF files.  [required]
  --output-dir PATH  Directory to save results. Defaults to current directory.
  --help             Show this message and exit.

Commands:
  process-pdfs  Process all PDFs in the given directory.
  process-xmls  Process all TEI XMLs in the given directory.
```

### Python Modules

See `example.py`

## Execution Instructions

You can execute **ScholarVista CLI** from your shell like this:

```bash
# Process PDF files and save the results to a specified directory
$ scholarvista --input-dir ./pdfs --output-dir ./output process-pdfs
```

_Note: The `process-pdfs` command requires the Grobid Service to be up and running as described in [requirements](#requirements)._

```bash
# Process TEI XML files and save the results to the current directory
$ scholarvista --input-dir ./xmls process-xmls
```

## License

Please refer to the `LICENSE` file.

## Where to Get Help

For further assistance or to contribute to the project, please refer to the `CONTRIBUTING.md` file.
