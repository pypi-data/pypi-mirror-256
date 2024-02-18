# updog
A Watchdog, for Services written in python

## Roadmap
- [ ] comunicate between instances (master/ slave)
- [X] Build a Postgres framework as service
- [X] Custom Resolve/Return for services
- [X] get req as service
- [ ] post req as service
- [ ] Notify

## build and publish to pypi
```bash
python3 setup.py sdist bdist_wheel
twine upload dist/*
```
