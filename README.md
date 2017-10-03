# KYPO Networking

## Testing

```shell
pushd master
python -m tox
popd
```

## Deployment and usage

```shell
SANDBOX_NAME='routing-119' SSH_CONFIG='/home/user/.ssh/config' fab deploy
ssh routing-119
kyponet-master
ssh 172.16.1.2
ping 10.0.1.2
...
```
