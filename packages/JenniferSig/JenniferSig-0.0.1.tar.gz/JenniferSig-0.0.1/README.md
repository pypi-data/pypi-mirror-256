****
This method is created by Jennifer He in 02/08/2024
A good method to treat the outlier for the real world data
description: 
1. calculate the p value for each feature
2. check the outlier for each row based on the z-score
3. check the outlier in each row pairwise and make sure their p values are less than 0.05
4. delete the row with the situation in 3 if both of them have high p value.
****
