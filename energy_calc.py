import math

def current_calc(kW, kU_l, cos_u=1, n_ph=3, show=1):
    I = kW / math.sqrt(3) / kU_l / cos_u
    if show:
        print(f'{I:.1f} А')
    return I

def tt_select(Pmax, Pmin, kU_l, K_tt, cos_u=1):
    Imax = current_calc(Pmax, kU_l, cos_u, show=0)
    Imin = current_calc(Pmin, kU_l, cos_u, show=0)
    print(f'Pmax={Pmax} кВт')
    print(f'Imax={Imax:.1f} А'.replace('.',','))
    print(f'K_tt={K_tt:.0f}'.replace('.',','))
    print(f'{Imax:.1f}/{K_tt:.0f}={Imax/K_tt:.1f}   {Imax/K_tt/5*100:.0f}%>40%'.replace('.',','))
    print(f'Pmin={Pmin} кВт')
    print(f'Imin={Imin:.1f} А'.replace('.',','))
    print(f'{Imin:.1f}/{K_tt:.0f}={Imin/K_tt:.2f}   {Imin/K_tt/5*100:.1f}%>5%'.replace('.',','))

def volt_loss(kW, kU_l, r, x, L, cos_u=1, n_ph=3):
    I = kW / math.sqrt(3) / kU_l / cos_u
    print(I)
    if n_ph==3:
        b = 1
    # dU = b * I * (r * L * cos_u + x * L * math.sin(math.acos(cos_u)))
    dU = kW * L * (r + x * math.tan(math.acos(cos_u))) / kU_l
    print(f'{dU:.1f} В')
    print(f'{dU * 100 / kU_l / 1000:.1f} %')