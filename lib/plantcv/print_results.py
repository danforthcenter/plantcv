### Print Numerical Data

def print_results(filename, header, data):
  print '\t'.join(map(str, header))
  print '\t'.join(map(str, data))