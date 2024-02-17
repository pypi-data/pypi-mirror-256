from http import HTTPStatus
from typing import Any, Dict, Optional, Union

import httpx

from ... import errors
from ...client import AuthenticatedClient, Client
from ...types import Response


def _get_kwargs(
    app_user_id: str,
) -> Dict[str, Any]:
    _kwargs: Dict[str, Any] = {
        "method": "delete",
        "url": f"/subscribers/{app_user_id}/offerings/override",
    }

    return _kwargs


def _parse_response(
    *, client: Union[AuthenticatedClient, Client], response: httpx.Response
) -> Optional[Any]:
    if response.status_code == HTTPStatus.CREATED:
        return None
    if client.raise_on_unexpected_status:
        raise errors.UnexpectedStatus(response.status_code, response.content)
    else:
        return None


def _build_response(
    *, client: Union[AuthenticatedClient, Client], response: httpx.Response
) -> Response[Any]:
    return Response(
        status_code=HTTPStatus(response.status_code),
        content=response.content,
        headers=response.headers,
        parsed=_parse_response(client=client, response=response),
    )


def sync_detailed(
    app_user_id: str,
    *,
    client: Union[AuthenticatedClient, Client],
) -> Response[Any]:
    """Remove a Customer's Current Offering Override

     Reset the offering overrides back to the current offering for a specific user

    Args:
        app_user_id (str):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[Any]
    """

    kwargs = _get_kwargs(
        app_user_id=app_user_id,
    )

    response = client.get_httpx_client().request(
        **kwargs,
    )

    return _build_response(client=client, response=response)


async def asyncio_detailed(
    app_user_id: str,
    *,
    client: Union[AuthenticatedClient, Client],
) -> Response[Any]:
    """Remove a Customer's Current Offering Override

     Reset the offering overrides back to the current offering for a specific user

    Args:
        app_user_id (str):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[Any]
    """

    kwargs = _get_kwargs(
        app_user_id=app_user_id,
    )

    response = await client.get_async_httpx_client().request(**kwargs)

    return _build_response(client=client, response=response)
