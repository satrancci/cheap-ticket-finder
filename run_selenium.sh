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

echo "Writing to logs before calling selenium"
curl ipinfo.io > "$logs_filename"
echo "" >> "$logs_filename" 

echo "#### START OF SELENIUM STDOUT: ####" >> "$logs_filename"
echo "" >> "$logs_filename"

echo "Selecting selenium script..."
if [ "$script_type" = "kayak_flight" ]; then
    echo "Running kayak_flights.py..."
    python3 kayak_flights.py $arg1 $code >> "$logs_filename"
else
    echo "Running expedia_flights.py..."
    python3 expedia_flights.py $arg1 $code >> "$logs_filename"
fi 

echo "selenium exitted. Writing to logs..."
echo "" >> "$logs_filename"
echo "#### END OF SELENIUM STDOUT ####" >> "$logs_filename"
echo "" >> "$logs_filename"
curl ipinfo.io >> "$logs_filename"
