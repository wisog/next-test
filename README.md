#Requisitos

* asgiref==3.2.10
* Django==3.1.2
* djangorestframework==3.12.1
* pytz==2020.1
* sqlparse==0.4.1

## Usuarios por default:
* admin/admin - superusuario
* cesar/qwerty - usuario

### Ejecución
python manage.py runserver [PORT]

#### Acceso de administrador:
http://127.0.0.1:{PORT}/admin

#### Acceso al api:
http://127.0.0.1:{PORT}/salas/api/v1/

#### Acceso al sistema:
http://127.0.0.1:{PORT}/