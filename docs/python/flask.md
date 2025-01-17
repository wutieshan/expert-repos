# Flask


## reference
> - [readthedocs](https://dormousehole.readthedocs.io/en/latest/index.html)


## install
```shell
# flask支持python3.8及以上版本
pip install flask


# (可选)为开发环境额外安装watchdog, 支持reload
pip install watchdog
```


## 启动flask应用
```shell
flask --app=app run --debug --host=0.0.0.0 --port=9012
flask --app=app:app_factory run --debug --port=9012
# --app指定启动的app模块名
# --debug开启debug模式, 启动reload
```