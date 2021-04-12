# autobuild

Generate **docker-compose** file using Jinja2 template from custom configuration **custom.yaml**

## custom.yaml format

* j2template - Jinja2 template to be used
* name - output docker-compose file name
* daemons 

## mandatory daemon vars

All daemons are declared using the following structure
```   
 - name: XXX
   image: docker-image
   config_mount_dir: /path
   data_mount_dir: /path
   ```

!!! Daemons with missing variables will not be taken into consideration !!!
   
The daemons listed below need special configuration

* XR_PROXY

```   
 - name: XR_PROXY
   image: blocknetdx/exrproxy:latest
   config_mount_dir: /test/path1
   nginx_mount_dir: /test/path2
   ```

> nginx_mount_dir

* ETH

```
    - name: ETH
      image: blocknetdx/eth-payment-processor:0.5.2
      postgresql_data_mount_dir: /test/path1
      geth_data_mount_dir: /test/path2
```
>postgresql_data_mount_dir
>geth_data_mount_dir
