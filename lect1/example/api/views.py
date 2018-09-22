from django.shortcuts import render
from jsonrpc import jsonrpc_method
from jsonrpc.exceptions import Error

from django.core.serializers import serialize

from cats.models import Cat, CatForm

import json

@jsonrpc_method( 'api.hello' )
def say_hello( request, name ):
    return "Hello, {}".format( name )


@jsonrpc_method( 'api.cat_list' )
def get_cats( request ):
    return json.loads( serialize( 'json', Cat.objects.all() ) )

@jsonrpc_method( 'api.add_cat' )
def add_cat( request, **kargs ):
    name = kargs.get( 'name', None )
    if name is None:
        raise Error( 'No "name" field' )
    form = CatForm( kargs )
    if not form.is_valid():
        raise Error( 'Not valid form' )
    cat = Cat.objects.filter( name=name).first() 
    if cat is not None:
        raise Error( 'The cat with the same name exists' )
    form.save()
    return "success"
