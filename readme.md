This is a simple exercise that consists of using various APIs, such as the ISS station API to track its position. Additionally, with the sunset and sunrise API, the program determines if it is currently night or not. If it is night, the code sends an email to users, prompting them to look up for the ISS. The relevant information about time and the ISS location at that moment is then written to a JSON file.

Whenever the code detects the position of the ISS within the specified field:

```python
import requests
import json
from datetime import datetime
import smtplib

# TO DO
# Add a graphical user interface that will allow users to insert their geo-location (longitude and altitude),
# the receiver email, and the sending one.