use 5.16.0;
use strict;
use warnings;

my $N_ATOMS_1 = 2;
my $N_ATOMS_2 = 5;

my $N_LEVELS_1 = 2;
my $N_LEVELS_2 = 3;

for my $n_atoms ( $N_ATOMS_1 .. $N_ATOMS_2 ) {
    for my $n_levels ( $N_ATOMS_1..$N_LEVELS_2 ) {
        for my $i ( 0 .. $n_levels-1 ) {
            for my $j ( 0..$i-1 ) {
                for my $i_atom ( 1 .. $n_atoms ) {
                	my $dense_filename = 'dark_dense/'.$n_atoms.'_'.$n_levels.'_'.$i.'_'.$j.'_'.$i_atom.'.csv';
                	my $sparse_filename = 'dark_sparse/'.$n_atoms.'_'.$n_levels.'_'.$i.'_'.$j.'_'.$i_atom.'.csv';
                	
                	# say 'cmp '.$dense_filename.' '.$sparse_filename;

                	print `cmp $dense_filename $sparse_filename`;
                	# die;
                }
            }
        }
    }
}
