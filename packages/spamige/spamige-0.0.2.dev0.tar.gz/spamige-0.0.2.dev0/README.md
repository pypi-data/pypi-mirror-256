# spamige

Wrapper for [spam](https://www.spam-project.dev/docs/installation/users.html) in order to describe the workflow used for correlation from laboratory experiment on ice.

# Quick start

## Clone the repository and install the wrapper using mamba

[mamba](https://mamba.readthedocs.io/en/latest/user_guide/mamba.html#mamba) is recommended to performed the isntallation but if you are more familiar with conda replace mamba by conda bellow.

```bash
git clone https://gricad-gitlab.univ-grenoble-alpes.fr/mecaiceige/tools/lib_python/spamige
cd spamige
mamba env create -f environment.yml
```

## Peformed rapid correlation

You need to have one folder containing all the tiff images that you want to use for the correlation. The images will be treated in the "natural" order given by [natsort.natsorted](https://natsort.readthedocs.io/en/5.4.0/natsorted.html) python function.

You also need on `mask.tiff` defining the region of interest (white: correlation, black: no correlation)

```bash
├── images_experiment
│   ├── img_1.tiff
│   ├── img_2.tiff
│   ├── ...
│   ├── img_10.tiff
│   ├── img_11.tiff
│   ├── ...
├── mask
│   ├── mask.tiff
```

Python script : `script_dic.py`

```python
import spamige.wrapper as spw

path_to_img='images_experiment/'
mask='mask/mask.tiff'

hws=20

spw.spam_workflow(path_to_img,mask,hws=hws,folder_prefix='hws'+str(hws))
```

Run the script

```bash
mamba activate spamige
python script_dic.py
```

It will performed correlation and create displacement and strain fields output.

```bash
├── images_experiment
├── mask
├── hws20
│   ├── spam-init_guess
|       ├── *.tsv
│   ├── spam-ldic-filtered
|       ├── *.vtk
│   ├── spam-ldic-not-filtered
|       ├── *.vtk
│   ├── spam-strain-filtered
|       ├── *.vtk
│   ├── spam-strain-not-filtered
|       ├── *.vtk
```
Folder's content:
- `spam-ldic-filtered`: filtered displacement fields
- `spam-ldic-not-filtered`: **not** filtered displacement fields
- `spam-strain-filtered`: filtered strain fields
- `spam-strain-not-filtered`: **not** filtered strain fields