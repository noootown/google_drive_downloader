import subprocess
import argparse
import sys
import re

def parse_args():
  parser = argparse.ArgumentParser()
  parser.add_argument('--url', dest='url', help='download url', default='', type=str)
  parser.add_argument('--cookie', dest='cookie', help='cookie', default='cookie', type=str)
  parser.add_argument('--file', dest='filename', help='file', default='file', type=str)
  args = parser.parse_args()

  if len(sys.argv) == 1 or not args.url:
    parser.print_help()
    sys.exit(1)

  return args

if __name__ == '__main__':
  args = parse_args()
  gid = re.findall('^https?://drive.google.com/file/d/([^/]+)', args.url)[0]

  def wget(url, filename = ''):
    cmd = 'wget'
    cmd += ' --tries=3 --no-check-certificate --load-cookie %s --save-cookie %s %s' % (args.cookie, args.cookie, url)
    if filename:
      cmd += ' -O %s' % filename
    subprocess.call(cmd.split(' '))

  wget('https://docs.google.com/uc?id=%s&export=download' % gid, args.filename)

  try:
    with open(args.filename, 'r') as file:
      href = re.findall('href="(\/uc\?export=download[^"]+)', file.read())

    if href:
      wget('https://docs.google.com%s' % href[0].replace('&amp;', '&'), args.filename)
  except:
    pass

  print('Finish downloading %s' % args.filename)
