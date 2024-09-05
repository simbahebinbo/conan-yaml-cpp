#!/bin/bash

conan remove yaml-cpp/0.6.2-0f9a586-p1 -c
conan create . --build=missing --update