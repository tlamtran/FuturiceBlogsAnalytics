import numpy as np
import matplotlib.pyplot as plt
import pandas as pd
from matplotlib.widgets import RectangleSelector
from matplotlib.lines import Line2D
from ast import literal_eval
from sklearn.manifold import TSNE
from sklearn.decomposition import PCA

# --- Parameters:

feature = 'title'
#feature = 'teaser text'
#feature = 'full text'

stat = 'total users'
#stat = 'bounce rate'
#stat = 'average session duration'

#reducer = 'pca'
reducer = 'tsne'

# --- Data preprocessing:

df = pd.read_csv('data/processed/futurice/blogs2.csv')
df.dropna(inplace=True)

X = np.vstack(df['bge embedded ' + feature].apply(literal_eval).apply(np.array).values)
y = df[stat].values.reshape(-1, 1)

if reducer == 'pca':
    pca = PCA(n_components=2)
    offset = 0.02
    X = pca.fit_transform(X)
elif reducer == 'tsne':
    tsne = TSNE(n_components=2, perplexity=5, random_state=42, init='random', learning_rate=200)
    offset = 5
    X = tsne.fit_transform(X)


# --- Plotting:

q20 = np.percentile(y, 20)
q40 = np.percentile(y, 40)
q60 = np.percentile(y, 60)
q80 = np.percentile(y, 80)

colors = []
for value in y:
    if value <= q20:
        colors.append('red')  # 0-20%
    elif value <= q40:
        colors.append('darkorange')  # 20-40%
    elif value <= q60:
        colors.append('gold')  # 40-60%
    elif value <= q80:
        colors.append('turquoise')  # 60-80%
    else:
        colors.append('green')  # 80-100%

legend_elements = [Line2D([0], [0], marker='o', color='w', label='0-20%', markersize=5, markerfacecolor='red'),
                   Line2D([0], [0], marker='o', color='w', label='20-40%', markersize=5, markerfacecolor='darkorange'),
                   Line2D([0], [0], marker='o', color='w', label='40-60%', markersize=5, markerfacecolor='gold'),
                   Line2D([0], [0], marker='o', color='w', label='60-80%', markersize=5, markerfacecolor='turquoise'),
                   Line2D([0], [0], marker='o', color='w', label='80-100%', markersize=5, markerfacecolor='green')]

fig, ax = plt.subplots(figsize=(10,8))
ax.set_title(f'Ada embbeded {feature} reduced with {reducer}')
ax.set_xlim(X[:, 0].min() - offset, X[:, 0].max() + offset)
ax.set_ylim(X[:, 1].min() - offset, X[:, 1].max() + offset)

ax.scatter(X[:, 0], X[:, 1], c=colors, alpha=0.5)

selected_points, = ax.plot([], [], 'ko', markersize=6)

def line_select_callback(click, release):
    x1, y1 = click.xdata, click.ydata
    x2, y2 = release.xdata, release.ydata
    
    mask = (X[:, 0] > min(x1, x2)) & (X[:, 0] < max(x1, x2)) & (X[:, 1] > min(y1, y2)) & (X[:, 1] < max(y1, y2))
    selected_points.set_data(X[mask][:, 0], X[mask][:, 1])
    fig.canvas.draw()

    masked_df = df[mask]

    # https://www.clearpeaks.com/using-chatgpt-for-topic-modelling-and-analysis-of-customer-feedback/
    print(masked_df.loc[:, feature])

rs = RectangleSelector(ax, line_select_callback, button=[1], interactive=True, useblit=True)

plt.legend(handles=legend_elements, loc='upper left', title=stat, bbox_to_anchor=(1.05, 1))
plt.tight_layout()
plt.show()
