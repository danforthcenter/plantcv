### Error handling
def fatal_error(error):
  # Print out the error message that gets passed, then quit the program
  # Error = error message text
  raise RuntimeError(error)