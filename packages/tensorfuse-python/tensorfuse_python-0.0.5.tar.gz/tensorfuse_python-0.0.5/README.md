# Tensorfuse SDK

Python SDK package for Tensorfuse


# Installation
Install the package using the command
```pip install -i https://test.pypi.org/simple/ tensorfuse```

# Usage

Default Logging:

```
from tensorfuse.tensorfuse import log_generic_event

status = log_generic_event(
    token=<AUTH_TOKEN>,
    log=<LOG_OBJECT>
)
```


Logging Using IDs:

```
from tensorfuse.tensorfuse import log_generic_event_using_ids

status = log_generic_event_using_ids(
    token=<AUTH_TOKEN>,
    teamId=<TEAM_ID>, 
    projectId=<PROJECT_ID>, 
    datasourceId=<DATASOURCE_ID>,  
    log=<LOG_OBJECT>
)
```


Logging Using Names:

```
from tensorfuse.tensorfuse import log_generic_event_using_names

status = log_generic_event_using_names(
    token=<AUTH_TOKEN>,
    teamName=<TEAM_NAME>, 
    projectName=<PROJECT_NAME>, 
    datasourceName=<DATASOURCE_NAME>,  
    log=<LOG_OBJECT>
)
```


## The Log Object:

```
log_obj = {
    "query": "<INPUT QUERY>",
    "response1": "<LLM 1 OUTPUT>",
    "response2": "<LLM 2 OUTPUT>",
    "human": "<HUMAN RATING>"
}
```

## Changing the Base Url
### You can also change the ``BASE_URL`` used for the API call

By default:

```
BASE_URL = "https://api.tensorfuse.io/"
```

To change, add the argument ``baseUrl`` in the function you use.

Example:

```
status = log_generic_event_using_names(
    token=<AUTH_TOKEN>,
    teamName=<TEAM_NAME>, 
    projectName=<PROJECT_NAME>, 
    datasourceName=<DATASOURCE_NAME>,  
    log=<LOG_OBJECT>,
    baseUrl="https://localhost:8000/"
)

```
