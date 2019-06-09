from PyQuantum.Common.Matrix import *
import PyQuantum.DarkState.operators as op

N_ATOMS_1 = 2
N_ATOMS_2 = 5

N_LEVELS_1 = 2
N_LEVELS_2 = 3

for n_atoms in range(N_ATOMS_1, N_ATOMS_2+1):
    # print('n_atoms', n_atoms)

    for n_levels in range(N_LEVELS_1, N_LEVELS_2+1):
        # print('n_levels', n_levels)

        for i in range(n_levels):
            # print('i', i, end='')

            for j in range(i):
                # print('j', j)

                for i_atom in range(1, n_atoms+1):
                    s = op.Sigma2(
                        i_=i,
                        j_=j,
                        num=i_atom,
                        n_atoms=n_atoms,
                        n_levels=n_levels
                    )

                    # filename = 'dark_dense/' + '_'.join(str(i)
                    # for i in [n_atoms, n_levels, i, j, i_atom]) + '.csv'
                    # print(filename)
                    m = Matrix(m=np.shape(s)[0], n=np.shape(s)[0], dtype=float)
                    # print(s)
                    m.data = s.todense()
                    m.to_csv('dark_dense/' + '_'.join(str(i)
                                                      for i in [n_atoms, n_levels, i, j, i_atom]) + '.csv', precision=0)
                    # for p in s.todense():
                    # print(p)
