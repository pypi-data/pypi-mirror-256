from scipy.stats import stats
from scipy.stats import zscore
import pandas as pd
import numpy as np
class JenniferSig():
    '''
        This method is create by Jennifer He for outlier selection :)
    '''
    def __init__(self) -> None:
        self.author = "Jennifer He"
        self.dataset = None
    
    def __getitem__(self, position) -> list:
        assert position == list, "the position should be a 2 elements integer list"
        assert len(position) == 2, "the position should be a 2 elements integer list"
        assert isinstance(position[0], int), "the position should be a 2 elements integer list"
        assert isinstance(position[1], int), "the position should be a 2 elements integer list"
        ix, iy = position
        return self.dataset.iloc[ix, iy]
    
    def __getitem__(self, position, value) -> list:
        assert position == list, "the position should be a 2 elements integer list"
        assert len(position) == 2, "the position should be a 2 elements integer list"
        assert isinstance(position[0], int), "the position should be a 2 elements integer list"
        assert isinstance(position[1], int), "the position should be a 2 elements integer list"
        ix, iy = position
        assert type(value) == type(self.dataset.iloc[ix,iy])
        ix, iy = position
        return self.dataset.iloc[ix, iy]
    
    def __repr__(self):
        return 'JenniferSig()'
    
    def __len__(self):
        return len(self.dataset)
    
    def jennifersignificant(self, dataset) -> list:
        assert isinstance(dataset, pd.DataFrame), "the dataset should be pd.dataframe"
        
        try:
            dataset == dataset.select_dtypes(include=['number'])
        except ValueError as e:
            print("input numeric dataset please")

        self.dataset = dataset
        
        corr_significance = {}
        
        p_values_df = pd.DataFrame(data=np.zeros(shape=(dataset.shape[1], dataset.shape[1])),
                                columns=dataset.columns,
                                index=dataset.columns)

        for row in dataset.columns:
            for col in dataset.columns:
                if row != col:
                    _, p_value = stats.pearsonr(dataset[row], dataset[col])
                    p_values_df.at[row, col] = p_value
                    if p_value < 0.05:  # Assuming 0.05 significance level
                        corr_significance[(row, col)] = True
                else:
                    p_values_df.at[row, col] = np.nan
                    
        
        z_scores = dataset.apply(zscore)
        outliers = np.abs(z_scores) > 3


        rows_to_drop = set()
        for (col1, col2), significant in corr_significance.items():
            if significant:
                # Find rows where both columns are outliers
                outlier_rows = outliers[col1] & outliers[col2]
                rows_to_drop.update(outlier_rows[outlier_rows].index.tolist())
        
        return rows_to_drop
    
    def __eq__(self, other):
        assert isinstance(other, pd.DataFrame) , "the input should be a pd.dataframe"
        return self.dataset == other