#!/bin/bash

# Define the base URL for the Flask API
BASE_URL="http://localhost:5000/api"

# Flag to control whether to echo JSON output
ECHO_JSON=true

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
    echo "Boxer retrieved successfully by ID ($boxer_id)."
    if [ "$ECHO_JSON" = true ]; then
      echo "Boxer JSON (ID $boxer_id):"
      echo "$response" | jq .
    fi
  else
    echo "Failed to get song by ID ($boxer_id)."
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
    echo "Failed to get boxer by name."
    exit 1
  fi
}

##########################################################
#
# Ring Management
#
##########################################################
bout(){
  echo "Fighting boxers in ring..."
  response=$(curl -s -X GET "$BASE_URL/fight")

  if echo "$response" | grep -q '"status": "success"'; then
    echo "Boxers fought successfully."
    if [ "$ECHO_JSON" = true ]; then
      echo "Winner JSON:"
      echo "$response" | jq .
    fi
  else
    echo "Failed to fight boxers."
    exit 1
  fi
}


clear_boxers(){
  echo "Clearing playlist..."
  response=$(curl -s -X POST "$BASE_URL/clear-boxers")

  if echo "$response" | grep -q '"status": "success"'; then
    echo "Ring cleared successfully."
  else
    echo "Failed to clear ring."
    exit 1
  fi

}

enter_ring(){
  name=$1

  echo "Adding boxer to ring: $name..."
  response=$(curl -s -X POST "$BASE_URL/enter-ring" \
    -H "Content-Type: application/json" \
    -d "{\"name\":\"$name\"}")

  if echo "$response" | grep -q '"status": "success"'; then
    echo "Boxer added to ring successfully."
    if [ "$ECHO_JSON" = true ]; then
      echo "Boxer JSON:"
      echo "$response" | jq .
    fi
  else
    echo "Failed to add song to playlist."
    exit 1
  fi
}

get_boxers() {
  echo "Getting all boxers in the ring..."
  response=$(curl -s -X GET "$BASE_URL/get-boxers")
  if echo "$response" | grep -q '"status": "success"'; then
    echo "All boxers retrieved successfully."
    if [ "$ECHO_JSON" = true ]; then
      echo "Boxers JSON:"
      echo "$response" | jq .
    fi
  else
    echo "Failed to get boxers."
    exit 1
  fi

}
######################################################
#
# Leaderboard
#
######################################################

# Function to get the song leaderboard sorted by play count
get_leaderboard() {
  sortby=$1

  echo "Getting boxer leaderboard sorted by $sortby..."
  response=$(curl -s -X GET "$BASE_URL/song-leaderboard?sort=$sortby")
  if echo "$response" | grep -q '"status": "success"'; then
    echo "Boxing leaderboard retrieved successfully."
    if [ "$ECHO_JSON" = true ]; then
      echo "Leaderboard JSON (sorted by $sortby):"
      echo "$response" | jq .
    fi
  else
    echo "Failed to get boxing leaderboard."
    exit 1
  fi
}

# Initialize the database
sqlite3 db/ring.db < sql/init_db.sql

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
get_leaderboard "wins"
get_leaderboard "win_pct"

echo "All tests passed successfully!"
