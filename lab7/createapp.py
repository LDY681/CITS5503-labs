from fabric import Connection

# Constants
EC2_INSTANCE_NAME = '24188516-vm-1'
PROJECT_DIR = '/opt/wwc/mysites/lab'

def install_prerequisites(c):
    # Update and upgrade system packages
    c.sudo('apt-get update -y')
    c.sudo('apt-get upgrade -y')

    # Install Python 3 virtual environment package
    c.sudo('apt-get install python3-venv -y')

    # Install Nginx
    c.sudo('apt install nginx -y')

def set_virtual_env(c):
    # Create project directory and navigate to it
    c.sudo(f'mkdir -p {PROJECT_DIR}')
    # Ensure permissions for accessing project directory
    c.sudo(f'chown -R ubuntu:ubuntu {PROJECT_DIR}')
    c.run(f'cd {PROJECT_DIR} && python3 -m venv myvenv')
    c.run(f'cd {PROJECT_DIR} && source myvenv/bin/activate && pip install django')

def setup_django_app(c):
    # Start a new Django project and app within the virtual environment
    c.run(f'cd {PROJECT_DIR} && source myvenv/bin/activate && django-admin startproject lab .')
    c.run(f'cd {PROJECT_DIR} && source myvenv/bin/activate && python3 manage.py startapp polls')

    # Modify the Django project settings and URLs
    c.run(f'echo "from django.http import HttpResponse" > {PROJECT_DIR}/polls/views.py')
    c.run(f'echo "def index(request): return HttpResponse(\'Hello, world.\')" >> {PROJECT_DIR}/polls/views.py')

    c.run(f'echo "from django.urls import path\nfrom . import views\nurlpatterns = [path(\'\', views.index, name=\'index\')]" > {PROJECT_DIR}/polls/urls.py')
    c.run(f'echo "from django.urls import include, path\nfrom django.contrib import admin\nurlpatterns = [path(\'polls/\', include(\'polls.urls\')), path(\'admin/\', admin.site.urls)]" > {PROJECT_DIR}/lab/urls.py')

def configure_nginx(c):
    # Properly handle the Nginx configuration using a temporary file to avoid echo issues
    nginx_config = '''
    server {
      listen 80 default_server;
      listen [::]:80 default_server;

      location / {
        proxy_set_header X-Forwarded-Host $host;
        proxy_set_header X-Real-IP $remote_addr;

        proxy_pass http://127.0.0.1:8000;
      }
    }
    '''
    
    # Write the configuration to a temp file and move it into place
    with open("nginx_temp.conf", "w") as f:
        f.write(nginx_config)
    
    c.put("nginx_temp.conf", "/tmp/nginx_temp.conf")
    c.sudo('mv /tmp/nginx_temp.conf /etc/nginx/sites-enabled/default')
    
    # Restart Nginx to apply changes
    c.sudo('service nginx restart')

def run_django_server(c):
    # Start Django development server in the background
    c.run(f'cd {PROJECT_DIR} && source myvenv/bin/activate && python3 manage.py runserver 8000', pty=False)

if __name__ == "__main__":
    conn = Connection(EC2_INSTANCE_NAME)

    install_prerequisites(conn)
    set_virtual_env(conn)
    setup_django_app(conn)
    configure_nginx(conn)
    run_django_server(conn)