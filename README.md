# logparser
AWS ELB 로그를 읽어와 분석합니다.

## Install
```shell
pip install -e .
```

## Usage

### get_log

ELB 로그 파일이 있는 곳을 `log_dir` 로 지정하여 로그 파일을 읽습니다. 로그 파일의 확장자는 `.gz`입니다.

```python
from logparser import get_log
import os    

log_dir = os.getcwd()
log_files = get_log(log_dir)
```

### logparse

분석에 사용할 수 있도록 로그를 파싱합니다. 

```python
from logparser import logparse
import os

logs = logparse(log_files)
```

## Options

아래와 같은 기능을 사용할 수 있습니다.

- `count(logs)` : 로그 개수를 확인합니다.
- `sequence(logs, field, reverse=False)` : field별 값의 로그 수를 세고, 로그 수를 기준으로 정렬합니다.
    - field : string
    - reverse: boolean
- `find(logs, field, find_value)`:  field의 특정 값으로 로그를 찾습니다.
    - field : string
    - find_value : string
- `period(logs, startdate, enddate)` :  특정 기간에 해당하는 로그를 찾습니다.
    - startdate, enddate : datetime

---

field 종류는 [다음 링크](https://docs.aws.amazon.com/elasticloadbalancing/latest/application/load-balancer-access-logs.html#access-log-entry-format) 를 확인하세요.

### Example

```python
from logparser import get_log, logparse, find
import os

log_dir = os.getcwd()
log_files = get_log(log_dir)
logs = logparse(log_files)

result = find(logs, 'user_agent', 'windows') 

for r in result:
	print(r['user_agent']) #or print(r)
```

## To Do

- `as_data(logs)` : change data type from generate type to list type
- `to_csv(result)` : save the analyze result to csv file
- `to_graph(result)` : draw the analyze result to graph
- ...

## Blog

프로젝트 제작 과정을 살펴 볼 수 있습니다.

- [pytest 사용기](https://jyejin.github.io/2020/08/09/project-3/
)