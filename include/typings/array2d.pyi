from typing import Callable, Literal, overload, Iterator, Self
from vmath import vec2i

Neighborhood = Literal['Moore', 'von Neumann']

class array2d_like[T]:
    @property
    def n_cols(self) -> int: ...
    @property
    def n_rows(self) -> int: ...
    @property
    def width(self) -> int: ...
    @property
    def height(self) -> int: ...
    @property
    def shape(self) -> vec2i: ...
    @property
    def numel(self) -> int: ...

    @overload
    def is_valid(self, col: int, row: int) -> bool: ...
    @overload
    def is_valid(self, pos: vec2i) -> bool: ...

    def get[R](self, col: int, row: int, default: R = None) -> T | R:
        """Get the value at the given position.
        
        If the position is out of bounds, returns the default value.
        """

    def render(self) -> str: ...

    def all(self: array2d_like[bool]) -> bool: ...
    def any(self: array2d_like[bool]) -> bool: ...

    def map[R](self, f: Callable[[T], R]) -> array2d[R]: ...
    def apply(self, f: Callable[[T], T]) -> None: ...
    def zip_with[R, U](self, other: array2d_like[U], f: Callable[[T, U], R]) -> array2d[R]: ...
    def copy(self) -> 'array2d[T]': ...
    def tolist(self) -> list[list[T]]: ...

    def __le__(self, other: T | array2d_like[T]) -> array2d[bool]: ...
    def __lt__(self, other: T | array2d_like[T]) -> array2d[bool]: ...
    def __ge__(self, other: T | array2d_like[T]) -> array2d[bool]: ...
    def __gt__(self, other: T | array2d_like[T]) -> array2d[bool]: ...
    def __eq__(self, other: T | array2d_like[T]) -> array2d[bool]: ...  # type: ignore
    def __ne__(self, other: T | array2d_like[T]) -> array2d[bool]: ...  # type: ignore

    def __add__(self, other: T | array2d_like[T]) -> array2d[T]: ...
    def __sub__(self, other: T | array2d_like[T]) -> array2d[T]: ...
    def __mul__(self, other: T | array2d_like[T]) -> array2d[T]: ...
    def __truediv__(self, other: T | array2d_like[T]) -> array2d[T]: ...
    def __floordiv__(self, other: T | array2d_like[T]) -> array2d[T]: ...
    def __mod__(self, other: T | array2d_like[T]) -> array2d[T]: ...
    def __pow__(self, other: T | array2d_like[T]) -> array2d[T]: ...

    def __and__(self, other: T | array2d_like[T]) -> array2d[T]: ...
    def __or__(self, other: T | array2d_like[T]) -> array2d[T]: ...
    def __xor__(self, other: T | array2d_like[T]) -> array2d[T]: ...
    def __invert__(self) -> array2d[T]: ...

    def __iter__(self) -> Iterator[tuple[vec2i, T]]: ...
    def __repr__(self) -> str: ...

    @overload
    def __getitem__(self, index: vec2i) -> T: ...
    @overload
    def __getitem__(self, index: tuple[int, int]) -> T: ...
    @overload
    def __getitem__(self, index: tuple[slice, slice]) -> array2d_view[T]: ...
    @overload
    def __getitem__(self, index: tuple[slice, int] | tuple[int, slice]) -> array2d_view[T]: ...
    @overload
    def __getitem__(self, mask: array2d_like[bool]) -> list[T]: ...
    @overload
    def __setitem__(self, index: vec2i, value: T): ...
    @overload
    def __setitem__(self, index: tuple[int, int], value: T): ...
    @overload
    def __setitem__(self, index: tuple[slice, slice], value: T | 'array2d_like[T]'): ...
    @overload
    def __setitem__(self, index: tuple[slice, int] | tuple[int, slice], value: T | 'array2d_like[T]'): ...
    @overload
    def __setitem__(self, mask: array2d_like[bool], value: T): ...

    # algorithms
    def count(self, value: T) -> int:
        """Count the number of cells with the given value."""

    def count_neighbors(self, value: T, neighborhood: Neighborhood) -> array2d[int]:
        """Count the number of neighbors with the given value for each cell."""

    def get_bounding_rect(self, value: T) -> tuple[int, int, int, int]:
        """Get the bounding rectangle of the given value.
        
        Returns a tuple `(x, y, width, height)` or raise `ValueError` if the value is not found.
        """

    def convolve(self: array2d_like[int], kernel: array2d_like[int], padding: int) -> array2d[int]:
        """Convolve the array with the given kernel."""

    def get_connected_components(self, value: T, neighborhood: Neighborhood) -> tuple[array2d[int], int]:
        """Get connected components of the grid via BFS algorithm.

        Returns the `visited` array and the number of connected components,
        where `0` means unvisited, and non-zero means the index of the connected component.
        """


class array2d_view[T](array2d_like[T]):
    @property
    def origin(self) -> vec2i: ...


class array2d[T](array2d_like[T]):
    def __new__(
            cls,
            n_cols: int,
            n_rows: int,
            default: T | Callable[[vec2i], T] | None = None
            ): ...

    @staticmethod
    def fromlist(data: list[list[T]]) -> array2d[T]: ...


class chunked_array2d[T, TContext]:
    def __new__(
            cls,
            chunk_size: int,
            default: T = None,
            context_builder: Callable[[vec2i], TContext] | None = None,
            ): ...
    
    @property
    def chunk_size(self) -> int: ...
    @property
    def default(self) -> T: ...
    @property
    def context_builder(self) -> Callable[[vec2i], TContext] | None: ...

    def __getitem__(self, index: vec2i) -> T: ...
    def __setitem__(self, index: vec2i, value: T): ...
    def __delitem__(self, index: vec2i): ...
    def __iter__(self) -> Iterator[tuple[vec2i, TContext]]: ...
    def __len__(self) -> int: ...

    def clear(self) -> None: ...
    def copy(self) -> Self: ...

    def world_to_chunk(self, world_pos: vec2i) -> tuple[vec2i, vec2i]:
        """Converts world position to chunk position and local position."""
        
    def add_chunk(self, chunk_pos: vec2i) -> TContext: ...
    def remove_chunk(self, chunk_pos: vec2i) -> bool: ...
    def move_chunk(self, src_chunk_pos: vec2i, dst_chunk_pos: vec2i) -> bool: ...
    def get_context(self, chunk_pos: vec2i) -> TContext | None: ...

    def view(self) -> array2d_view[T]: ...
    def view_rect(self, pos: vec2i, width: int, height: int) -> array2d_view[T]: ...
    def view_chunk(self, chunk_pos: vec2i) -> array2d_view[T]: ...
    def view_chunks(self, chunk_pos: vec2i, width: int, height: int) -> array2d_view[T]: ...
