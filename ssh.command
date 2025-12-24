#!/bin/bash

# Define the servers, their respective private keys, and user-friendly names
declare -A servers=(
  [1]="ubuntu@89.168.52.201"
  [2]="ubuntu@89.168.58.163"
  [3]="ubuntu@143.47.37.105"
)
declare -A keys=(
  [1]="/Users/pixo/Documents/Me/keys/priv/pixo.key"
  [2]="/Users/Pixo/Documents/Me/keys/priv/haroune.key"
  [3]="/Users/Pixo/Documents/Me/keys/priv/madara.key"
)
declare -A names=(
  [1]="Pixo"
  [2]="Haroune"
  [3]="Madara"
)

# Function to display the menu
display_menu() {
  clear
  echo "========================="
  echo "  SSH Server Connector"
  echo "========================="
  echo ""
  echo "Please choose a server to connect to:"
  for i in "${!servers[@]}"; do
    echo "$i) ${names[$i]}"
  done
  echo "0) Exit"
  echo ""
}

# Function to handle invalid choice
invalid_choice() {
  echo "Invalid choice. Please try again."
  sleep 1
}

# Function to connect to the chosen server
connect_to_server() {
  local choice=$1
  echo "Connecting to ${names[$choice]} (${servers[$choice]})..."
  ssh -i "${keys[$choice]}" "${servers[$choice]}"
}

# Main loop for user input
while true; do
  display_menu
  read -p "Enter the number of the server you want to connect to: " choice

  case $choice in
    0)
      echo "Exiting."
      exit 0
      ;;
    [1-3])
      connect_to_server "$choice"
      break
      ;;
    *)
      invalid_choice
      ;;
  esac
done
