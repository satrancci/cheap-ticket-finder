args="$@"

IFS=' ' read -r -a data_chunk <<< "$args"

echo "${#data_chunk[@]} data_chunk received!"

declare -a countries
for file in $(ls ./nordvpn_servers/ | shuf); # to minimize risk of more than one container connecting to the same NordVPN server at the same time
do
    if [ "$file" != "servers.txt" ]; then
        #echo "$file"
        countries=(${countries[@]} "./nordvpn_servers/$file")
    fi
done
echo "${#countries[@]} countries"

# Pass variables from .env
export $(egrep -v '^#' .env | xargs)

randint=$[RANDOM]
container_name="$randint"

echo "Creating a directory ./crawled_data/$randint..."
mkdir -p ./crawled_data/$randint

docker run --restart unless-stopped -ti --cap-add=NET_ADMIN --cap-add=SYS_MODULE --device /dev/net/tun --name $container_name \
        --sysctl net.ipv4.conf.all.rp_filter=2 \
        -e USER=$NORDVPN_USERNAME -e PASS=$NORDVPN_PASSWORD \
        -e CONNECT="" -e TECHNOLOGY=NordLynx -d bubuntux/nordvpn

SLEEP_TIME=20

for data_point in "${data_chunk[@]}"
do
    for country_file in "${countries[@]}"
    do
        echo "Sleeping for $SLEEP_TIME seconds..."
        sleep $SLEEP_TIME

        code=`sort --random-sort $country_file | head -n 1`
        echo "Random code $code selected from $country_file..."

        echo "Renaming $container_name container..."
        docker rename $container_name "$code"_"$randint"
        container_name="$code"_"$randint"

        echo "Connecting to $code..."
        docker exec $container_name nordvpn c $code

        echo "Sleeping for $SLEEP_TIME seconds..."
        sleep $SLEEP_TIME

        echo "Spinning up a selenium container for location $code..."
        docker run -v "$(pwd)"/crawled_data/$randint:/run_dir/data --net=container:$container_name --rm --name "selenium_$randint" selenium $data_point $code

    done

done


echo "Logging out from the container $container_name..."
docker exec -it $container_name nordvpn logout

sleep 10

echo "Stopping and removing the container $container_name..."
docker stop $container_name && docker rm $container_name

