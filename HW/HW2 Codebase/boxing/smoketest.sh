#!/bin/bash

# Define the base URL for the Flask API
BASE_URL="http://localhost:5000/api"

# Flag to control whether to echo JSON output
ECHO_JSON=false

# Parse command-line arguments
while [ "$#" -gt 0 ]; do
  case $1 in
    --echo-json) ECHO_JSON=true ;;
    *) echo "Unknown parameter passed: $1"; exit 1 ;;
  esac
  shift
done


###############################################
#
# Health checks
#
###############################################

# Function to check the health of the service
check_health() {
  echo "Checking health status..."
  curl -s -X GET "$BASE_URL/health" | grep -q '"status": "success"'
  if [ $? -eq 0 ]; then
    echo "Service is healthy."
  else
    echo "Health check failed."
    exit 1
  fi
}

# Function to check the database connection
check_db() {
  echo "Checking database connection..."
  curl -s -X GET "$BASE_URL/db-check" | grep -q '"status": "success"'
  if [ $? -eq 0 ]; then
    echo "Database connection is healthy."
  else
    echo "Database check failed."
    exit 1
  fi
}


##########################################################
#
# Boxer Management
#
##########################################################

add_boxer() {
  name=$1
  weight=$2
  height=$3
  reach=$4
  age=$5

  echo "Adding boxer ($name, $weight, $height, $reach, $age) to the boxers..."
  curl -s -X POST "$BASE_URL/add-boxer" -H "Content-Type: application/json" \
    -d "{\"name\":\"$name\", \"weight\":\"$weight\", \"height\":$height, \"reach\":\"$reach\", \"age\":$age}" | grep -q '"status": "success"'

  if [ $? -eq 0 ]; then
    echo "Boxer added successfully."
  else
    echo "Failed to add boxer."
    exit 1
  fi
}

delete_boxer() {
  boxer_id=$1

  echo "Deleting boxer by ID ($boxer_id)..."
  response=$(curl -s -X DELETE "$BASE_URL/delete-boxer/$boxer_id")
  if echo "$response" | grep -q '"status": "success"'; then
    echo "Boxer deleted successfully by ID ($boxer_id)."
  else
    echo "Failed to delete boxer by ID ($boxer_id)."
    exit 1
  fi
}

get_boxer_by_id() {
  boxer_id=$1

  echo "Getting boxer by ID ($boxer_id)..."
  response=$(curl -s -X GET "$BASE_URL/get-boxer-by-id/$boxer_id")
  if echo "$response" | grep -q '"status": "success"'; then
    echo "Song retrieved successfully by ID ($song_id)."
    if [ "$ECHO_JSON" = true ]; then
      echo "Song JSON (ID $song_id):"
      echo "$response" | jq .
    fi
  else
    echo "Failed to get song by ID ($song_id)."
    exit 1
  fi
}

get_boxer_by_name() {
  name=$1

  echo "Getting boxer by name ($name)..."
  response=$(curl -s -X GET "$BASE_URL/get-boxer-by-name/$name")
  if echo "$response" | grep -q '"status": "success"'; then
    echo "Boxer retrieved successfully by name ($name)."
    if [ "$ECHO_JSON" = true ]; then
      echo "Boxer JSON (by name):"
      echo "$response" | jq .
    fi
  else
    echo "Failed to get song by compound key."
    exit 1
  fi
}

##########################################################
#
# Ring Management
#
##########################################################
bout(){

}


clear_boxers(){

}

enter_ring(){

}

get_boxers() {

}
######################################################
#
# Leaderboard
#
######################################################

# Function to get the song leaderboard sorted by play count
get_leaderboard() {
  echo "Getting song leaderboard sorted by play count..."
  response=$(curl -s -X GET "$BASE_URL/song-leaderboard?sort=play_count")
  if echo "$response" | grep -q '"status": "success"'; then
    echo "Song leaderboard retrieved successfully."
    if [ "$ECHO_JSON" = true ]; then
      echo "Leaderboard JSON (sorted by play count):"
      echo "$response" | jq .
    fi
  else
    echo "Failed to get song leaderboard."
    exit 1
  fi
}

# Initialize the database
sqlite3 db/playlist.db < sql/init_db.sql

# Health checks
check_health
check_db

# Boxer functions
add_boxer "Boxer1" 150 70 74.5 25
add_boxer "Boxer2" 170 74 78.5 25
add_boxer "Boxer3" 180 72 74.3 30
add_boxer "Boxer4" 134 73 74.5 30
add_boxer "Boxer5" 200 76 80.5 24

delete_boxer 1

get_boxer_by_id 2
get_boxer_by_name "Boxer1"

# Ring functions
bout
clear_boxers

enter_ring
get_boxers

# Leaderboard
get_leaderboard "win"
get_leaderboard "loss"

echo "All tests passed successfully!"
