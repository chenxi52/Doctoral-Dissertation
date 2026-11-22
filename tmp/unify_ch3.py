import io

def load(p):
    return io.open(p, encoding='utf-8').read()

def save(p, s):
    io.open(p, 'w', encoding='utf-8').write(s)

def apply(text, rules, label):
    for old, new, desc in rules:
        n = text.count(old)
        print('  [%s] %-24s %d' % (label, desc, n))
        text = text.replace(old, new)
    return text

B = chr(92)

rules = [
    (B+'mathscr{L}='+B+'mathcal{S}'+B+'cup'+B+'mathcal{T}_q',
     B+'mathcal{D}_l='+B+'mathcal{S}'+B+'cup'+B+'mathcal{T}_q', 'mathscr L def'),
    (B+'mathcal{L}='+B+'mathcal{S}'+B+'cup'+B+'mathcal{T}_q',
     B+'mathcal{D}_l='+B+'mathcal{S}'+B+'cup'+B+'mathcal{T}_q', 'mathcal L def'),
    ('d_X(x\''+','+B+'mathcal{L})',
     'd_X(x\''+','+B+'mathcal{D}_l)', 'd_X coverage'),
    (B+'mathcal{T}/'+B+'mathscr{L}/'+B+'mathcal{T}_q',
     B+'mathcal{T}/'+B+'mathcal{D}_l/'+B+'mathcal{T}_q', 'table emp dist'),
    (B+'mathcal{R}_{n_t}', B+'mathfrak{R}_{n_t}', 'Rademacher unify'),
    (B+'mathbb{V}_k', 'V_k', 'mathbb V_k -> V_k'),
    ('设 $I='+B+'phi(x)$', '设 $'+B+'mathbf{I}='+B+'phi(x)$', 'I def'),
    (B+'mathrm{sim}(I, w_k)', B+'mathrm{sim}('+B+'mathbf{I}, '+B+'mathbf{w}_k)', 'sim I w'),
    (B+'mathrm{sim}(I, w_i)', B+'mathrm{sim}('+B+'mathbf{I}, '+B+'mathbf{w}_i)', 'sim I wi'),
    ('$w_k='+B+'mathrm{Enc}_t(V_k)$',
     '$'+B+'mathbf{w}_k='+B+'mathrm{Enc}_t(V_k)$', 'w_k def'),
    ('$w_k^0='+B+'mathrm{Enc}_t(V_k^0)$',
     '$'+B+'mathbf{w}_k^0='+B+'mathrm{Enc}_t(V_k^0)$', 'w_k^0 def'),
    ('文本嵌入 $w_k$', '文本嵌入 $'+B+'mathbf{w}_k$', 'w_k prose'),
    ('嵌入 $w_k$', '嵌入 $'+B+'mathbf{w}_k$', 'w_k prose2'),
    (B+'min_{g'+B+'in'+B+'mathcal{G}}', B+'min_{g_V'+B+'in'+B+'mathcal{G}}', 'min g'),
    ('L(h(x),g(x))', 'L(h(x),g_V(x))', 'align loss'),
    ('L(g(x),f\''+'_P(x))', 'L(g_V(x),f\''+'_P(x))', 'vil err loss'),
    ('L(g(x),h(x))', 'L(g_V(x),h(x))', 'align loss2'),
    (B+'mathcal{L}_{kg}', B+'mathcal{L}_{'+B+'text{kg}}', 'L_kg'),
    (B+'mathcal{L}_{ce}', B+'mathcal{L}_{'+B+'text{CE}}', 'L_ce'),
    (B+'mathcal{L}_{ent}', B+'mathcal{L}_{'+B+'text{ent}}', 'L_ent'),
    (B+'mathcal{L}_{div}', B+'mathcal{L}_{'+B+'text{div}}', 'L_div'),
    (B+'mathcal{L}_{dis}^{V'+B+'rightarrow T}',
     B+'mathcal{L}_{V'+B+'leftarrow T}^{dist}', 'L_dis VT'),
    (B+'mathcal{L}_{dis}^{T'+B+'rightarrow V}',
     B+'mathcal{L}_{T'+B+'leftarrow V}^{dist}', 'L_dis TV'),
    ('d_{'+B+'mathcal{Z}}', 'd_Z', 'd_calZ'),
    ('$q$近邻集合${N_1,'+B+'cdots,N_q}$',
     '$q_n$近邻集合${'+B+'mathcal{N}_1,'+B+'cdots,'+B+'mathcal{N}_{q_n}}', 'MH neighbours'),
]

p = 'body/chap3.tex'
s = load(p)
print('=== chap3 ===')
s = apply(s, rules, 'ch3')
save(p, s)
print('saved', p)
