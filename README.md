## Requirements

Python      3.5  
requests    2.10.0  

```sh
$ pip install -r requirements.txt
```

## Usage

Running ghtool:

```sh
$ ./ghtool -h
```

Prints:
```
usage: ghtool [-h] {list,desc,latest} ...

Provides data and information from GitHub

positional arguments:
  {list,desc,latest}  Available commands
    list              Lists latest repository with applied filters
    desc              Shows info on requested repositories
    latest            Shows name of newest repository

optional arguments:
  -h, --help          show this help message and exit
```

### Examples


```sh
$ ./ghtool list
```  

```sh
$ ./ghtool list ruby
```  

```sh
$ ./ghtool list ruby -n 10
```  

-t provides extended output e.g  
\#15 creator/repo_name 02.07.2017--21:45:30

```sh
$ ./ghtool list ruby -n 50 -t
```

Latest - Name of newest public github repo

```sh
$ ./ghtool latest
```

Desc - requests info on github repositories, does it in parallel


```sh
$ ./ghtool desc michaelnickson/icfwebsite_project heitorchang/mytags-revival lddahz789/blogSource EmplaceBackCS/Unity3D-MMO-Style-Cam geeckmc/MOOZISMS-JAVASCRIPT_SDK Leelava/CoreJava-Assignment5.4 TunnyTraffic/hashid egarat/vuejs-vuex-project-list nagasaimanoj/NareshIT-Manikanta-Sir flmn28/profy yavtuk/yavtuk.github.io augustinevt/AE-React-Boiler
```
