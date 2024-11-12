from math import sqrt
from rank import countsum

S_all = countsum
SAMPLE_ok = 40_491_613
SAMPLE_all = 5_000_000_000
print(f'|S_all| = {S_all}')
print(f'SAMPLE_ok = {SAMPLE_ok}')
print(f'SAMPLE_all = {SAMPLE_all}')

print('==========')

p_hat = SAMPLE_ok / SAMPLE_all
sigma_p_hat = sqrt((p_hat * (1 - p_hat)) / SAMPLE_all)
print(f'sigma = {sigma_p_hat}')

p_upper = p_hat + 3 * sigma_p_hat
p_lower = p_hat - 3 * sigma_p_hat
print(f'p_upper = {p_upper}\np_lower = {p_lower}')

print('==========')

S_ok_upper = p_upper * S_all
S_ok_lower = p_lower * S_all
print(f'CI: {S_ok_lower} <= |S_ok| <= {S_ok_upper}')

margin_of_error = S_all * 3 * sigma_p_hat

# margin_of_errorの指数部をS_allに合わせる
# adjust the exponent of margin_of_error to match that of S_all
exponent_S_ok = int('{:e}'.format(p_hat * S_all).split('e')[1])
adjusted_significand_MoE = margin_of_error / (10 ** exponent_S_ok)
print('MoE = ±{:.10f}e{:+d}'.format(adjusted_significand_MoE, exponent_S_ok))
