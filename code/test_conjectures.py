from check_conjectures import check_dataset
from check_conjectures import check_random
from check_conjectures import print_summary

log_file = 'counter-examples.txt'
check_dataset(log_file)
check_random(log_file, 5000)
print_summary()