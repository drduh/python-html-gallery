#!/usr/bin/env python
#
# Generates thumbnails and HTML gallery pages for jpgs in a directory.

import datetime
import glob
import fnmatch
import os
import random
import re
import shutil
import static
import sys
import time

try:
  from PIL import Image
except ImportError:
  try:
    import Image
  except ImportError:
    print 'Requires Python Imaging Library. See README.'
    sys.exit(1)


def ListFiles(regex, path):
  """Returns list of matching files in path."""
  rule = re.compile(fnmatch.translate(regex), re.IGNORECASE)
  return [name for name in os.listdir(path) if rule.match(name)] or None


def ListDirs(path):
  """Returns list of directories in path."""
  return [d for d in os.listdir(path) if os.path.isdir(
      os.path.join(path, d))]


def Now(time=True):
  """Returns formatted current time."""
  if time:
    return datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')
  else:
    return datetime.datetime.now().strftime('%Y%m%d')


def RandomThumb(page):
  """Returns path to random thumbnail for a given page."""
  return random.choice(
      glob.glob(os.path.join(page.split('/')[0], '*_thumb.jpg')))


def OrganizeRoot():
  """Creates directories for images in root directory."""
  try:
    os.chdir(static.root)
  except OSError:
    print 'Could not cd into %s' % static.root
    sys.exit(1)

  fs = ListFiles('*.jpg', '.')
  if fs:
    for jpg in fs:
      datehour = Now(time=False)
      if not os.path.exists(datehour):
        print 'Creating directory: %s' % datehour
        os.makedirs(datehour)
      if not os.path.exists(os.path.join(datehour, jpg)):
        shutil.move(jpg, datehour)
      else:
        print '%s already exists' % os.path.join(datehour, jpg)


def GenerateThumbnails(page, jpgs):
  """Generates thumbnails for gallery pages.

  Args:
    page: str, name of page for thumbnails.
    jpgs: list, jpg files to create thumbnails for.
  Returns:
    url_imgs: list, image links to write.
  """
  c_exist = 0
  c_save = 0
  c_small = 0
  pc = 0
  url_imgs = []

  for jpg in jpgs:
    try:
      im = Image.open(jpg)
      if im.size > static.min_size:
        thumb = '%s_%s.%s' % (jpg.split('.')[0], 'thumb', 'jpg')
        if not os.path.exists(thumb):
          im.thumbnail(static.thumb_size, Image.ANTIALIAS)
          im.save(thumb, 'JPEG')
          c_save += 1

          if (pc == 100):  # progress counter
            print '%s: wrote 100 thumbnails, continuing' % page
            pc = 0
          pc += 1

        else:
          c_exist += 1

        url_imgs.append(static.url_img % (jpg, jpg, thumb))
      else:
        if '_thumb.jpg' not in jpg:
          c_small += 1
    except IOError as e:
      print 'Problem with %s: %s, moving to %s' % (jpg, e, static.tmp)
      try:
        shutil.move(jpg, static.tmp)
      except shutil.Error:
        print 'Could not move %s' % jpg
        pass

  print '%s: %d new thumbnails, %d already exist, %d too small' % (
      page, c_save, c_exist, c_small)
  return url_imgs


def WriteGalleryPage(page):
  """Writes a gallery page for jpgs in path.

  Args:
    page: str, name of page under root directory.
  """
  os.chdir(os.path.join(static.root, page))

  with open(static.index, 'w') as index_file:
    index_file.write(static.header % page)
    index_file.write(static.timestamp % Now())

    try:
      jpgs = sorted(ListFiles('*.jpg', '.'))[::-1]
    except TypeError:
      print '%s: No images found' % page
      return

    for e in GenerateThumbnails(page, jpgs):
      index_file.write(e)

    index_file.write(static.footer)


def WriteGalleryPages():
  """Write gallery pages for directories in root path."""
  for page in sorted(ListDirs(static.root), key=os.path.getmtime):
    WriteGalleryPage(page)


def WriteIndex():
  """Write index file with gallery links and thumbnails in root path."""
  os.chdir(static.root)

  with open(static.index, 'w') as index_file:
    index_file.write(static.header % 'Good day to you, sir/madam!')
    index_file.write(static.timestamp % Now())

    page_count = 0
    for page in sorted(glob.glob('*/%s' % static.index)):
      page_count += 1
      try:
        for _ in range(static.n_thumbs):
          index_file.write(static.img_src % RandomThumb(page))
        index_file.write(static.url_dir % (page, page.split('/')[0]))
      except IndexError:
        print '%s: No thumbnails found, removing' % page
        os.unlink(page)

    index_file.write(static.footer)

  print 'Wrote %s with %s gallery link(s)' % (
      os.path.join(static.root, static.index), page_count)


def main():
  """Main function."""
  OrganizeRoot()
  WriteGalleryPages()
  WriteIndex()


if __name__ == '__main__':
  main()
