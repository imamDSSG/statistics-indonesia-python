import urllib
import os
import pandas as pd


def download_if_needed(URL, filename):
    """
    Download from URL to filename unless filename already exists
    """
    if os.path.exists(filename):
        print(filename, 'already exists')
        return
    else:
        print('downloading', filename)
        urllib.urlretrieve(URL, filename)


def get_education_data():
    """
    Download BPS education data, unless already downloaded
    """
    download_if_needed('http://data.go.id/dataset/58490386-5c56-410f-bdcc-57' +
                       'bf0d3cc35c/resource/2aa6278c-09c7-446e-bb37-67553870' +
                       '5163/download/processedjumlahpenduduktingkatpendidik' +
                       'anjeniskelaminkabupatensensus2010.csv',
                       'indonesia_education-country.csv')


def get_Istat_data():
    """
    Download Istat Household Budget Survey, unless already downloaded
    """
    download_if_needed('http://www.istat.it/en/files/2016/02/ISTAT_MFR_' +
                       'HBS_2014_IT1.zip',
                       'Istat_HBS_2014.zip')


def get_HBS_data():
    """
    Fetch pronto data (if needed) and extract trips as dataframe
    """
    get_Istat_data()
    zf = zipfile.ZipFile('Istat_HBS_2014.zip')
    file_handle = zf.open('FILENAME.csv')
    return pd.read_csv(file_handle)


def to_xml(df, filename=None, mode='w'):
    def row_to_xml(row):
        xml = ['<item>']
        for i, col_name in enumerate(row.index):
            xml.append('  <field name="{0}">{1}</field>'.format(col_name,
                                                                row.iloc[i]))
        xml.append('</item>')
        return '\n'.join(xml)
    res = '\n'.join(df.apply(row_to_xml, axis=1))

    if filename is None:
        return res
    with open(filename, mode) as f:
        f.write(res)

pd.DataFrame.to_xml = to_xml


# Convenience functions for working with color ramps and bars
def colorbar_index(ncolors, cmap, labels=None, **kwargs):
    """
    This is a convenience function to stop you making off-by-one errors
    Takes a standard colourmap, and discretizes it,
    then draws a colour bar with correctly aligned labels
    """
    cmap = cmap_discretize(cmap, ncolors)
    mappable = cm.ScalarMappable(cmap=cmap)
    mappable.set_array([])
    mappable.set_clim(-0.5, ncolors+0.5)
    colorbar = plt.colorbar(mappable, **kwargs)
    colorbar.set_ticks(np.linspace(0, ncolors, ncolors))
    colorbar.set_ticklabels(range(ncolors))
    if labels:
        colorbar.set_ticklabels(labels)
    return colorbar


def cmap_discretize(cmap, N):
    """
    Return a discrete colormap from the continuous colormap cmap.

        cmap: colormap instance, eg. cm.jet.
        N: number of colors.

    Example
        x = resize(arange(100), (5,100))
        djet = cmap_discretize(cm.jet, 5)
        imshow(x, cmap=djet)

    """
    if type(cmap) == str:
        cmap = get_cmap(cmap)
    colors_i = np.concatenate((np.linspace(0, 1., N), (0., 0., 0., 0.)))
    colors_rgba = cmap(colors_i)
    indices = np.linspace(0, 1., N + 1)
    cdict = {}
    for ki, key in enumerate(('red', 'green', 'blue')):
        cdict[key] = [(indices[i], colors_rgba[i - 1, ki],
                      colors_rgba[i, ki]) for i in xrange(N + 1)]

    return matplotlib.colors.LinearSegmentedColormap(cmap.name + "_%d" % N,
                                                     cdict, 1024)
