# MZ-PDF_Linkgenerator

This script allows you to generate a legit link for download PDF documents from the "MZ ePaper" website.

## Prerequisites

To run this script, make sure you have the following dependencies installed:

- Python 3.x
- requests library

You can install the requests library using pip:

```
pip install requests
```

## Usage

1. Open the script file `main.py` in a editor of your choice.
2. Replace the placeholder values in the `user_data` list with your actual login credentials with the format [MAIL, PASSWD].
4. Choose the desired address from the `addresses` list by change the index (0 in this example)
```python
address_for_download = addresses[0][1])
```

The script will print the download link for the PDF document. You can copy and paste the link into your browser to download the document.

To save the Document you could implement something like:

```python
with open((str(down_name) + ".pdf"), "wb") as f:
   response = requests.get(final)
   f.write(response.content)
```


Feel free to modify the script according to your needs or incorporate it into your own projects.
