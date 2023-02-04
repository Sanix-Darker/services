## SERVICES

## HOW TO MAKE IT RUN

Copy the service config to the appropriate directory !

```bash
cd /lib/systemd/system
cp /home/sa/services/service/self-xxxx.service .
```

Then, use systemctl to reload the daemon + enable the service

```bash
sudo systemctl daemon-reload
sudo systemctl enable self-xxxx.service  # works also for 'disable'
```

To check if the service is enable : 

```bash
sudo systemctl list-unit-files | grep self-xxxx.service
```

To start it, you can use the start command :

```bash
sudo systemctl start self-xxxx.service
```
