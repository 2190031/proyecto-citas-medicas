import pytest
from django.utils import timezone
from medical.models import *

"""# @pytest.mark.django_db
def test_create_insurance(db):
    insurance = Seguro.objects.create(nom_seg="ARS Humano", tarifa_seg="1000")
    
    assert insurance.id_seg == 1 and insurance.nom_seg == "ARS Humano" and insurance.tarifa_seg == "1000"
    
def test_update_insurance(db):
    insurance = Seguro.objects.create(nom_seg="ARS Humano", tarifa_seg="1000")
    insurance.nom_seg = "SeNaSa"
    insurance.save()
    
    # insurance_query = Seguro.objects.get(nom_seg="SeNaSa)
    # assert insurance_query.nom_seg == "SeNaSa"
    
    assert insurance.id_seg == 1 and insurance.nom_seg == "SeNaSa" and insurance.tarifa_seg == "1000"
    

@pytest.fixture
def paciente(db) -> Paciente:
    return Paciente.objects.create(
        nom_pac = "John Doe",
        edad_pac = 25,
        sexo_pac = "M",
        email_pac = "abc@abc.com",
        dni_pac = "012345678900",
        tel_per_pac = "18091234567",
        tel_dom_pac = "",
        id_seg = ""
    )
"""


@pytest.fixture
def seguro():
    return Seguro.objects.create(nom_seg="Seguro de Prueba", tarifa_seg=100.0)

@pytest.fixture
def paciente(seguro):
    return Paciente.objects.create(nom_pac="Paciente de Prueba", edad_pac=30, sexo_pac="M", email_pac="test@example.com", dni_pac="12345678901", tel_per_pac="1234567890", id_seg=seguro)

@pytest.fixture
def secretaria():
    return Secretaria.objects.create(nom_sec="Secretaria de Prueba", email_sec="secretaria@example.com")

@pytest.fixture
def especialidad():
    return Especialidad.objects.create(nom_espec="Especialidad de Prueba")

@pytest.fixture
def doctor(especialidad):
    return Doctor.objects.create(nom_doc="Doctor de Prueba", consult_doc="Consulta de Prueba", tarifa_doc=200.0)

@pytest.fixture
def usuario():
    return Usuario.objects.create(email_usu="usuario@example.com", pass_usu="password")

@pytest.fixture
def usuario_paciente(usuario, paciente):
    return Usuario_Paciente.objects.create(id_usu=usuario, id_pac=paciente)

@pytest.fixture
def usuario_secretaria(usuario, secretaria):
    return Usuario_Secretaria.objects.create(id_usu=usuario, id_sec=secretaria)



# def test_filter_especialidad(especialidad):
#     assert Especialidad.objects.filter(nom_espec="Cardiología").exists()

@pytest.mark.django_db
def test_seguro_model(seguro):
    assert seguro.nom_seg == "Seguro de Prueba"
    assert seguro.tarifa_seg == 100.0
    assert seguro.created is not None
    assert seguro.updated is not None

@pytest.mark.django_db
def test_paciente_model(paciente):
    assert paciente.nom_pac == "Paciente de Prueba"
    assert paciente.edad_pac == 30
    assert paciente.sexo_pac == "M"
    assert paciente.email_pac == "test@example.com"
    assert paciente.dni_pac == "12345678901"
    assert paciente.tel_per_pac == "1234567890"
    assert paciente.tel_dom_pac is None
    assert paciente.created is not None
    assert paciente.updated is not None

@pytest.mark.django_db
def test_secretaria_model(secretaria):
    assert secretaria.nom_sec == "Secretaria de Prueba"
    assert secretaria.email_sec == "secretaria@example.com"
    assert secretaria.created is not None
    assert secretaria.updated is not None

@pytest.mark.django_db
def test_especialidad_model(especialidad):
    assert especialidad.nom_espec == "Especialidad de Prueba"
    assert especialidad.created is not None
    assert especialidad.updated is not None

@pytest.mark.django_db
def test_doctor_model(doctor):
    assert doctor.nom_doc == "Doctor de Prueba"
    assert doctor.consult_doc == "Consulta de Prueba"
    assert doctor.tarifa_doc == 200.0
    assert doctor.created is not None
    assert doctor.updated is not None

@pytest.mark.django_db
def test_doctor_especialidad_model(especialidad, doctor):
    doctor_especialidad = Doctor_Especialidad.objects.create(id_espec=especialidad, id_doc=doctor)
    assert doctor_especialidad.id_espec == especialidad
    assert doctor_especialidad.id_doc == doctor

@pytest.mark.django_db
def test_doctor_secretaria_model(secretaria, doctor):
    doctor_secretaria = Doctor_Secretaria.objects.create(id_doc=doctor, id_sec=secretaria)
    assert doctor_secretaria.id_doc == doctor
    assert doctor_secretaria.id_sec == secretaria

@pytest.mark.django_db
def test_usuario_model(usuario):
    assert usuario.email_usu == "usuario@example.com"
    assert usuario.pass_usu == "password"
    assert usuario.created is not None
    assert usuario.updated is not None

@pytest.mark.django_db
def test_usuario_paciente_model(usuario_paciente):
    assert usuario_paciente.id_usu.email_usu == "usuario@example.com"
    assert usuario_paciente.id_pac.nom_pac == "Paciente de Prueba"

@pytest.mark.django_db
def test_usuario_secretaria_model(usuario_secretaria):
    assert usuario_secretaria.id_usu.email_usu == "usuario@example.com"
    assert usuario_secretaria.id_sec.nom_sec == "Secretaria de Prueba"

@pytest.mark.django_db
def test_cita_model(usuario, secretaria, seguro, paciente, especialidad, doctor, usuario_paciente, usuario_secretaria):
    cita = Cita.objects.create(fecha_sol=timezone.now().date(), motivo_sol="Motivo de Prueba", estado_sol=0, is_doc=doctor, is_usu_pac=usuario_paciente, is_usu_sec=usuario_secretaria)
    assert cita.fecha_sol == timezone.now().date()
    assert cita.motivo_sol == "Motivo de Prueba"