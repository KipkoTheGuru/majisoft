set :application, "myorder_platform"
set :deploy_to, "~/webapp_releases/myorder_platform"
set :shared_children, %w(config lib upload)

set :repository, "~/hg/repos/myorder_platform"
set :scm, :mercurial

set :user, "wezatele"
set :use_sudo, false
set :python_command, "PYTHONPATH=/home/wezatele/webapps/myorder_platform/lib/python2.7:$PYTHONPATH python2.7"

server "wezatele.webfactional.com", :app, :web, :primary => true

namespace :deploy do

  task :restart do
    run "/home/wezatele/webapps/myorder_platform/apache2/bin/restart"
  end

  task :finalize_update, :except => { :no_release => true } do
    #django.syncdb
  end

end

namespace (:django) do

  desc <<-DESC
    Run the "python manage.py collectstatic" task
  DESC
  
  task :static do
    run "mkdir -p #{latest_release}/static"
    run "cd #{latest_release} && #{python_command} manage.py collectstatic --noinput" 
  end

  desc <<-DESC
    Run the "python manage.py syncdb" task
  DESC
  task :syncdb do
    run "cd #{latest_release} && #{python_command} manage.py syncdb --noinput"
  end

  desc <<-DESC
    Run the "python manage.py migrate" task
  DESC
  task :migrate do
    run "cd #{latest_release} && #{python_command} manage.py migrate --noinput"
  end

end
