**Overview**

For photographers keeping every raw file captured can use a lot of space.  
This utility allows a photographer to purge any unused raw files leaving 
only the processed files with their associated raws


For example, given the folder1 below:

<pre>
folder1/
  IMG_1000.cr3
  IMG_1001.cr3
  IMG_1002.cr3
  Processed/
    IMG_1000.jpg
</pre>

Running `praw -i /blah/folder1` would remove 1001 and 1002 raw 
files as they don't have an associated cr3 file, yielding:

<pre>
folder1/
  IMG_1000.cr3
  Processed/
    IMG_1000.jpg
</pre>
