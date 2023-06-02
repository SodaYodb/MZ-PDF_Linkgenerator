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
2. Replace the placeholder values in the `user_data` list with your actual login credentials. Each element in the list represents a user with the format [ID, MAIL, PASSWD]. You can add multiple users by appending additional lists within the user_data list.
4. Choose the desired address from the `addresses` list by change the index (3 in this example)
   ```python
   adress_for_download = addresses[3][1])
   ```

The script will print the download link for the PDF document. You can copy and paste the link into your browser to download the document.

## License

This project is licensed under the [MIT License](LICENSE).
