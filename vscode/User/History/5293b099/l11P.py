from rest_framework import status
from rest_framework.decorators import api_view
from rest_framework.response import Response

from applications.models import Application


@api_view(["GET"])
def application_status(request, id):
    """
    Given an application id and a logged user,
    Return a list of (not overwriting) available transitions.

    Output:
    {
        id: str,
        status: str,
        available_transitions: [ str ]
    }
    """
    if not request.user.is_authenticated:
        return Response(
            {"error": "Not authenticated"},
            status=status.HTTP_403_FORBIDDEN,
        )

    try:
        application = Application.objects.get(id=id)
    except Application.DoesNotExist:
        return Response(status=status.HTTP_404_NOT_FOUND)

    if (
        not request.user.has_perm("applications.manage_applications")
        and application.profile.user != request.user
    ):
        return Response(
            {"error": "Insufficient permissions"},
            status=status.HTTP_403_FORBIDDEN,
        )

    return Response(
        {
            "id": id,
            "status": application.status,
            "available_transitions": application.get_available_transitions_names(
                user=request.user
            ),
        }
    )


@api_view(["POST"])
def apply_transition(request, id, transition):
    """
    Transition the status of an application.
    """
    if not request.user.is_authenticated:
        return Response(status=status.HTTP_403_FORBIDDEN)

    try:
        application = Application.objects.get(id=id)
    except Application.DoesNotExist:
        return Response(status=status.HTTP_404_NOT_FOUND)

    # User permission checking is performed in the function
    if transition not in application.get_available_transitions_names(
        user=request.user
    ):
        return Response(
            "Unknown or unavailable transition",
            status=status.HTTP_404_NOT_FOUND,
        )

    # transition is a valid and authorized transition.
    getattr(application, transition)()
    application.save()
    return Response()

@api_view(["GET", "POST"])
def application_notes(request, id):
    """
    Endpoint to get/set the notes associated to an application.

    GET/POST response body:
    {
        "notes": str
    }

    POST request body:
    {
        "notes": str
    }
    """
    if  request.method == 'GET':
        # TODO: Use proper permission
        if not request.user.is_staff:
            return Response(status=status.HTTP_403_FORBIDDEN)
        
    elif  request.method == 'POST':
        # TODO: Use proper permission
        if not request.user.is_staff:
            return Response(status=status.HTTP_403_FORBIDDEN)