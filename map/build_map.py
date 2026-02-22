from .map import *

def build_map():
    """ Builds and returns the warehouse map."""
    map = Map()

    map.add(
        StartNode(1, n=2),  # Start Node
        TJunction(2, missing='n', s=1, w=3, e=7),
        TJunction(3, missing='n', s=4, e=2, w=5),
        TJunction(5, missing='w', e=3, s=6, n=11),
        TJunction(7, missing='n', w=2, s=8, e=9),
        TJunction(9, missing='e', w=7, s=10, n=30),

        DeadEnd(6, n=5),  # Loading Bay 1
        DeadEnd(4, n=3),  # Loading Bay 2
        DeadEnd(8, n=7),  # Loading Bay 3
        DeadEnd(10, n=9),  # Loading Bay 4
        Bay(11, missing='w', n=12, s=5, e=17),
        Bay(12, missing='w', s=11, n=13, e=18),
        Bay(13, missing='w', n=14, s=12, e=19),
        Bay(14, missing='w', n=15, s=13, e=20),
        Bay(15, missing='w', n=16, s=14, e=21),
        Bay(16, missing='w', n=49, s=15, e=22),
        DeadEnd(17, w=11),  # Lower Rack A, Bay 6
        DeadEnd(18, w=12),  # Lower Rack A, Bay 5
        DeadEnd(19, w=13),  # Lower Rack A, Bay 4
        DeadEnd(20, w=14),  # Lower Rack A, Bay 3
        DeadEnd(21, w=15),  # Lower Rack A, Bay 2
        DeadEnd(22, w=16),  # Lower Rack A, Bay 1

        Bay(30, missing='e', n=31, s=9, w=36),
        Bay(31, missing='e', n=32, s=30, w=37),
        Bay(32, missing='e', n=33, s=31, w=38),
        Bay(33, missing='e', n=34, s=32, w=39),
        Bay(34, missing='e', n=35, s=33, w=40),
        Bay(35, missing='e', n=50, s=34, w=41),
        DeadEnd(36, e=30),  # Lower Rack B, Bay 6
        DeadEnd(37, e=31),  # Lower Rack B, Bay 5
        DeadEnd(38, e=32),  # Lower Rack B, Bay 4
        DeadEnd(39, e=33),  # Lower Rack B, Bay 3
        DeadEnd(40, e=34),  # Lower Rack B, Bay 2
        DeadEnd(41, e=35),  # Lower Rack B, Bay 1

        Marker(49, {'s': 16, 'n': 51}),
        Marker(50, {'s': 35, 'n': 52}),

        Corner(51, ('s', 'e'), s=49, e=53),
        Corner(52, ('s', 'w'), s=50, w=53),
        TJunction(53, missing='n', s=54, w=51, e=52),  # change s to n

        TJunction(54, missing="s", w=55, e=56, n=53),  # change n tos
        Corner(55, ('n', 'e'), n=63, e=54),
        Corner(56, ('n', 'w'), n=57, w=54),

        Bay(57, missing='w', n=58, s=56, e=42),
        Bay(58, missing='w', n=59, s=57, e=43),
        Bay(59, missing='w', n=60, s=58, e=44),
        Bay(60, missing='w', n=61, s=59, e=45),
        Bay(61, missing='w', n=62, s=60, e=46),
        Bay(62, missing='w', n=48, s=61, e=47),
        DeadEnd(42, w=57),  # Upper Rack A, Bay 1
        DeadEnd(43, w=58),  # Lower Rack A, Bay 2
        DeadEnd(44, w=59),  # Lower Rack A, Bay 3
        DeadEnd(45, w=60),  # Lower Rack A, Bay 4
        DeadEnd(46, w=61),  # Lower Rack A, Bay 5
        DeadEnd(47, w=62),  # Lower Rack A, Bay 6

        Bay(63, missing='e', n=64, s=55, w=23),
        Bay(64, missing='e', n=65, s=63, w=24),
        Bay(65, missing='e', n=66, s=64, w=25),
        Bay(66, missing='e', n=67, s=65, w=26),
        Bay(67, missing='e', n=68, s=66, w=27),
        Bay(68, missing='e', n=29, s=67, w=28),
        DeadEnd(23, e=63),  # Upper Rack B, Bay 1
        DeadEnd(24, e=64),  # Upper Rack B, Bay 2
        DeadEnd(25, e=65),  # Upper Rack B, Bay 3
        DeadEnd(26, e=66),  # Upper Rack B, Bay 4
        DeadEnd(27, e=67),  # Upper Rack B, Bay 5
        DeadEnd(28, e=68),  # Upper Rack B, Bay 6

        DeadEnd(48, s=62),
        DeadEnd(29, s=68)

    )

    return map