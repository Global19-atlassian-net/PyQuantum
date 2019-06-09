use 5.16.0;
use strict;
use warnings;

# system("python3 -O ../run_tc.py --config=./test_tcl/tc_config.py > /dev/null");
# system("python3 -O ../run_tc_l.py --config=./test_tcl/tcl_config.py > /dev/null");

system("python3 ../run_tc.py --config=./test_tcl/tc_config.py > /dev/null");
system("python3 ../run_tc_l.py --config=./test_tcl/tcl_config.py > /dev/null");

system("cmp test_tcl/TC/out/2_2/z.csv test_tcl/TCL/out/2_2/z.csv");
system("cmp test_tcl/TC/out/2_2/x.csv test_tcl/TCL/out/2_2/x.csv");
system("cmp test_tcl/TC/out/2_2/t.csv test_tcl/TCL/out/2_2/t.csv");

# system("rm -r test_tcl/TC  2>/dev/null || true");
# system("rm -r test_tcl/TCL 2>/dev/null || true");
