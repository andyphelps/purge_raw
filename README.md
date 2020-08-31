Utility to remove unprocessed RAW files from a folder keeping only RAW files that yielded results

For example, given the folder1 below:

<pre>
folder1/
  IMG_1000.cr3
  IMG_1001.cr3
  IMG_1002.cr3
  Processed/
    IMG_1000.jpg
</pre>

running `python3 purgeraw.main -i /blah/folder1` would remove 1001 and 1002 raw files yielding:

<pre>
folder1/
  IMG_1000.cr3
  Processed/
    IMG_1000.jpg
</pre>

