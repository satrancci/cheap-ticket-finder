# store a list of txt filenames to a variable
args="$@"

IFS=' ' read -r -a countries <<< "$args"

echo "${#countries[@]} countries received!"

# Pass variables from .env
export $(egrep -v '^#' .env | xargs)

#echo "NORDVPN_USERNAME: $NORDVPN_USERNAME"
#echo "NORDVPN_PASSWORD: $NORDVPN_PASSWORD"

for country_file in "${countries[@]}"
do
    echo "$country_file"
    code=`sort --random-sort ./nordvpn_servers/$country_file | head -n 1`
    echo "Random code $code selected from $country_file..."

    docker run -ti --cap-add=NET_ADMIN --cap-add=SYS_MODULE --device /dev/net/tun --name $code \
            --sysctl net.ipv4.conf.all.rp_filter=2 \
            -e USER=$NORDVPN_USERNAME -e PASS=$NORDVPN_PASSWORD \
            -e CONNECT=$code -e TECHNOLOGY=NordLynx -d bubuntux/nordvpn

    echo "Sleeping for 30 seconds..."
    sleep 30

    echo "Crawling through $code..."
    docker run -v "$(pwd)"/run_dir:/run_dir --net=container:$code --rm selenium $code

    echo "Logging out from $code..."
    docker exec $code nordvpn logout

    echo "Removing $code..."
    docker stop $code && docker rm $code

    echo "Sleeping for 60 seconds..."
    sleep 60
    
done
