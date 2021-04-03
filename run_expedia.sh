### Read data ###
declare -a data_points
for file in $(cat data_expedia.txt);
do
    echo "$file imported"
    data_points=(${data_points[@]} "$file")

done
echo "${#data_points[@]} data_points"

### Read HotspotShield VPN country codes ### 
declare -a countries
for file in $(cat hotspot_shield_codes.txt);
do
    #echo "$file"
    countries=(${countries[@]} "$file")

done
echo "${#countries[@]} countries"

NUM_OF_RETRIES_PER_COUNTRY=3 # if we can't connect to some country in a given number of iterations, skip it
SLEEP_TIME=10

for data_point in "${data_points[@]}"
do
    for country in "${countries[@]}"
    do
        disconnected=1
        ATTEMPT=0
        while (( $disconnected == 1 && $ATTEMPT < $NUM_OF_RETRIES_PER_COUNTRY ))
        do  
            echo "Sleeping for $SLEEP_TIME seconds..."
            sleep $SLEEP_TIME
            echo "Disconnecting..."
            hotspotshield disconnect
            echo "Sleeping for $SLEEP_TIME seconds..."
            sleep $SLEEP_TIME
            echo "Connecting to $country"
            hotspotshield connect $country
            echo "Verifying connection..."
            echo "Sleeping for $SLEEP_TIME seconds..."
            sleep $SLEEP_TIME
            disconnected=$(hotspotshield status | grep disconnected | wc -l)
            echo "disconnected: $disconnected"
            ATTEMPT=$(expr $ATTEMPT + 1 )
            echo "ATTEMPT: $ATTEMPT/$NUM_OF_RETRIES_PER_COUNTRY done"

        done

        code=$(hotspotshield status | grep location | grep -o "[A-Z][A-Z]")
        echo "CONNECTED to $code"

        uniq_id=$(echo "$data_point" | cut -d ',' -f1)
        echo "uniq_id: $uniq_id"
        base_dir="./crawled_data/expedia"
        echo "base_dir: $base_dir"

        logs_filename="$base_dir/$uniq_id"_"$code"_"logs.txt"
        echo "logs_filename: $logs_filename"

        echo "Writing to logs before calling expedia_flights.py"
        hotspotshield status > "$logs_filename"

        echo "" >> "$logs_filename"
        echo "#### START OF SELENIUM STDOUT: ####" >> "$logs_filename"
        echo "" >> "$logs_filename"

        echo "Running expedia_flights.py..."
        python3 expedia_flights.py $data_point $code >> "$logs_filename"
        echo "expedia_flights.py exitted. Writing hotspotshield status to logs..."
        echo "" >> "$logs_filename"
        echo "#### END OF SELENIUM STDOUT ####" >> "$logs_filename"
        echo "" >> "$logs_filename"
        hotspotshield status >> "$logs_filename"

        echo "Trying new country..."

    done

done


