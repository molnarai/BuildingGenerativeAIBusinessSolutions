#!/bin/bash
JSON_FILE=${1:-}
# cat "$JSON_FILE"| jq ".results.audio_segments[] | {speaker_label, transcript}"
cat "$JSON_FILE"| jq -r '"| Speaker | Transcript |\n|----|----|\n",  (.results.audio_segments[] | "| \(.speaker_label) | \(.transcript) |")'
# cat "$JSON_FILE"| jq -r '
#   "| Speaker | Transcript |\n|----|----|\n",
#   (.results.audio_segments | group_by(.speaker_label)[] | 
#    "| \(.[0].speaker_label) | \(map(.transcript) | join(" ")) |")
# '