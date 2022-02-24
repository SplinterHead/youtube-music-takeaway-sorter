from dataclasses import dataclass

import pytest

from src.csv import CSVTrack
from src.sorter import sort_lists


@dataclass
class SorterTestCase:
    description: str
    csv_list: list[CSVTrack]
    os_list: list[tuple]
    sorted_list: list[CSVTrack]


sorter_test_cases = [
    SorterTestCase(
        description="Single CSV record and matching OS file",
        csv_list=[
            CSVTrack(title="Song 1", album="Album 1", artist="Artist 1", duration=10)
        ],
        os_list=[("Song 1.mp3", 10.0)],
        sorted_list=[
            CSVTrack(
                title="Song 1",
                album="Album 1",
                artist="Artist 1",
                duration=10,
                filename="Song 1.mp3",
            )
        ],
    ),
    SorterTestCase(
        description="Two CSV records and matching OS files",
        csv_list=[
            CSVTrack(title="Song 1", album="Album 1", artist="Artist 1", duration=10),
            CSVTrack(title="Song 1", album="Album 2", artist="Artist 2", duration=10),
        ],
        os_list=[("Song 1.mp3", 10.0), ("Song 1(1).mp3", 10.0)],
        sorted_list=[
            CSVTrack(
                title="Song 1",
                album="Album 1",
                artist="Artist 1",
                duration=10,
                filename="Song 1.mp3",
            ),
            CSVTrack(
                title="Song 1",
                album="Album 2",
                artist="Artist 2",
                duration=10,
                filename="Song 1(1).mp3",
            ),
        ],
    ),
    SorterTestCase(
        description="Two CSV records but single OS file",
        csv_list=[
            CSVTrack(title="Song 1", album="Album 1", artist="Artist 1", duration=10),
            CSVTrack(title="Song 1", album="Album 2", artist="Artist 2", duration=10),
        ],
        os_list=[("Song 1.mp3", 10.0)],
        sorted_list=[
            CSVTrack(
                title="Song 1",
                album="Album 1",
                artist="Artist 1",
                duration=10,
                filename="Song 1.mp3",
            ),
        ],
    ),
    SorterTestCase(
        description="Two CSV records of different durations and matching OS files",
        csv_list=[
            CSVTrack(title="Song 1", album="Album 1", artist="Artist 1", duration=10),
            CSVTrack(title="Song 1", album="Album 2", artist="Artist 2", duration=20),
        ],
        os_list=[("Song 1.mp3", 10.0), ("Song 1(1).mp3", 20.0)],
        sorted_list=[
            CSVTrack(
                title="Song 1",
                album="Album 1",
                artist="Artist 1",
                duration=10,
                filename="Song 1.mp3",
            ),
            CSVTrack(
                title="Song 1",
                album="Album 2",
                artist="Artist 2",
                duration=20,
                filename="Song 1(1).mp3",
            ),
        ],
    ),
    SorterTestCase(
        description="Single CSV record and similar OS file",
        csv_list=[
            CSVTrack(title="Song 1", album="Album 1", artist="Artist 1", duration=10)
        ],
        os_list=[("Song 1.mp3", 12.1)],
        sorted_list=[
            CSVTrack(
                title="Song 1",
                album="Album 1",
                artist="Artist 1",
                duration=10,
                filename="Song 1.mp3",
            )
        ],
    ),
    SorterTestCase(
        description="Two CSV records and similar OS files",
        csv_list=[
            CSVTrack(title="Song 1", album="Album 1", artist="Artist 1", duration=10),
            CSVTrack(title="Song 1", album="Album 2", artist="Artist 2", duration=15),
        ],
        os_list=[("Song 1.mp3", 12.1), ("Song 1(1).mp3", 14.8)],
        sorted_list=[
            CSVTrack(
                title="Song 1",
                album="Album 1",
                artist="Artist 1",
                duration=10,
                filename="Song 1.mp3",
            ),
            CSVTrack(
                title="Song 1",
                album="Album 2",
                artist="Artist 2",
                duration=15,
                filename="Song 1(1).mp3",
            ),
        ],
    ),
    SorterTestCase(
        description="Three CSV records and OS files matching first and last",
        csv_list=[
            CSVTrack(title="Song 1", album="Album 1", artist="Artist 1", duration=10),
            CSVTrack(title="Song 1", album="Album 2", artist="Artist 2", duration=13),
            CSVTrack(title="Song 1", album="Album 3", artist="Artist 3", duration=17),
        ],
        os_list=[("Song 1.mp3", 11.0), ("Song 1(1).mp3", 16.0)],
        sorted_list=[
            CSVTrack(
                title="Song 1",
                album="Album 1",
                artist="Artist 1",
                duration=10,
                filename="Song 1.mp3",
            ),
            CSVTrack(
                title="Song 1",
                album="Album 3",
                artist="Artist 3",
                duration=17,
                filename="Song 1(1).mp3",
            ),
        ],
    ),
    SorterTestCase(
        description="Two CSV records and OS file duration exactly in the middle",
        csv_list=[
            CSVTrack(title="Song 1", album="Album 1", artist="Artist 1", duration=10),
            CSVTrack(title="Song 1", album="Album 2", artist="Artist 2", duration=13),
        ],
        os_list=[("Song 1.mp3", 11.5)],
        sorted_list=[
            CSVTrack(
                title="Song 1",
                album="Album 1",
                artist="Artist 1",
                duration=10,
                filename="Song 1.mp3",
            )
        ],
    ),
    SorterTestCase(
        description="Filenames including special characters",
        csv_list=[
            CSVTrack(title="Song 1", album="Album 1", artist="Artist 1", duration=10),
            CSVTrack(title="Song 1?", album="Album 1", artist="Artist 1", duration=10),
            CSVTrack(title="Song-1", album="Album 1", artist="Artist 1", duration=10),
            CSVTrack(title="Song/1", album="Album 1", artist="Artist 1", duration=10),
        ],
        os_list=[
            ("Song 1.mp3", 10),
            ("Song 1_.mp3", 10),
            ("Song-1.mp3", 10),
            ("Song_1.mp3", 10),
        ],
        sorted_list=[
            CSVTrack(
                title="Song 1",
                album="Album 1",
                artist="Artist 1",
                duration=10,
                filename="Song 1.mp3",
            ),
            CSVTrack(
                title="Song 1?",
                album="Album 1",
                artist="Artist 1",
                duration=10,
                filename="Song 1_.mp3",
            ),
            CSVTrack(
                title="Song-1",
                album="Album 1",
                artist="Artist 1",
                duration=10,
                filename="Song-1.mp3",
            ),
            CSVTrack(
                title="Song/1",
                album="Album 1",
                artist="Artist 1",
                duration=10,
                filename="Song_1.mp3",
            ),
        ],
    ),
]


@pytest.mark.parametrize(
    "testcase", sorter_test_cases, ids=[x.description for x in sorter_test_cases]
)
def test_sorter_combines_lists(testcase):
    actual = sort_lists(testcase.csv_list, testcase.os_list)
    expected = testcase.sorted_list

    assert expected == actual
