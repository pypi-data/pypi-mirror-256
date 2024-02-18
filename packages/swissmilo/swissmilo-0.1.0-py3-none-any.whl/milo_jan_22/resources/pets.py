# File generated from our OpenAPI spec by Stainless.

from __future__ import annotations

import httpx

from ..types import Pet, pets, pet_list_params
from .._types import NOT_GIVEN, Body, Query, Headers, NoneType, NotGiven
from .._utils import maybe_transform
from .._compat import cached_property
from .._resource import SyncAPIResource, AsyncAPIResource
from .._response import (
    to_raw_response_wrapper,
    to_streamed_response_wrapper,
    async_to_raw_response_wrapper,
    async_to_streamed_response_wrapper,
)
from .._base_client import (
    make_request_options,
)

__all__ = ["Pets", "AsyncPets"]


class Pets(SyncAPIResource):
    @cached_property
    def with_raw_response(self) -> PetsWithRawResponse:
        return PetsWithRawResponse(self)

    @cached_property
    def with_streaming_response(self) -> PetsWithStreamingResponse:
        return PetsWithStreamingResponse(self)

    def create(
        self,
        *,
        # Use the following arguments if you need to pass additional parameters to the API that aren't available via kwargs.
        # The extra values given here take precedence over values defined on the client or passed to this method.
        extra_headers: Headers | None = None,
        extra_query: Query | None = None,
        extra_body: Body | None = None,
        timeout: float | httpx.Timeout | None | NotGiven = NOT_GIVEN,
    ) -> None:
        """Create a pet"""
        extra_headers = {"Accept": "*/*", **(extra_headers or {})}
        return self._post(
            "/pets",
            options=make_request_options(
                extra_headers=extra_headers, extra_query=extra_query, extra_body=extra_body, timeout=timeout
            ),
            cast_to=NoneType,
        )

    def retrieve(
        self,
        pet_id: str,
        *,
        # Use the following arguments if you need to pass additional parameters to the API that aren't available via kwargs.
        # The extra values given here take precedence over values defined on the client or passed to this method.
        extra_headers: Headers | None = None,
        extra_query: Query | None = None,
        extra_body: Body | None = None,
        timeout: float | httpx.Timeout | None | NotGiven = NOT_GIVEN,
    ) -> Pet:
        """
        Info for a specific pet

        Args:
          extra_headers: Send extra headers

          extra_query: Add additional query parameters to the request

          extra_body: Add additional JSON properties to the request

          timeout: Override the client-level default timeout for this request, in seconds
        """
        if not pet_id:
            raise ValueError(f"Expected a non-empty value for `pet_id` but received {pet_id!r}")
        return self._get(
            f"/pets/{pet_id}",
            options=make_request_options(
                extra_headers=extra_headers, extra_query=extra_query, extra_body=extra_body, timeout=timeout
            ),
            cast_to=Pet,
        )

    def list(
        self,
        *,
        limit: int | NotGiven = NOT_GIVEN,
        # Use the following arguments if you need to pass additional parameters to the API that aren't available via kwargs.
        # The extra values given here take precedence over values defined on the client or passed to this method.
        extra_headers: Headers | None = None,
        extra_query: Query | None = None,
        extra_body: Body | None = None,
        timeout: float | httpx.Timeout | None | NotGiven = NOT_GIVEN,
    ) -> pets.Pets:
        """
        List all pets

        Args:
          limit: How many items to return at one time (max 100)

          extra_headers: Send extra headers

          extra_query: Add additional query parameters to the request

          extra_body: Add additional JSON properties to the request

          timeout: Override the client-level default timeout for this request, in seconds
        """
        return self._get(
            "/pets",
            options=make_request_options(
                extra_headers=extra_headers,
                extra_query=extra_query,
                extra_body=extra_body,
                timeout=timeout,
                query=maybe_transform({"limit": limit}, pet_list_params.PetListParams),
            ),
            cast_to=pets.Pets,
        )


class AsyncPets(AsyncAPIResource):
    @cached_property
    def with_raw_response(self) -> AsyncPetsWithRawResponse:
        return AsyncPetsWithRawResponse(self)

    @cached_property
    def with_streaming_response(self) -> AsyncPetsWithStreamingResponse:
        return AsyncPetsWithStreamingResponse(self)

    async def create(
        self,
        *,
        # Use the following arguments if you need to pass additional parameters to the API that aren't available via kwargs.
        # The extra values given here take precedence over values defined on the client or passed to this method.
        extra_headers: Headers | None = None,
        extra_query: Query | None = None,
        extra_body: Body | None = None,
        timeout: float | httpx.Timeout | None | NotGiven = NOT_GIVEN,
    ) -> None:
        """Create a pet"""
        extra_headers = {"Accept": "*/*", **(extra_headers or {})}
        return await self._post(
            "/pets",
            options=make_request_options(
                extra_headers=extra_headers, extra_query=extra_query, extra_body=extra_body, timeout=timeout
            ),
            cast_to=NoneType,
        )

    async def retrieve(
        self,
        pet_id: str,
        *,
        # Use the following arguments if you need to pass additional parameters to the API that aren't available via kwargs.
        # The extra values given here take precedence over values defined on the client or passed to this method.
        extra_headers: Headers | None = None,
        extra_query: Query | None = None,
        extra_body: Body | None = None,
        timeout: float | httpx.Timeout | None | NotGiven = NOT_GIVEN,
    ) -> Pet:
        """
        Info for a specific pet

        Args:
          extra_headers: Send extra headers

          extra_query: Add additional query parameters to the request

          extra_body: Add additional JSON properties to the request

          timeout: Override the client-level default timeout for this request, in seconds
        """
        if not pet_id:
            raise ValueError(f"Expected a non-empty value for `pet_id` but received {pet_id!r}")
        return await self._get(
            f"/pets/{pet_id}",
            options=make_request_options(
                extra_headers=extra_headers, extra_query=extra_query, extra_body=extra_body, timeout=timeout
            ),
            cast_to=Pet,
        )

    async def list(
        self,
        *,
        limit: int | NotGiven = NOT_GIVEN,
        # Use the following arguments if you need to pass additional parameters to the API that aren't available via kwargs.
        # The extra values given here take precedence over values defined on the client or passed to this method.
        extra_headers: Headers | None = None,
        extra_query: Query | None = None,
        extra_body: Body | None = None,
        timeout: float | httpx.Timeout | None | NotGiven = NOT_GIVEN,
    ) -> pets.Pets:
        """
        List all pets

        Args:
          limit: How many items to return at one time (max 100)

          extra_headers: Send extra headers

          extra_query: Add additional query parameters to the request

          extra_body: Add additional JSON properties to the request

          timeout: Override the client-level default timeout for this request, in seconds
        """
        return await self._get(
            "/pets",
            options=make_request_options(
                extra_headers=extra_headers,
                extra_query=extra_query,
                extra_body=extra_body,
                timeout=timeout,
                query=maybe_transform({"limit": limit}, pet_list_params.PetListParams),
            ),
            cast_to=pets.Pets,
        )


class PetsWithRawResponse:
    def __init__(self, pets: Pets) -> None:
        self._pets = pets

        self.create = to_raw_response_wrapper(
            pets.create,
        )
        self.retrieve = to_raw_response_wrapper(
            pets.retrieve,
        )
        self.list = to_raw_response_wrapper(
            pets.list,
        )


class AsyncPetsWithRawResponse:
    def __init__(self, pets: AsyncPets) -> None:
        self._pets = pets

        self.create = async_to_raw_response_wrapper(
            pets.create,
        )
        self.retrieve = async_to_raw_response_wrapper(
            pets.retrieve,
        )
        self.list = async_to_raw_response_wrapper(
            pets.list,
        )


class PetsWithStreamingResponse:
    def __init__(self, pets: Pets) -> None:
        self._pets = pets

        self.create = to_streamed_response_wrapper(
            pets.create,
        )
        self.retrieve = to_streamed_response_wrapper(
            pets.retrieve,
        )
        self.list = to_streamed_response_wrapper(
            pets.list,
        )


class AsyncPetsWithStreamingResponse:
    def __init__(self, pets: AsyncPets) -> None:
        self._pets = pets

        self.create = async_to_streamed_response_wrapper(
            pets.create,
        )
        self.retrieve = async_to_streamed_response_wrapper(
            pets.retrieve,
        )
        self.list = async_to_streamed_response_wrapper(
            pets.list,
        )
