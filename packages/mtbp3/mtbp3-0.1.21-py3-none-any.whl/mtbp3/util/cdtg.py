#  Copyright (C) 2023 Y Hsu <yh202109@gmail.com>
#
#  This program is free software: you can redistribute it and/or modify
#  it under the terms of the GNU General Public license as published by
#  the Free software Foundation, either version 3 of the License, or
#  any later version.
#
#  This program is distributed in the hope that it will be useful,
#  but WITHOUT ANY WARRANTY; without even the implied warranty of
#  MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the
#  GNU General Public License for more details
#
#  You should have received a copy of the GNU General Public license
#  along with this program. If not, see <https://www.gnu.org/license/>

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns

class catPlotter:
    """
    A class for creating categorical box plots and strip plots.

    Parameters:
    - df (pandas.DataFrame): The input DataFrame.
    - group_col (str): The column name for grouping the data.
    - y_col (str): The column name for the y-axis variable.
    - grid_col (str, optional): The column name for creating subplots based on a grid. Default is None.
    - grid_wrap (int, optional): The number of columns in the grid. Default is None.
    - pt_size (int, optional): The size of the points in the strip plot. Default is 5.
    - x_scale_base (int, optional): The base for the x-axis scale. Default is 10.
    - title (str, optional): The title of the plot. Default is an empty string.
    - fig_size_0 (int, optional): The width of the figure. Default is 7.
    - fig_size_1 (int, optional): The height of the figure. Default is 6.
    - grid_kws (dict, optional): Additional keyword arguments for the FacetGrid. Default is None.
    """

    def __init__(self, df, group_col, y_col, grid_col=None, grid_wrap=None, pt_size=5, x_scale_base=10, title="", fig_size_0=7, fig_size_1=6, grid_kws=None):
        if df is None:
            df = self.generate_example_dataset()
        self.df = df
        self.group_col = group_col
        self.y_col = y_col
        self.grid_col = grid_col
        self.grid_wrap = grid_wrap
        self.pt_size = pt_size
        self.x_scale_base = x_scale_base
        self.title = title
        self.fig_size_0 = fig_size_0
        self.fig_size_1 = fig_size_1
        self.grid_kws = grid_kws

    def boxplot(self):
        """
        Create a categorical box plot and strip plot.

        Raises:
        - ValueError: If group_col or y_col is not found in DataFrame columns.
        """
        if self.group_col not in self.df.columns or self.y_col not in self.df.columns:
            raise ValueError("group_col or y_col not found in DataFrame columns")

        if self.grid_kws is None:
            self.grid_kws = {}

        df = self.df.sort_values(self.group_col).reset_index()
        sns.set_style("ticks", {'axes.grid': True})

        if not self.grid_col or not self.grid_col in df.columns:
            self.grid_col = ""

        if self.grid_col:
            if not self.grid_wrap:
                self.grid_wrap = 1

            g = sns.FacetGrid(df, col=self.grid_col, col_wrap=self.grid_wrap, height=self.grid_kws.get('height', 2.5), aspect=self.grid_kws.get('aspect', 3), sharex=True, sharey=False, legend_out=True)
            group_order = sorted(df[self.group_col].unique())
            g.map(sns.boxplot, self.y_col, self.group_col, order=group_order, whis=[0, 100], width=0.4, palette=sns.light_palette("#79C", n_colors=len(group_order)), hue_order=group_order)
            g.map(sns.stripplot, self.y_col, self.group_col, order=group_order, size=self.pt_size, color=".3", alpha=0.5, jitter=0.2, palette=sns.dark_palette("#69d", reverse=True, n_colors=len(group_order)), hue_order=group_order)
            g.set_titles("{col_name}")
            g.set(xlabel=None, xticklabels=[])
            g.despine(trim=False, left=False)

            if self.x_scale_base > 0:
                plt.xscale("log", base=self.x_scale_base)

            for ax in g.axes.flat:
                tmp = ax.get_xlim()
                font_size = int(ax.xaxis.label.get_fontsize() * 0.9)
                subset_df = df[df[self.grid_col] == ax.get_title()]
                group_counts = subset_df.groupby(self.group_col, dropna=True).size()
                geometric_means = subset_df.groupby(self.group_col)[self.y_col].apply(lambda x: np.exp(np.mean(np.log(x))))
                nan_percentage = subset_df.groupby(self.group_col)[self.y_col].apply(lambda x: x.isna().mean() * 100)
                combined_data = pd.concat([group_counts, geometric_means, nan_percentage], axis=1)
                combined_data.columns = ['Group_Count', 'Geometric_Mean', 'Nan_Percentage']
                combined_data.reset_index(inplace=True)
                for i in list(range(0, len(group_order))):
                    if group_order[i] in group_counts.index:
                        count = group_counts[group_order[i]]
                        mean = geometric_means[group_order[i]]
                        nanperct = nan_percentage[group_order[i]]
                        ax.text(tmp[1], i, f'N={count}; %m={nanperct:.1f}\n♦GM={mean:.2f}', va='center', ha='left', fontsize=font_size)
                        ax.plot(mean, i, marker='D', markersize=max(int(font_size*.6),1), color="#248")

            plt.suptitle(self.title, weight='bold')
            plt.tight_layout()

        else:
            f, ax = plt.subplots(figsize=(self.fig_size_0, self.fig_size_1))
            sns.boxplot(df, x=self.y_col, y=self.group_col, hue=self.group_col, whis=[0, 100], width=.6, palette='dark:.3')
            sns.stripplot(df, x=self.y_col, y=self.group_col, size=self.pt_size, color=".3", alpha=0.3)

            if self.x_scale_base > 0:
                plt.xscale("log", base=self.x_scale_base)

            group_counts = df.groupby(self.group_col, dropna=True).size()
            geometric_means = df.groupby(self.group_col)[self.y_col].apply(lambda x: np.exp(np.mean(np.log(x))))
            nan_percentage = df.groupby(self.group_col)[self.y_col].apply(lambda x: x.isna().mean() * 100)
            combined_data = pd.concat([group_counts, geometric_means, nan_percentage], axis=1)
            combined_data.columns = ['Group_Count', 'Geometric_Mean', 'Nan_Percentage']
            combined_data.reset_index(inplace=True)
            for i in range(len(combined_data)):
                mean = combined_data['Geometric_Mean'][i]
                count = combined_data['Group_Count'][i]
                group = combined_data[self.group_col][i]
                pctnan = combined_data['Nan_Percentage'][i]
                ax.text(ax.get_xlim()[1], i, f'N: {count}\nGM: {mean:.2f}\nNaN: {pctnan:.2f}%', va='center', ha='left')

            plt.tight_layout()
            ax.set_title(self.title)
            ax.xaxis.grid(True)
            ax.set(ylabel="")
            sns.despine(trim=False, left=True)

    @staticmethod
    def generate_example_dataset():
        """
        Generate an example dataset.

        Returns:
            pandas.DataFrame: The example dataset.
        """
        grid = np.random.choice(['G1', 'G2'], size=100)
        group = np.random.choice(['A', 'B', 'C','D','E'], size=100)

        value = np.random.normal(0, 1, size=100)
        df = pd.DataFrame({'Group': group, 'Value': value, 'Grid': grid})
        df.loc[df['Group'] == 'B', 'Value'] += 2
        df.loc[df['Group'] == 'C', 'Value'] += 3

        df['Value'] = np.exp(np.abs(df['Value'])+2)
        return df

if __name__ == "__main__": 
    #cat_plot = catPlotter(None, 'Group', 'Value', grid_col='Grid', x_scale_base=5, title='My Title')
    #cat_plot.boxplot()
    #plt.show()
    pass

