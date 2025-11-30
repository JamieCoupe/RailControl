class TimetableRow:
    def __init__(self, station_id, arrival_s, departure_s, dwell_s, runtime_s):
        self.station_id = station_id
        self.arrival_s = arrival_s
        self.departure_s = departure_s
        self.dwell_s = dwell_s
        self.runtime_s = runtime_s  # running time from previous station
