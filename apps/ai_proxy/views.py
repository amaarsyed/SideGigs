from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import AllowAny
from rest_framework.response import Response
from .safety import score_employer, questions_for_missing
from .models import EmployerScreen   # add this import

@api_view(["POST"])
@permission_classes([AllowAny])
def safety_questions(request):
    return Response(questions_for_missing(request.data or {}))

@api_view(["POST"])
@permission_classes([AllowAny])
def safety_score(request):
    result = score_employer(request.data or {})
    # save if client asks: /api/ai/safety/score/?save=1
    save_flag = request.query_params.get("save") == "1"
    if save_flag:
        EmployerScreen.objects.create(
            email=(request.data or {}).get("email",""),
            input=request.data or {},
            score=result["score"],
            rating=result["rating"],
            reasons=result.get("reasons", []),
            next_steps=result.get("next_steps", []),
        )
    return Response(result)
