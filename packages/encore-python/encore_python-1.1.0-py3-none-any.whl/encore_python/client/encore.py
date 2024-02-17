import logging
import os
import tempfile

from dataclasses import dataclass
from datetime import datetime as dt
from typing import Any, Callable, Optional, Tuple, Mapping, Final, Generator, Iterator


import requests

from sng_parser import decode_sng

from .parsing import _search_filter
from ..types import (
    BasicSearch,
    BasicSearchOpts,
    AdvancedSearch,
    AdvancedSearchOpts,
    SearchResponse,
    ErrorResponse,
    Song,
)

from ..types.request import EncoreRequestHeaders

__all__ = ["EncoreAPI"]
logger = logging.getLogger(__package__)


@dataclass
class EncoreAPI:
    """
    Python interface to interact with the Encore music search and download API.
    """

    _ratelimit_left: int = 0
    _ratelimit_reset: dt = dt.fromtimestamp(0)
    _ratelimit_total: int = 50
    SEARCH_URL: Final = "https://api.enchor.us"
    DOWNLOAD_URL: Final = "https://files.enchor.us"

    create_name_filter: Callable[
        [str, Optional[Tuple[AdvancedSearch]], bool, bool, Optional[Mapping[str, Any]]],
        AdvancedSearch,
    ] = staticmethod(_search_filter("name"))
    create_album_filter: Callable[
        [str, Optional[Tuple[AdvancedSearch]], bool, bool, Optional[Mapping[str, Any]]],
        AdvancedSearch,
    ] = staticmethod(_search_filter("album"))
    create_genre_filter: Callable[
        [str, Optional[Tuple[AdvancedSearch]], bool, bool, Optional[Mapping[str, Any]]],
        AdvancedSearch,
    ] = staticmethod(_search_filter("genre"))
    create_year_filter: Callable[
        [str, Optional[Tuple[AdvancedSearch]], bool, bool, Optional[Mapping[str, Any]]],
        AdvancedSearch,
    ] = staticmethod(_search_filter("year"))
    create_artist_filter: Callable[
        [str, Optional[Tuple[AdvancedSearch]], bool, bool, Optional[Mapping[str, Any]]],
        AdvancedSearch,
    ] = staticmethod(_search_filter("artist"))
    create_charter_filter: Callable[
        [str, Optional[Tuple[AdvancedSearch]], bool, bool, Optional[Mapping[str, Any]]],
        AdvancedSearch,
    ] = staticmethod(_search_filter("charter"))

    def search(
        self,
        query: str | AdvancedSearch | BasicSearch,
        *,
        per_page: int = 20,
        page: int = 1,
        instrument: str = None,
        difficulty: str = None,
        iter_results: bool = False,
    ) -> SearchResponse | ErrorResponse | Generator[Song, None, None]:
        """
        Executes a search query against the Encore API.

        This method can handle simple string queries as well as structured `BasicSearch` and `AdvancedSearch` objects.
        Depending on the query type, it constructs the appropriate request to the API, handling rate limits and
        parsing the response.

        Parameters:
            query (str | AdvancedSearch | BasicSearch): The search query or object.
            per_page (int): The number of results to return per page. Default is 20.
            page (int): The page number of the search results to return. Default is 1.
            instrument (str, optional): Filter results by specified instrument.
            difficulty (str, optional): Filter results by specified difficulty level.
            iter_results (bool, optional): Return a generator containing the `Song` object of all results.
            Defaults to False

        Returns:
            SearchResponse | ErrorResponse: The search results or an error response,
                                            depending on the outcome of the API call.
        """
        if isinstance(query, str):
            query = BasicSearch(
                search=query,
                per_page=per_page,
                page=page,
                instrument=instrument,
                difficulty=difficulty,
            )
        adv_search = isinstance(query, AdvancedSearch)
        # Assuming query is a search object
        query = query.to_json()
        if self.ratelimit_left == 0 and (x := dt.now()) < self.ratelimit_reset:
            print(f"Cannot search, wait until {x.isoformat()}")
            return
        res = self._search(query_json=query, advanced=adv_search)
        logger.debug("Search returned status of %d", res.status_code)
        try:
            res.raise_for_status()
            resp = SearchResponse(res.json())
            if iter_results:
                return self._iter_results(query=query, resp=resp)
        except:
            return ErrorResponse(res.json())

    def _iter_results(
        self, query: AdvancedSearch | BasicSearch, *, resp: SearchResponse
    ) -> Generator[Song, None, None]:
        adv_search = isinstance(query, AdvancedSearch)
        itered = 0
        while itered != resp.found:
            for res in resp.data:
                itered += 1
                yield res
            if itered != resp.found:
                query.page += 1

            resp = self._search(query_json=query, advanced=adv_search)
            try:
                resp.raise_for_status()
                resp = SearchResponse(resp.json())
            except:
                return ErrorResponse(resp.json())

    def _search(
        self, *, query_json: BasicSearchOpts | AdvancedSearchOpts, advanced: bool
    ) -> requests.Response:
        """
        Internal method to perform the actual API request for a search operation.

        Constructs the request based on whether it's a basic or advanced search,
        serializes the query parameters into JSON, and sends the request to the Encore API.

        Parameters:
            query_json (BasicSearchOpts | AdvancedSearchOpts): The search query parameters serialized as JSON.
            advanced (bool): Flag indicating whether the search is an advanced search.

        Returns:
            requests.Response: The raw response from the API.
        """
        endpoint = "/search"
        if advanced:
            endpoint += "/advanced"
        logger.debug("Running search on %s", endpoint)
        res = requests.post(
            self.SEARCH_URL + endpoint, json=query_json, headers=self.headers
        )
        self._set_rate_limit_info(res)
        return res

    def _set_rate_limit_info(self, r: requests.Response):
        self.ratelimit_total = r.headers["X-RateLimit-Limit"]
        self.ratelimit_reset = r.headers["X-RateLimit-Reset"]
        self.ratelimit_left = r.headers["X-RateLimit-Remaining"]
        logger.debug(
            "%d queries done, %d remaining. Ratelimit resets at %s",
            self.ratelimit_total,
            self.ratelimit_left,
            self.ratelimit_reset.isoformat(),
        )

    def search_by_artist(
        self,
        artist: str,
        *adv_filter_objs: Optional[Tuple[AdvancedSearch]],
        exact: bool = True,
        exclude: bool = False,
        iter_results: bool = False,
        **additional_filters: AdvancedSearchOpts,
    ) -> SearchResponse | ErrorResponse:
        """
        Search music tracks by artist name, with optional additional filters.

        Allows for exact or fuzzy matching, inclusion or exclusion of the specified artist,
        and additional filtering using advanced search options.

        Parameters:
            artist (str): The artist name to search for.
            adv_filter_objs (Tuple[AdvancedSearch]): Additional advanced search filter objects to use with the search query.
            exact (bool): Flag for exact matching on the artist name. Default is True.
            exclude (bool): Flag for excluding the specified artist from the results. Default is False.
            additional_filters (AdvancedSearchOpts): Additional filter options as keyword arguments.
            iter_results (bool, optional): Return a generator containing the `Song` object of all results.
            Defaults to False

        Returns:
            SearchResponse | ErrorResponse: The search results or an error response.
        """

        adv_search = self.create_artist_filter(
            artist, *adv_filter_objs, exact=exact, exclude=exclude, **additional_filters
        )

        return self.search(adv_search, iter_results=iter_results)

    def search_by_album(
        self,
        album: str,
        *adv_filter_objs: Optional[Tuple[AdvancedSearch]],
        artist: Optional[str] = None,
        exact: bool = True,
        exclude: bool = False,
        iter_results: bool = False,
        **additional_filters: AdvancedSearchOpts,
    ) -> SearchResponse | ErrorResponse:
        """
        Search music tracks by album name, with optional artist name and additional filters.

        Allows for exact or fuzzy matching, inclusion or exclusion of the specified album,
        and additional filtering using advanced search options.

        Parameters:
            album (str): The album name to search for.
            adv_filter_objs (Tuple[AdvancedSearch]): Additional advanced search filter objects to use with the search query.
            artist (str, optional): An optional artist name to further filter the search.
            exact (bool): Flag for exact matching on the album name. Default is True.
            exclude (bool): Flag for excluding the specified album from the results. Default is False.
            additional_filters (AdvancedSearchOpts): Additional filter options as keyword arguments.
            iter_results (bool, optional): Return a generator containing the `Song` object of all results.
            Defaults to False

        Returns:
            SearchResponse | ErrorResponse: The search results or an error response.
        """
        params = self.create_album_filter(
            album, *adv_filter_objs, exact=exact, exclude=exclude, **additional_filters
        )
        if artist:
            params = self.create_artist_filter(
                artist, params, exact=exact, exclude=exclude
            )

        return self.search(params, iter_results=iter_results)

    def download(
        self,
        song: str | Song,
        *,
        as_sng: bool = True,
        as_buffer: bool = False,
        outdir: Optional[str] = None,
        sng_dir: Optional[str] = None,
        allow_nonsng_files: bool = False,
        overwrite: bool = False,
    ) -> None | Iterator[bytes]:
        """
        Downloads a song from the Encore API.

        Accepts either a song md5 string or a `Song` object, retrieves the specified song md5 from the API,
        and writes the file to disk or is returned as a buffer. The option to decode the file is allowed by setting `as_sng` to False

        See [sng-format-python](https://github.com/joshrmcdaniel/sng-format-python/blob/v1.1.0/README.md#usage) docs for sng conversion args
        Parameters:
            song (str | Song): The song identifier or `Song` object to download.
            as_sng (bool, optional): To store the song as .sng. Defaults to True.
            as_buffer (bool, optional): Return the content buffer. Defaults to False
            outdir: (str, optional): Output dir of the file. Defaults to working directory
            sng_dir (str, optional): Directory name of the converted sng file. Only needed when
            converting from the .sng format. Generated from metadata if not specified.
            allow_nonsng_files (bool, optional): Allow files not specified in the sng format to
            be decoded. Defaults to False.
            overwrite (bool, optional): Overwrite the existing song path if exists. Defaults to False.

        Returns:
            None: The downloaded song file content.
        """
        if isinstance(song, Song):
            song = song.md5
        filename = f'{song}.sng'
        res = requests.get(
            f"{self.DOWNLOAD_URL}/{filename}", headers=self.headers, stream=True
        )
        res.raise_for_status()
        if as_buffer:
            return res.iter_content(1024)

        if as_sng:
            out = open(os.path.join(outdir, filename), 'wb')
        else:
            out = tempfile.TemporaryFile("wb+")

        for chunk in res.iter_content(1024):
            out.write(chunk)

        if as_sng:
            out.close()
            return

        out.seek(0)
        decode_sng(
            out,
            outdir=outdir,
            allow_nonsng_files=allow_nonsng_files,
            sng_dir=sng_dir,
            overwrite=overwrite
        )
        out.close()

    @property
    def ratelimit_reset(self) -> dt:
        return self._ratelimit_reset

    @ratelimit_reset.setter
    def ratelimit_reset(self, value: int | str):
        if isinstance(value, str):
            value = int(value)
        self._ratelimit_reset = dt.fromtimestamp(value)

    @property
    def ratelimit_left(self) -> int:
        return self._ratelimit_left

    @ratelimit_left.setter
    def ratelimit_left(self, value: int | str):
        if isinstance(value, str):
            value = int(value)
        self._ratelimit_left = value

    @property
    def ratelimit_total(self) -> int:
        return self._ratelimit_total

    @ratelimit_total.setter
    def ratelimit_total(self, value: int | str):
        if isinstance(value, str):
            value = int(value)
        self._ratelimit_total = value

    @property
    def headers(self) -> EncoreRequestHeaders:
        return {"Accept": "application/json"}
