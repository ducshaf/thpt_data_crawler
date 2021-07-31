import pandas as pd
import numpy as np
import matplotlib.pyplot as plt


def plot(x):
    if type(x) is list:
        for i in x:
            plt.plot(i, label=i.index.name)
        plt.xticks(np.arange(0, 30.25, 0.25))
    else:
        plt.plot(x, label=x.index.name)
        plt.xticks(x.index)
    plt.legend()
    plt.show()


def diem_theo_mon(df):
    # Phổ điểm theo môn
    van = df.groupby(['Van'])['SBD'].nunique()
    toan = df.groupby(['Toan'])['SBD'].nunique()
    dia = df.groupby(['Dia'])['SBD'].nunique()
    gdcd = df.groupby(['GDCD'])['SBD'].nunique()
    hoa = df.groupby(['Hoa'])['SBD'].unique()
    li = df.groupby(['Ly'])['SBD'].nunique()
    sinh = df.groupby(['Sinh'])['SBD'].nunique()
    su = df.groupby(['Su'])['SBD'].nunique()
    anh = df.groupby(['Anh'])['SBD'].nunique()
    van_normalize = van.groupby(np.rint(van.index*4)/4).sum()

    return van, toan, dia, gdcd, hoa, li, sinh, su, anh, van_normalize


def diem_theo_to_hop(df):
    # Phổ điểm theo tổ hợp môn
    df['A00'] = round(df['Toan'] + df['Ly'] + df['Hoa'], 2)
    df['A01'] = round(df['Toan'] + df['Ly'] + df['Anh'], 2)
    df['A02'] = round(df['Toan'] + df['Ly'] + df['Sinh'], 2)
    df['B00'] = round(df['Toan'] + df['Ly'] + df['Dia'], 2)
    df['C00'] = round(df['Van'] + df['Su'] + df['Dia'], 2)
    df['C01'] = round(df['Van'] + df['Toan'] + df['Ly'], 2)
    df['C02'] = round(df['Van'] + df['Toan'] + df['Hoa'], 2)
    df['C04'] = round(df['Toan'] + df['Van'] + df['Dia'], 2)
    df['C19'] = round(df['Van'] + df['Su'] + df['GDCD'], 2)
    df['C20'] = round(df['Van'] + df['GDCD'] + df['Dia'], 2)
    df['D01-6'] = round(df['Van'] + df['Toan'] + df['Anh'], 2)
    df['D07'] = round(df['Toan'] + df['Hoa'] + df['Anh'], 2)
    df['D14'] = round(df['Van'] + df['Su'] + df['Anh'], 2)
    df['D15'] = round(df['Van'] + df['Anh'] + df['Dia'], 2)

    A00 = df.groupby(['A00'])['SBD'].nunique()
    A01 = df.groupby(['A01'])['SBD'].nunique()
    A02 = df.groupby(['A02'])['SBD'].nunique()
    B00 = df.groupby(['B00'])['SBD'].nunique()
    C00 = df.groupby(['C00'])['SBD'].nunique()
    C01 = df.groupby(['C01'])['SBD'].nunique()
    C02 = df.groupby(['C02'])['SBD'].nunique()
    C04 = df.groupby(['C04'])['SBD'].nunique()
    C19 = df.groupby(['C19'])['SBD'].nunique()
    C20 = df.groupby(['C20'])['SBD'].nunique()
    D01_6 = df.groupby(['D01-6'])['SBD'].nunique()
    D07 = df.groupby(['D07'])['SBD'].nunique()
    D14 = df.groupby(['D14'])['SBD'].nunique()
    D15 = df.groupby(['D15'])['SBD'].nunique()

    return A00, A01, A02, B00, C00, C01, C02, C04, C19, C20, D01_6, D07, D14, D15


def cdf(x):
    # Tính hàm phân phối tích lũy
    cdf = x.cumsum()
    return cdf


d21 = pd.read_csv('diem2021.csv')
d20 = pd.read_csv('diem2020.csv')

print(d21)
van, toan, dia, gdcd, hoa, li, sinh, su, anh, van_normalize = diem_theo_mon(d21)
A00, A01, A02, B00, C00, C01, C02, C04, C19, C20, D01_6, D07, D14, D15 = diem_theo_to_hop(d21)
A00_, A01_, A02_, B00_, C00_, C01_, C02_, C04_, C19_, C20_, D01_6_, D07_, D14_, D15_ = diem_theo_to_hop(d20)

d21['A'] = round((d21['Toan']*2 + d21['Anh']*2 + d21['Ly'])*3/5, 2)
d21['B'] = round((d21['Toan']*2 + d21['Ly']*2 + d21['Hoa'])*3/5, 2)
d21['2021'] = pd.DataFrame(np.where(d21['A'] > d21['B'], d21['A'], d21['B']))
cn8_21 = d21.groupby(['2021'])['SBD'].nunique()

d20['A'] = round((d20['Toan']*2 + d20['Anh']*2 + d20['Ly'])*3/5, 2)
d20['B'] = round((d20['Toan']*2 + d20['Ly']*2 + d20['Hoa'])*3/5, 2)
d20['2020'] = pd.DataFrame(np.where(d20['A'] > d20['B'], d20['A'], d20['B']))
cn8_20 = d20.groupby(['2020'])['SBD'].nunique()

cdf1 = cdf(cn8_21)
cdf2 = cdf(cn8_20)

# plot([cdf1, cdf2])
print(cn8_21.sum())
for i in cdf1.items():
    print(i)
# print((cn8_21.sum()))

# result_index = cdf1.sub(cdf2[27]).abs().sort_values()
# print(cdf1[result_index.idxmin()])
# print(result_index)