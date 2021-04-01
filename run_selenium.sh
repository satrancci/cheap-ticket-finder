arg1=$1
code=$2
echo "Argument received: $arg1"
echo "Code received: $code"

uniq_id=$(echo "$arg1" | cut -d ',' -f1)
echo "uniq id: $uniq_id"
script_type=$(echo "$arg1" | cut -d ',' -f2)
echo "Script type: $script_type"

logs_filename="./data/$uniq_id"_"$code"_"logs.txt"
echo "logs_filename: $logs_filename"

curl ipinfo.io > "$logs_filename"
echo "\n" >> "$logs_filename" 

if [ "$script_type" = "kayak_flight" ]; then
    echo "Running kayak_flights.py..."
    python3 -u kayak_flights.py $arg1 $code
else
    echo "Could not find kayak_flights.py."
    exit 1
fi 

curl ipinfo.io >> "$logs_filename"
