<a name="readme-top"></a>

<!-- PROJECT LOGO -->
<br />
<div align="center">
    <img src="https://github.com/dave-lanigan/lambchop/assets/29602997/9c0826c8-b6b0-4ad7-84f4-85ff4b1e7c74" alt="Logo" width="250" height="250">

  <h3 align="center">lambchop</h3>

  <p align="center">
    A sidekick that makes your AWS Lambda async
  <br/>

   ![](https://img.shields.io/badge/language-python-blue)
   ![version](https://img.shields.io/badge/version-0.0.12-green)
   ![](https://img.shields.io/badge/license-MIT-red)
   
  </p>
</div>

## Overview

`lambchop` is an Python package that gives regular AWS Lambda asyncronous functionality by allow them to run background processes. This works by utilizing AWS Lambda [extensions](https://docs.aws.amazon.com/lambda/latest/dg/lambda-extensions.html) which runs in a different process than the main lambda function code.


## Installation
pypi:

```
pip install lambchop
```

github:

```
pip install git+ssh://git@github.com/dave-lanigan/lambchop.git
```
```
pip install git+https://git@github.com/dave-lanigan/lambchop.git
```

> 📝 Sudo privileges may be required because the lambda extension resides in the `/opt/extensions/` directory

## Usage

```
import time
from lambchop import SideKick

def long_running_process(x, y):
    print("Starting process 1.")
    time.sleep(x + y)
    print("Completed.")


def long_running_process2(x, y):
    print("Starting process 2.")
    time.sleep(x + y)
    print("Completed.")


def main():
    sk = SideKick()
    sk.add_task(long_running_process, x=5, y=3)
    sk.add_task(long_running_process2, x=5, y=3)
    sk.process()

if __name__ == "__main__":
    main()
```