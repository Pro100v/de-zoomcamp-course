#!/bin/bash

echo "This is answer for hw-01 #1 question:"
podman run --rm --name hw-01 python:3.12.8 sh -c "pip -V | awk '{print \$2}'"