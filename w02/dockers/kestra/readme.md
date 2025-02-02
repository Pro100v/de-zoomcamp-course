# Kestra 

Download the Docker Compose file using the following command on Linux and macOS:

```bash
curl -o docker-compose.yml \
https://raw.githubusercontent.com/kestra-io/kestra/develop/docker-compose.yml
```

## podman 

Before run docker compose, if for it use **podman**, we need to start podman machine for ability to mount host volumes into container. For more details see: https://stackoverflow.com/questions/69298356/how-to-mount-a-volume-from-a-local-machine-on-podman 

```bash
podman machine init --cpus 2 --rootful -v /tmp:/tmp -v $PWD:$PWD
podman machine start
podman compose up -d
```

### Troubleshuting

```bash
podman machine start
> Starting machine "podman-machine-default"
> Error: could not find "gvproxy" in one of [/usr/local/libexec/podman /usr/local/lib/podman /usr/libexec/podman /usr/lib/podman].  To resolve this error, set the helper_binaries_dir key in the `[engine]` section of containers.conf to the directory containing your helper binaries.
```

We need instal podman-gvproxy 

```bash
sudo dnf install -y podman-gvproxy
```

... i don't fix problem with podman, and install docker
