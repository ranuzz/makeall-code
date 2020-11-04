Scaffolding code for a simple C++ project

### Anatomy of make file

Targets are defined as labels `target:` in the file and the automation tool (make or nmake) can be directed to run them by passing that label as an argument.

Compilation steps include creating object files for all source files and them combining them to create the final binary.

Clean tasks are simply removing all executables, objects and configuration files.

### Snippy

Sample program to get the OS name

### Development and Build

### Linux Steps
 
> Ubuntu 20.04 (make)

```sh
./cofig.sh

make all
```

### Windows Steps

> x64 target on x64 host using VS 2019 CL tool (nmake)

Follow the link to install vscode editor and VS 2019 c++ build tools
> https://code.visualstudio.com/docs/cpp/config-msvc

Open Developer command prompt for VS 2019 <br />
or run 

```sh
"C:\Program Files (x86)\Microsoft Visual Studio\2019\BuildTools\VC\Auxiliary\Build\vcvarsall.bat"
```
from a cmd prompt

Alternatively create a shortcut with following target

> %comspec% /k "C:\Program Files (x86)\Microsoft Visual Studio\2019\BuildTools\VC\Auxiliary\Build\vcvarsall.bat" amd64

If you are using visual studio code then locate project directory and run
```sh
code .
```
and use code's `Build Task` for the compilation.

Alternative;y, run `config.bat` to create build directory and moving appropriate make file and then run `namke all`