
#comando
#comando python manage.py sync_roles

from rolepermissions.roles import AbstractUserRole

class Administrador(AbstractUserRole):
    available_permission = {}

class Funcionario(AbstractUserRole):
    available_permissions = {}

class Cliente(AbstractUserRole):
    available_permissions = {}