![lint workflow](https://github.com/mciccale/ScholarVista/actions/workflows/main.yml/badge.svg)
![zenodo](https://zenodo.org/badge/DOI/10.5281/zenodo.10654761.svg)

# ScholarVista

**ScholarVista** is a tool that extracts and plots information from a set of Academic Research Papers in PDF format. It utilizes [Grobid](https://github.com/kermitt2/grobid/), a library for extracting content from research papers, to extract all the relevant data. The extracted data is then plotted and displayed using Python.

## Table of Contents:

- **[Requirements](#requirements)**
- **[Install ScholarVista](#install-scholarvista)**
- **[Using ScholarVista](#using-scholarvista)**
- **[Execution Instructions](#execution-instructions)**
- **[Running Example](#running-example)**
- **[Where to Get Help](#where-to-get-help)**

## Requirements

You will need the **Grobid Service** to be installed and running in your machine. See Grobid Installation Instrucions [here](https://grobid.readthedocs.io/en/latest/Run-Grobid/).

## Install ScholarVista

### PIP

```bash
$ pip install scholarvista
```

When using **_pip_** it is a good practice to use virtual environments. Check out the official documentation on virtual envornments [here](https://docs.python.org/3/library/venv.html).

## Using ScholarVista

### CLI Tool

The most convenient way of using **ScholarVista** is by using its CLI.

The CLI Tool will generate a **keyword cloud** and a **list of URLs** for each PDF analyzed, together with a **histogram** comparing the numer of figures of each PDF.

```
Usage: scholarvista [OPTIONS]

  Process all PDFs in the given directory and display or save the results.

Options:
  --pdf-dir PATH      Directory containing PDF files.  [required]
  --save / --no-save  Save results to a file. Default is to display results
                      without saving.
  --output-dir PATH   Directory to save results. Defaults to current directory
                      if the --save flag is provided.
  --help              Show this message and exit.
```

### Python Modules

See `example.py`

## Execution Instructions

Make sure the **Grobid Service** is up and running. See [requirements](#requirements).

Once it has started, you can execute **ScholarVista CLI** from your shell like this:

```bash
# Save it to a specified directory
$ scholarvista --pdf-dir ./my_pdfs --save --output-dir ./output
```

```bash
# Display the results without saving them
$ scholarvista --pdf-dir ./my_pdfs
```

## License

Please refer to the `LICENSE` file.

## Where to Get Help

For further assistance or to contribute to the project, please refer to the `CONTRIBUTING.md` file.
