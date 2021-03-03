
LENGTH=$(ls nordvpn_servers | grep -v servers.txt | wc -l)
echo "Number of countries: $LENGTH"
N=$1
echo "Argument received: $N"

# Check if input is a number. Source: https://stackoverflow.com/questions/806906/how-do-i-test-if-a-variable-is-a-number-in-bash
re='^[0-9]+$'
if ! [[ $1 =~ $re ]]; then
   echo "error: Not a number. N must be between 1 and 5 inclusive." >&2; exit 1
fi

# Check the number range. Must not exceed 5 (to avoid authentication problems; NordVPN supports up to 6 concurrent sessions)
if (($N <= 0 || $N > 5)); then
  echo "error: N must be between 1 and 5 inclusive" >&2; exit 1
fi

chunk=$(expr $LENGTH / $N)
echo "chunk size: $chunk"

if ($(expr $LENGTH % $N > 0)); then
    n_processes=$(expr $N + 1 ) # to account for the last chunk. E.g. if Length=58 and N=4, 4 chunks will have size 14 and the last one will have size 2.
else
    n_processes=$N
fi

echo "Number of processes: $n_processes"

ls nordvpn_servers | grep -v servers.txt | xargs -n $chunk -P $n_processes bash run_helper.sh