# SCAV - P2
We assume that there is a folder called Data which contains all the needed files.
## Exercice 1
In this exercice our goal is being able to extract some useful information from the video. The user can chose between the following options:
1. Duration
2. Height
3. Weight
4. Number of frames
5. Bit rate
6. Know all the spec information.

Notice that for the first 5 choises we had used the following command:

```
command = "ffprobe -v error -select_streams v:0 -show_entries stream={} -of csv=s=x:p=0 {}".format(options[int(x)], dyr.inp)
```
 
Where options[int(x)] contains one of the options and dyr.inp is the input video path.

## Exercice 2
In this exercice our goal is being able to rename the 5 quality outputs of the BBB that you did in last seminar. Notice that you can rename any file iif is inside Data folder.

In order to implement this, we have considered the way the user may put the new name on the terminal. Three possibilities:
- Entering only the name: "hola"
- Entering the name and extension without changing it from the original: "hola.png"
- Entering the name and a new extension: "hola.jpg"

To be able to evaluate this we have used check_ext_name(name) function:

```
def check_ext_name(name):
    split = name.split('.')
    #Check if there is extension
    if(len(split) > 1):
        file_extension = split.pop()
    else:
        file_extension = None

    return split[0],file_extension
```

In order to handle this, our script first checks if the user has included an extension or not. If not the format is mantained. If there is an extension, we check if is different or equal to the original filename: if is equal there is no problem, if is different we will do a change of format(Last exercice).

- When we do not need to change the extension we use: 

```
new_filename= dyr.outp / "{}.{}".format(name,old_ext)
os.rename(dyr.outp/old_file,new_filename)
```

- When we need to change the extension we use: 

```
new_filename= dyr.outp / "{}.{}".format(name,ext)
ext_change(dyr.outp / old_file,new_filename)
```
It should be pointed out that the Data folder files are printed before the user choose the file to rename, in this way the user is not only limited to the past seminar files.

## Exercice 3
In this exercice our goal is to change the resolution of the file that the user has chosen. Again, the Data folder files are printed before the user choose the file to work with.

In order to implement this exercice we also have considered the ways the user may enter the wanted resolution. We consider that there are two main possible formats:
- 720p or 720 format
- 720x480 format

Then, the first step is check which format have used the user by means of split('x') funtion.
If we are in the first case we set the scale as:
```
#ensure that the value is only numeric
new_dim = new_dim[0].split('p')
scale = "{}:-2".format(new_dim[0])
command = "ffmpeg -i Data/{} -vf scale={} -c:v libx264 -crf 18 -preset veryslow -c:a copy Data/{}_{}.{}".format(
                    filename, scale, name, new_dim[0],ext)
 os.system(command)
```
If we are in the second case we set the scale as:
```
scale = "{}:{}".format(new_dim[0],new_dim[1])
command = "ffmpeg -i Data/{} -vf scale={} -c:v libx264 -crf 18 -preset veryslow -c:a copy Data/{}{}_{}.{}".format(
                filename, scale, name,new_dim[0],new_dim[1],ext)
os.system(command)
```
## Exercice 4
In this exercice our goal is being able to transcode the input into an output with another codec. Again, the user is the responsible of chossing the new codec. 
In order to implement this, the avaiable files in the folder are printed in the terminal, then the user choose one of them and indicate the new extension. We have make use of check_ext_name(name) function to being able to separate the name and the extension of the chosen file. The last step is set the new filename as: [file name] + new extension and call ext_change(old,new) function.
```
def ext_change(old,new):
    command = "ffmpeg -i {} -c:v libx264 -crf 18 -preset veryslow -c:a copy {}".format(old, new)
    os.system(command)
```

