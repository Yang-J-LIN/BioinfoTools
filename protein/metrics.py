import numpy as np
import pandas as pd


def top_L_precision(pred, truth, m=0, n=-1, ratio=1):
    assert pred.shape == truth.shape
    L = pred.shape[0]

    n = (L + n) % L

    width = n - m

    pred_contact_of_interest = []
    truth_contact_of_interest = []

    for i in range(width):
        pred_contact_of_interest.append(np.diag(pred, k=m+i))
        truth_contact_of_interest.append(np.diag(truth, k=m+i))
    
    pred_contact_of_interest = np.concatenate(pred_contact_of_interest)
    truth_contact_of_interest = np.concatenate(truth_contact_of_interest)

    df = pd.DataFrame({
        'pred': pred_contact_of_interest,
        'truth': truth_contact_of_interest
    })

    df = df.sort_values(by=['pred'], ascending=False)

    print(df)

    top_L = df['truth'].values[0:int(L / ratio)]

    print(top_L.sum())

    return top_L.sum(), int(L / ratio)




if __name__ == '__main__':
    x = np.arange(36).reshape((6,6))
    print(x)
    top_L_precision(x, x)
