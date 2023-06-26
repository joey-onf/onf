#!/bin/bash

declare -a files=( $(find . -name '*.py' -print) )
files+=('makefile')

emacs "${files[@]}"
