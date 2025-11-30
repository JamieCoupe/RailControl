from railcontrol.domain.timetable.expanded_passenger_leg import ExpandedPassengerLeg
from railcontrol.domain.timetable.expanded_passenger_route import ExpandedPassengerRoute
from railcontrol.domain.timetable.passenger_route import PassengerRoute
from railcontrol.domain.track.track_block import PlatformTrackBlock


class PassengerRouteExpander:
    def __init__(
        self,
        station_repo,
        track_block_repo,
        track_section_repo,
        routing_service
    ):
        self.station_repo = station_repo
        self.track_block_repo = track_block_repo
        self.track_section_repo = track_section_repo
        self.routing_service = routing_service

    def _resolve_platform_block_for_stop(self, passenger_stop):
        """
            Select the correct PlatformTrackBlock for a stop.

            Rules:
            1. If passenger_stop.platform_preference is given:
                  return the matching platform, or raise error.
            2. If only one platform exists:
                  return it.
            3. If multiple platforms exist and no preference:
                  choose simple default (first).
            4. If no platforms exist:
                  raise ValueError.

            Returns: PlatformTrackBlock
            """

        # Get all platform blocks for this station
        station = self.station_repo.get(passenger_stop.station_id)
        platform_blocks = self.track_block_repo.get_by_station(station.id)

        if not platform_blocks:
            raise ValueError(f"No platform blocks found for station '{station.id}'.")

        # If a platform is specified in the PassengerStop
        pref = passenger_stop.platform_preference
        if pref is not None:
            for block in platform_blocks:
                if block.platform_number == pref:
                    return block

            # Not found → error
            raise ValueError(
                f"Station '{station.id}' has no platform {pref}. "
                f"Available: {[b.platform_number for b in platform_blocks]}"
            )

        # Otherwise:
        # If only one platform → return it
        if len(platform_blocks) == 1:
            return platform_blocks[0]

        # If multiple platforms and no preference → simple default
        return platform_blocks[0]

    def _resolve_platform_junctions(self, platform_block: PlatformTrackBlock):
        """
        Given a platform block, determine which junctions it connects to.

        Steps:
            - Look up track sections for this block ID.
            - If none exist: raise an error.
            - If more than one exist: for now return the first.
            - Return (start_junction_id, end_junction_id)
        """
        platform_track_sections = self.track_section_repo.get_by_block_id(platform_block.id)
        if not platform_track_sections:
            raise ValueError(f"No track sections found for platform block {platform_block.id}")

        # Always use the first section for now
        first_section = platform_track_sections[0]
        return first_section.start_junction_id, first_section.end_junction_id


    def _build_route_leg(self, stop_a, stop_b):
        """
        Computes a single leg of the passenger journey using the routing service.

        Steps:
            - Resolve platform of stop A, resolve (jA_start, jA_end)
            - Resolve platform of stop B, resolve (jB_start, jB_end)
            - For now: route from jA_end → jB_start
            - Validate route success
            - Return ExpandedStopLeg

        Later improvements:
            - direction-aware choice of entry/exit
            - conflict detection
            - request-stop logic
        """
        platform_a = self._resolve_platform_block_for_stop(stop_a)
        jA_entry, jA_exit = self._resolve_platform_junctions(platform_a)

        platform_b = self._resolve_platform_block_for_stop(stop_b)
        jB_entry, jB_exit = self._resolve_platform_junctions(platform_b)

        route = self.routing_service.find_route(jA_exit, jB_entry)
        if not route.success:
            raise ValueError(
                f"Could not route from {stop_a.station_id} to {stop_b.station_id}: "
                f"{route.message}"
            )


        inbound_edges = []
        path_nodes = route.node_ids
        edges_by_node = self.routing_service.graph.edges

        for i in range(len(path_nodes) - 1):
            u = path_nodes[i]
            v = path_nodes[i + 1]

            # Find the RoutingEdge with to_node == v
            for edge in edges_by_node[u]:
                if edge.to_node == v:
                    inbound_edges.append(edge)
                    break

        if stop_b.dwell_time is not None and stop_b.dwell_time < 0:
            raise ValueError(f"Dwell time cannot be negative at station {stop_b.station_id}")

        if stop_b.dwell_time is not None:
            dwell_seconds = stop_b.dwell_time
        else:
            dwell_seconds = platform_b.dwell_time_minutes * 60

        platform_section = self.track_section_repo.get_by_block_id(platform_b.id)[0]

        leg = ExpandedPassengerLeg(
            station_id=stop_b.station_id,
            platform_block_id=platform_b.id,
            arrival_junction_id=jB_entry,
            departure_junction_id=jB_exit,
            inbound_path_edges=inbound_edges,
            dwell_time=dwell_seconds,
            is_request_stop=stop_b.is_request_stop,
            platform_length_mm=platform_b.length_mm,
            platform_max_speed=platform_section.max_speed,
        )

        return leg

    def expand_route(self, passenger_route:PassengerRoute) -> ExpandedPassengerRoute:
        """
        Returns an ExpandedPassengerRoute containing:
          - the original stops
          - a list of ExpandedStopLeg objects (one per consecutive stop)
        """

        # 1. Validate inputs (do this later)
        # 2. Prepare empty legs list
        legs = []

        # 3. Iterate across stop pairs
        stops = passenger_route.stops

        first_stop = stops[0]
        first_stop_platform = self._resolve_platform_block_for_stop(stops[0])
        fA_entry, fA_exit = self._resolve_platform_junctions(first_stop_platform)
        first_section = self.track_section_repo.get_by_block_id(first_stop_platform.id)[0]

        if first_stop.dwell_time is not None and first_stop.dwell_time < 0:
            raise ValueError(f"Dwell time cannot be negative at station {first_stop.station_id}")

        if first_stop.dwell_time is not None:
            dwell_seconds = first_stop.dwell_time
        else:
            dwell_seconds = first_stop_platform.dwell_time_minutes * 60

        legs.append(
            ExpandedPassengerLeg(
                station_id=first_stop.station_id,
                platform_block_id=first_stop_platform.id,
                arrival_junction_id=fA_entry,
                departure_junction_id=fA_exit,
                inbound_path_edges=[],
                dwell_time=dwell_seconds,
                is_request_stop=first_stop.is_request_stop,
                platform_length_mm=first_section.length_mm,
                platform_max_speed=first_section.max_speed,
            )
        )
        for i in range(len(stops) - 1):
            # We'll implement this after routing logic is ready
            leg = self._build_route_leg(stops[i], stops[i + 1])
            legs.append(leg)

        # 4. Return a structure (create this next lesson)
        return ExpandedPassengerRoute(legs=legs, direction= passenger_route.direction)

    