from rest_framework.serializers import Serializer
from app.utils.exceptions import CustomValidatorException
from .models import Student


STUDENT_FIELDS_PORTUGUESE_MAPPING = {
    "name": "NOME",
    "phone": "TELEFONE",
    "reference": "REFERÊNCIA",
}


def validate_student(student_id, gym_id):
    if Student.objects.filter(id=student_id, gym__id=gym_id).exists():
        student = Student.objects.get(id=student_id, gym__id=gym_id)
        return student
    else:
        raise CustomValidatorException("Aluno não encontrado.")


def validate_student_serializer(serializer_instance: Serializer, gym_id) -> Serializer:
    data = serializer_instance.initial_data
    data["gym"] = gym_id

    ## Verificando se há campos vazios no body
    empty_fields = []
    for i in data:
        if not data[i]:
            empty_fields.append(i)
    if empty_fields:
        raise CustomValidatorException(
            f"O(s) campo(s) {[STUDENT_FIELDS_PORTUGUESE_MAPPING[f] for f in empty_fields]} não pode(m) estar em branco"
        )

    ## Verificando se esse aluno já existe no banco
    if Student.objects.filter(name=data.get("name", ""), gym__id=gym_id).exists():
        raise CustomValidatorException("Aluno com mesmo nome já existe.")

    return serializer_instance
