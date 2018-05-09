import pandas as pd
import consolidateFiles as cf
import datacleaning as cl


def get_interval_data(frags, path):
    for i, f in enumerate(frags):
        if i % 1000 == 0:
            print (i, '/', len(frags))
        f['rr'] = cf.beats_in_fragment(f, path)
    return frags

def gen_fragments_dataset(sessions, duration, crop, path, mindata=0.83, maxpower=7500):
    
    # define fragments
    frags = cf.fragment_sessions(sessions, duration, crop)

    # retrieve RR data
    frags = get_interval_data(frags, path)
    
    # [cleaning] remove RR artifacts
    df = pd.DataFrame(frags)
    df['rr'] = df['rr'].apply(cl.clean_rr_series)
    df['beatcount'] = df['rr'].apply(len)

    # [cleaning] remove fragments with too few beats
    dfc = df[df['beatcount'] > mindata * duration]

    # aggregate in features TODO do this without converting to dic
    dic = dfc.to_dict(orient='records')
    for i in dic:
        i.update(cf.features_from_dic(i['rr']))
    dfc = pd.DataFrame(dic)
    
    # [cleaning] remove HF outliers possibly caused by gaps in sequences
    dfc = dfc[(dfc['hf'] < maxpower) & (dfc['hf'] < maxpower)]

    print(len(df), 'total frags and', len(dfc), 'kept')

    return dfc.drop(['rr'], axis = 1)

