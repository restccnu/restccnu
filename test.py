from pip._vendor.requests.packages import urllib3
from requests.packages import urllib3 as _urllib3

r = urllib3.Retry(total=10)
if isinstance(r, _urllib3.Retry):
    print('The patch fixed this')
else:
    print("The patch didn't fix this")
