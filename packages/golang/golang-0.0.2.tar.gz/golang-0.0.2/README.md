# golang

Run Go code in Python.

⚠️: WIP

# install

```shell
pip install golang
```

or

```shell
pip install git+ssh://git@github.com/menduo/golang.git
```

# example

## run code

```python
import golang

code = """
package main
import "fmt"

func main(){
    fmt.Println("Hello World from github.com/menduo/golang")
}
"""
golang.run_code(code)
```

## run file

```python
import golang

filepath = "~/ws/contrib/golang/golang/testdata/gocode/code1/main.go"
golang.run_file(filepath)
```

