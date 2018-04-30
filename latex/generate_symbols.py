import string
data = [ ]
for letter in string.ascii_letters:
  data.append((letter, r'\mathrm{%s}'%(letter), letter))

x = {
    'alpha' : None,
    'beta' : None,
    'gamma' : None,
    'delta' : None,
    'epsilon' : None,
    'varepsilon' : None,
    'zeta' : None,
    'eta' : None,
    'theta' : None,
    'vartheta' : None,
    'iota' : None,
    'kappa' : None,
    'lambda' : None,
    'mu' : None,
    'nu' : None,
    'xi' : None,
    'pi' : None,
    'varpi' : None,
    'rho' : None,
    'varrho' : None,
    'tau' : None,
    'upsilon' : None,
    'phi' : None,
    'varphi' : None,
    'chi' : None,
    'psi' : None,
    'omega' : None,
    'Delta' : ( r'\Delta', r'\mathchar"7101' ),
    'Xi' : ( r'\Xi', r'\mathchar"7104' ),
    'Lambda' : ( r'\Lambda', r'\mathchar"7103' ),
    'Sigma' : ( r'\Sigma', r'\mathchar"7106' ),
    'Omega' : ( r'\Omega', r'\mathchar"710A' ),
    'Upsilon' : ( r'\Upsilon', r'\mathchar"7107' )
    }

for k in sorted(x.keys()):
  v = x[k]
  if v is None:
    up, slant = r'\up' + k, '\\' + k
  else:
    up, slant = v
  data.append((k, up, slant))

for letter, up, slant in data:
  print r'\DeclareRobustCommand{\P%s}{\ensuremath{\ifthenelse{\boolean{uprightparticles}}{%s}{%s}}\xspace}'%(letter, up, slant)
