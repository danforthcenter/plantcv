### Read image
def readimage(filename):
  # Reads image into numpy ndarray and splits the path and image filename
  # filename = user inputed filename (possibly including a path)
  try:
    img = cv2.imread(filename)
  except:
    fatal_error("Cannot open " + filename);
  
  # Split path from filename
  path, img_name = os.path.split(filename)
  
  return img, path, img_name