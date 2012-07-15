import subprocess
import os
import time
import sys

class GitMirror():
  def __init__(self, mirror, sections):
    if mirror[len(mirror)-1] != '/':
      mirror += '/'
      
    self.mirror = mirror
    self.sections = sections
    
    #first, initialize this area if we've never been here before
    if not os.path.exists('.git'):
      subprocess.check_output(['git', 'init'])
      self.createPatch = False
      self.lastCommit = None
    else:
      self.createPatch = True
      str = subprocess.check_output(['git', 'log'])
      lines = str.split('\n')
      if len(lines) != 0:
        tokens = lines[0].split(' ')
        if len(tokens) < 2 or tokens[0] != 'commit':
          self.lastCommit = None
        else:
          self.lastCommit = tokens[1]
      else:
        self.lastCommit = None
  
  def createMirror(self):
    print("Starting to download all the files from %s" % (self.mirror))
    if (not self.createPatch and self.lastCommit is None):
      print("Since this is your first time this process will take while depending on the speed if your connection.  It's probably best if you run this over night.")

    if self.sections is None:
      self.mirrorSection('')
    else:
      for section in self.sections:
        self.mirrorSection(section)

    #next, commit them all to the Git repository
    subprocess.check_output(['git', 'add', '.'])
    subprocess.check_output(['git', 'commit', '-m', '"Latest mirror updates"'])
    if self.lastCommit is None:
      print("Since this is your first time, you'll have to pack up this entire directory and take it with you.")
    else:
      subprocess.check_output(['git', 'format-patch', '%s' % (self.lastCommit)])

  def mirrorSection(self, section):
    #next, download the various resources held at a Jenkins mirror
    fullPath = self.mirror + section + '/'
    print("Mirroring %s" % (fullPath))
    download = subprocess.Popen(['wget', '-m', '-np', '-q', fullPath])
    download.poll()
    while (download.returncode is None):
      time.sleep(1)
      sys.stdout.write('.')
      sys.stdout.flush()
      download.poll()
    
    if (download.returncode != 0):
      raise Exception('Failed to mirror %s' % (fullPath))

def usage():
  print("%s <mirror> [section1] [section2] ... [sectionN]" % (sys.argv[0]))

if __name__ == '__main__':
  if len(sys.argv) < 2:
    usage()
  if len(sys.argv) == 2:
    print("Warning: Your selected options will result in a FULL copy of your selected mirror.  Make sure you have enough disk space to complete this operation.")
    var = raw_input("Are you sure you want to proceed? [Y/N]: ")
    if var != 'Y' and var != 'y':
      exit()
    sections = None
  else:
    sections = sys.argv[2:]
    sections.append('art')
    sections.append('updates')
  
  GitMirror(sys.argv[1], sections).createMirror()
  