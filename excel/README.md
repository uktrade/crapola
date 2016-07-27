# Convert Excel HTML files to CSV

Python 3 required.

Install.

Activate venv:

    . venv/bin/activate

Create a report in Microsoft Dynamics and click "Export to Excel". Grab the
file created that ends in ``.xls`` but has headers that look like:

    <html xmlns:v="urn:schemas-microsoft-com:vml" xmlns:o="urn:schemas-microsoft-com:office:office" xmlns:x="urn:schemas-microsoft-com:office:excel" xmlns="http://www.w3.org/TR/REC-html40"><head><meta http-equiv=Content-Type content="text/html; charset=windows-1252"><meta name=ProgId content=Excel.Sheet><style type="text/css">
            <!--table

Use Python to convert the file:

    python excel/process.py [file downloaded] > [csv filename]

The file at location ``csv filename`` should now contain a CSV version of the
data exported from Dynamics.

Running the test suite requires py.test
