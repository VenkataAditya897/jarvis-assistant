#!/bin/bash

# Enable apt in the build phase
apt-get update && apt-get install -y espeak-ng
