def parse_flight_args(args):
    '''
    Returns a tuple with the following values:

    (return_code, country_code, uniq_id, travel_type, airport_orig, airport_dest, flight_date)
    '''

    print(f"[parse_flight_args]: Received: {len(args)} arguments: {args}")
    if len(args) != 3:
        print(f"[parse_flight_args] There must be two required arguments: (kayak_flights.py || expedia_flights.py) <data_point> <country_code>")
        return (-1, None, None, None, None, None, None)
    try:
        DATA_POINT = args[1]
        COUNTRY_CODE = args[2]
    except Exception as exc:
        print(f" \
        [parse_flight_args]: Could not import arguments: {exc}\n \
        There must be two required arguments: (kayak_flights.py || expedia_flights.py) <data_point> <country_code> \
        ")
        return (-1, None, None, None, None, None, None)

    try:
        DATA_ID, TRAVEL_TYPE, AIRPORT_ORIG, AIRPORT_DEST, FLIGHT_DATE = DATA_POINT.split(',')
        print(f"[parse_flight_args]: The DATA_POINT argument successfully parsed")
    except Exception as exc:
        print(f"[parse_flight_args]: Could not parse the DATA_POINT argument")
        return (-1, None, None, None, None, None, None)
    
    return (0, COUNTRY_CODE, DATA_ID, TRAVEL_TYPE, AIRPORT_ORIG, AIRPORT_DEST, FLIGHT_DATE)


