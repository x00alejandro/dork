#!/bin/bash

declare -A GITHUB=(["start"]="https://github.com/search?q=%22" ["end"]="&type=Code")

raw() {
    local keyword=$1

    touch "${keyword}_raw.txt"

        while read -r line; do
          modified_line="${GITHUB[start]}${keyword}%22+${line}${GITHUB[end]}"
          echo "$modified_line" >> "${keyword}_raw.txt"
        done < github_keywords.txt
}

verbose() {
    local keyword=$1

        touch "${keyword}_verbose.txt"

      while read -r line; do
        if [[ "$line" != "" ]]; then
            echo "##### ${line} #####" >> "${keyword}_verbose.txt"
            echo "${GITHUB[start]}${keyword}%22+${line}${GITHUB[end]}" >> "${keyword}_verbose.txt"
            echo "" >> "${keyword}_verbose.txt"
        fi
      done < github_keywords.txt
}

main() {
  while [[ $# -gt 0 ]]; do
    case "$1" in
      -r|--raw)
        raw=true
        shift
        ;;
      -v|--verbose)
        verbose=true
        shift
        ;;
      -a|--all)
        all=true
        shift
        ;;
      *)
        param="$1"
        shift
        ;;
    esac
  done

  if [ -z "$raw" ] && [ -z "$verbose" ] && [ -z "$all" ]; then
    echo "Error: No flag provided."
    exit 1
  fi

  if [ -z "$param" ]; then
    echo "Error: No parameter provided."
    exit 1
  fi

  if [ "$raw" ]; then
    raw "$param"
  fi
  if [ "$verbose" ]; then
    verbose "$param"
  fi
  if [ "$all" ]; then
    raw "$param"
    verbose "$param"
  fi
}

main "$@"
