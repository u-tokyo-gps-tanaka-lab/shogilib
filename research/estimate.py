from decimal import Decimal, getcontext
from mpmath import mp

getcontext().prec = 100
mp.dps = 50

S_all = mp.mpf('80880932079767835177773204009328769812438521503800714936366945233084532')
s = mp.mpf('40491613')
n = mp.mpf('5000000000')

p_hat = s / n

sigma = mp.sqrt((p_hat * (1 - p_hat)) / n)
print(f'sigma = {sigma}')

expected_S_ok = p_hat * S_all
print(f'Expected |S_ok| calculated from the sample = {expected_S_ok}')

p_upper = p_hat + 3 * sigma
p_lower = p_hat - 3 * sigma
print(f'p_upper = {p_upper}\np_lower = {p_lower}')

S_ok_upper = p_upper * S_all
S_ok_lower = p_lower * S_all
print(f'{S_ok_lower} <= |S_ok| <= {S_ok_upper}')

error = S_all * 3 * sigma
print(f'Error = {error}')
