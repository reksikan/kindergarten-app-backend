from enum import Enum
from typing import Dict, Callable, Any, Optional, List, Union, Sequence, Set, Type

from fastapi import params, Depends
from fastapi.datastructures import Default, DefaultPlaceholder
from fastapi.routing import APIRouter, APIRoute
from fastapi.types import IncEx
from fastapi.utils import generate_unique_id
from starlette.responses import JSONResponse, Response
from starlette.routing import BaseRoute

from src.db.manager import DBManager
from src.services.manager import ServiceManager


class BaseRouter:
    _router: APIRouter
    _db_manager: DBManager
    _service_manager: ServiceManager
    endpoints: List[Dict[str, Any]]

    def __init__(self, db_manager: DBManager, service_manager: ServiceManager):
        self._db_manager = db_manager
        self._service_manager = service_manager

        for endpoint in self.endpoints:
            dependencies = endpoint.pop('dependencies') or []
            endpoint['dependencies'] = []
            for dependence in dependencies:
                if hasattr(dependence, 'setup'):
                    dependence.setup(db_manager)
                endpoint['dependencies'].append(Depends(dependence))

            endpoint['endpoint'] = getattr(self, endpoint['endpoint'])
            self._router.add_api_route(**endpoint)

    @property
    def router(self) -> APIRouter:
        return self._router


def add_route(
    endpoints: List[Dict[str, Any]],
    path: str,
    *,
    response_model: Any = Default(None),
    status_code: Optional[int] = None,
    tags: Optional[List[Union[str, Enum]]] = None,
    dependencies: Optional[Sequence[Callable]] = None,
    summary: Optional[str] = None,
    description: Optional[str] = None,
    response_description: str = "Successful Response",
    responses: Optional[Dict[Union[int, str], Dict[str, Any]]] = None,
    deprecated: Optional[bool] = None,
    methods: Optional[Union[Set[str], List[str]]] = None,
    operation_id: Optional[str] = None,
    response_model_include: Optional[IncEx] = None,
    response_model_exclude: Optional[IncEx] = None,
    response_model_by_alias: bool = True,
    response_model_exclude_unset: bool = False,
    response_model_exclude_defaults: bool = False,
    response_model_exclude_none: bool = False,
    include_in_schema: bool = True,
    response_class: Union[Type[Response], DefaultPlaceholder] = Default(
        JSONResponse
    ),
    name: Optional[str] = None,
    route_class_override: Optional[Type[APIRoute]] = None,
    callbacks: Optional[List[BaseRoute]] = None,
    openapi_extra: Optional[Dict[str, Any]] = None,
    generate_unique_id_function: Union[
        Callable[[APIRoute], str], DefaultPlaceholder
    ] = Default(generate_unique_id),
) -> Callable[[Callable], Callable]:

    def register_method(func: Callable[[Any], Any]) -> Callable[[Any], Any]:
        endpoints.append({
            'path': path,
            'endpoint': func.__name__,
            'response_model': response_model,
            'status_code': status_code,
            'tags': tags,
            'dependencies': dependencies,
            'summary': summary,
            'description': description,
            'response_description': response_description,
            'responses': responses,
            'deprecated': deprecated,
            'methods': methods,
            'operation_id': operation_id,
            'response_model_include': response_model_include,
            'response_model_exclude': response_model_exclude,
            'response_model_by_alias': response_model_by_alias,
            'response_model_exclude_unset': response_model_exclude_unset,
            'response_model_exclude_defaults': response_model_exclude_defaults,
            'response_model_exclude_none': response_model_exclude_none,
            'include_in_schema': include_in_schema,
            'response_class': response_class,
            'name': name,
            'route_class_override': route_class_override,
            'callbacks': callbacks,
            'openapi_extra': openapi_extra,
            'generate_unique_id_function': generate_unique_id_function
        })
        return func

    return register_method