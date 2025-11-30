import math

from railcontrol.application.utils.scale_conversion import travel_time_seconds
from railcontrol.config import dwell_safety_buffer_seconds, block_occupancy_buffer
from railcontrol.domain.timetable.block_occupancy import BlockOccupancy
from railcontrol.domain.timetable.expanded_passenger_route import ExpandedPassengerRoute


class BlockOccupancyGenerator:
    def __init__(self,service_id: str, start_time: int, expanded_route: ExpandedPassengerRoute):
        self.service_id = service_id
        self.start_time = start_time
        self.expanded_route = expanded_route

    def generate(self) -> list[BlockOccupancy]:

        block_occupancies = []
        current_time = self.start_time
        for leg in self.expanded_route.legs:
            # Add on for each section or block in the inbound path
            for edge in leg.inbound_path_edges:

                block_id = edge.track_block_id
                traversal_time = travel_time_seconds(edge.length_mm, edge.max_speed)
                t_entry = current_time
                t_exit = math.ceil(current_time + traversal_time + dwell_safety_buffer_seconds)
                current_time = t_exit + block_occupancy_buffer
                block_occupancies.append(BlockOccupancy(
                    block_id=block_id,
                    t_entry=t_entry,
                    t_exit=t_exit,
                    service_id=self.service_id,
                    direction=self.expanded_route.direction,
                    length_mm=edge.length_mm,
                    max_speed=edge.max_speed,
                    source_start_junction=edge.from_node,
                    source_end_junction=edge.to_node,
                ))


            #Initial block occupancy
            block_id = leg.platform_block_id
            t_entry = current_time
            t_exit = math.ceil(current_time + leg.dwell_time + dwell_safety_buffer_seconds)
            current_time = t_exit + block_occupancy_buffer

            block_occupancies.append(BlockOccupancy(
                block_id=block_id,
                t_entry=t_entry,
                t_exit=t_exit,
                service_id=self.service_id,
                direction=self.expanded_route.direction,
                length_mm=leg.platform_length_mm,
                max_speed=leg.platform_max_speed,
                source_start_junction=leg.arrival_junction_id,
                source_end_junction=leg.departure_junction_id,
            ))

        return block_occupancies

