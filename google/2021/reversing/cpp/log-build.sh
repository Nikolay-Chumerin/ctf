#!/bin/bash
gcc cpp.c -fno-diagnostics-show-caret -ftrack-macro-expansion=0 2>&1 | grep note > build-log.txt