import os, re, shutil
from tempfile import mkdtemp, NamedTemporaryFile
from subprocess import call, check_output

# this is the directory in the git repository that contains .bib files
git_prefix = 'bibliography/'

# svn URL -- you may need to tweak this depending on how you want to authenticate etc.
url_prefix = 'svn+ssh://cernsvn/reps/lhcbdocs/Templates/LHCb-latex-template/latest/latex/'

# below here should "just work" -- run from the root directory of a checkout of the git repository

# store where we started (we chdir to a toy git repo below)
orig_directory = os.getcwd()

results = [ ]
for fname in ['LHCb-PAPER.bib', 'LHCb-DP.bib', 'LHCb-CONF.bib', 'LHCb-TDR.bib', 'main.bib']:
  git_file_name = git_prefix + fname
  url = url_prefix + fname

  # Make sure we're in the real git repository
  os.chdir(orig_directory)
  abs_git_file_name = os.path.abspath(git_file_name)

  # look at the git history for this file
  # result is ordered [newest, ..., oldest]
  old_svn_commit = None
  git_log_string = check_output(['git', 'log', '--format=%B%x00', git_file_name]).decode()
  log_lines = [ x.strip() for x in git_log_string.split("\0") ]
  for log_line in log_lines:
    m = re.match('^lhcbdocs-svn-update-(\d+)-(\d+):', log_line)
    if m:
      # There's an old commit updating from SVN revision m.group(1) to m.group(2)
      old_svn_commit = int(m.group(2))
      print("Last update was " + m.group(1) + " -> " + m.group(2))

  # if we couldn't figure out what the last SVN revision that was imported was, hardcode some defaults
  if old_svn_commit is None:
    old_svn_commit = {
        'main.bib' : 112450,
        'LHCb-DP.bib' : 111782,
        'LHCb-TDR.bib' : 104311,
        'LHCb-CONF.bib' : 109627,
        'LHCb-PAPER.bib' : 117445,
        }[fname]
    print("WARNING: couldn't find old svn-update commit, using a hardcoded revision " + str(old_svn_commit))

  # see what the latest version in SVN is -- do we actually need to do anything?
  new_svn_commit = int(check_output(['svn', 'info', '--show-item', 'last-changed-revision', url]))

  if old_svn_commit == new_svn_commit:
    print("No update needed, skipping " + git_file_name)
    continue
  else:
    print("Updating from SVN revision %d -> %d"%(old_svn_commit, new_svn_commit))

  # Use git to do a 3-way merge
  old_svn_file_name = git_file_name + '.svnold'
  new_svn_file_name = git_file_name + '.svnnew'
  call(['svn', 'export', '--revision', str(old_svn_commit), url, old_svn_file_name])
  call(['svn', 'export', '--revision', str(new_svn_commit), url, new_svn_file_name])
  merge_result = call(['git', 'merge-file', git_file_name, old_svn_file_name, new_svn_file_name])
  os.remove(old_svn_file_name)
  os.remove(new_svn_file_name)

  # Get the svn history that we're merging
  svn_log = check_output(['svn', 'log', '--revision', str(old_svn_commit) + ':' + str(new_svn_commit), url])

  # Construct the commit message
  commit_message = "lhcbdocs-svn-update-%d-%d:\n\n%s"%(old_svn_commit, new_svn_commit, svn_log)

  # Store the results -- split into two loops like this so that the git output doesn't swamp the messages we print below
  results.append((merge_result, git_file_name, commit_message))

# Go back to the main directory
os.chdir(orig_directory)

if len(results):
  print('')
  print('='*60)
  print('')

for merge_result, git_file_name, commit_message in results:
  # If the merge was successful, we can commit the result
  if merge_result == 0:
    call(['git', 'commit', '-m', commit_message, git_file_name])
  else:
    with NamedTemporaryFile(delete=False) as ofile:
      msg_file = ofile.name
      ofile.write(commit_message)
    print("Merge of %s failed, resolve it yourself and then run: git commit --file=%s %s"%(git_file_name, msg_file,
      git_file_name))
