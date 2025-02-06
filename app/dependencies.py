"""
API Dependencies
"""
from typing import Annotated
from fastapi import Header


async def get_token_header(x_token: Annotated[str, Header()]):
    """Check token header"""
    #implament this when we implement authentication
    print("X_token at get_token_header ", x_token)


async def get_query_token(token: str):
    """Check query token"""
    # implement when we implement authentication
    print("Token get_query_token ", token)
