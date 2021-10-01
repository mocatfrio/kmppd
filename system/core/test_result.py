import pandas as pd
import system.config.config as config
import application.helpers.constant as C
import application.helpers.io as io
from dotenv import load_dotenv

load_dotenv()


PARAM = config.get_scenario()

def generate():
    result = {
        'cardinality': cardinality(),
    }
    # waktu indexing

    io.export_excel(C.STORAGE_PATH, 'result.xlsx', result)


def cardinality():
    df1 = pd.DataFrame(['', '', '', 'Indexing time', 'Local processing time'])
    df2 = pd.DataFrame({
        'Number of data': PARAM['cardinality'],
        'Dimension': PARAM['const_dimension'],
        'Grid size': PARAM['const_grid_size'],
        'KMPPD': [1,2,3,4,5],
        'Optimized KMPPD': [1,2,3,4,5],
        'KMPPD': [1,2,3,4,5],
        'Optimized KMPPD': [1,2,3,4,5]
    })

    frames = [df1, df2]
    result = pd.concat(frames)
