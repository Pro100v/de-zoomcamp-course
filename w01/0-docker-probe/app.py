import sys

import pandas as pd

print(f"Pandas version: {pd.__version__}")
print(f"App args: {sys.argv}")

dt = sys.argv[1]

# do some think amazing

print(f"App complete successfully for date={dt}! ")
