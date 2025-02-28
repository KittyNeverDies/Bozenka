import logging

from django.http import HttpRequest
from django.shortcuts import render

from rest_framework import viewsets
from rest_framework.decorators import action
from rest_framework.response import Response


class AuthViews(viewsets.ViewSet):
    """
    ViewsSet for authentication of bozenka platform.
    Gives ability to access to accounts using email and password
    """

    @action(detail=False, methods=['post'])
    def register(self, request) -> Response:
        """
        View for registering a new user
        :param request: Request object
        :return: Response object
        """
        email = request.data.get('email')
        password = request.data.get('password')


        return Response(
            {
                'status': 'success',
                'message': 'Successfully registered.',
            },
        )


    @action(detail=False, methods=['post'])
    def login(self, request) -> Response:
        """
        View for logging in a user
        :param request: Request object
        :return: Response object
        """
        email = request.data.get('email')
        password = request.data.get('password')


        return Response(
            {
                'status': 'success',
                'message': 'Successfully logged in.',
            },
        )
