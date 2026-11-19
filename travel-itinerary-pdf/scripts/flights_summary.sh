#!/bin/bash
# Summarise a saved Skyscanner search_flights JSON result (round trip), cheapest first.
# usage: flights_summary.sh <result.json> [N]
jq -r --argjson n "${2:-14}" '[.buckets[].items[]] | unique_by(.id) | sort_by(.price.raw) | .[:$n][] |
 "\(.price.formatted) | " + ([.legs[] | ([.segments[] | "\(.marketingCarrier.displayCode)\(.flightNumber) \(.origin.displayCode)\(.departure[11:16])-\(.destination.displayCode)\(.arrival[11:16])"] | join(" + ")) + " (\(.durationInMinutes)m,\(.stopCount)st)"] | join("  ||  "))' "$1"
