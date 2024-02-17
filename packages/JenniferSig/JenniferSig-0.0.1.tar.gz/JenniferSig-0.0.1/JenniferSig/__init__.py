from .JenniferSig import *

__docformat__ = "restructuredtext"

__doc__ = '''
    This method is created by Jennifer He in 02/08/2024
    A good method to treat the outlier for the real world data
    description: 
    1. calculate the p value for each feature
    2. check the outlier for each row based on the z-score
    3. check the outlier in each row pairwise and make sure their p values are less than 0.05
    4. delete the row with the situation in 3 if both of them have high p value.
'''

# Let users know if they're missing any of our hard dependencies
_hard_dependencies = ("numpy", "scipy", "pandas")
_missing_dependencies = []
# Optionally, define some package-level data or perform initialization setup

__all__ = [
    "JenniferSig",
]

__version__ = '1.0.0'