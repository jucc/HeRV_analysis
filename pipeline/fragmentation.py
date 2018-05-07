import pandas as pd
import consolidateFiles as cf


def gen_fragments_dataset(sessions, duration, crop, path):
    
    # define fragments
    frags = cf.fragment_sessions(sessions, duration, crop)

    # retrieve RR data
    for f in frags:
        f['rr'] = cf.beats_in_fragment(f, path)
    
    # [cleaning] remove RR artifacts
    df = pd.DataFrame(frags)
    df['rr'] = df['rr'].apply(cl.clean_rr_series)
    df['beatcount'] = df['rr'].apply(len)

    # [cleaning] remove fragments with too few beats
    df = df[df['beatcount'] > 0.6 * duration]

    # aggregate in features TODO do this without converting to dic
    dic = df.to_dict(orient='records')
    for i in dic:
        i.update(cf.features_from_dic(i['rr']))
    df = pd.DataFrame(dic)
    
    # [cleaning] remove HF outliers possibly caused by gaps in sequences
    df = df[df['hf'] < 15000]

    return df.drop(['rr'], axis = 1)

