node 'knowledgecommonsdc.local' {
  
  # Module includes
  include nginx

  # Package includes
  package { 
    'emacs':
      ensure => present;
    
    'git':
      ensure => present;
  }

  # User and group setup
  group { 'git':
    ensure => present,
  }

  user { 'git':
    ensure   => present,
    gid      => 'git',
    groups   => ['www-data',],
    home     => '/srv/git',
    shell    => '/usr/bin/git-shell',
  }

  user { 'www-data':
    shell  => '/bin/bash',
    groups => ['git',],
  }

  ssh_authorized_key { 'dev@knowledgecommonsdc.local':
    ensure => present,
    user   => 'git',
    key    => 'AAAAB3NzaC1yc2EAAAADAQABAAABAQCcYZArb+s9mfZd2DVE5K9TfzxBUQt36VpH7tN9ZMjF814H7s8ottQPRRMmtI5j1thEAmNfGMZqzx7EQmCtOCZ07TuAyLDR7ygarPHnLLe21n1ZelSO5wvQN6keCPsRSRzPrwATKBpF2r0zHsvIBBhrIlUoY+jlx9UJPmAL5NJ+rPoGo2mNcOVLXo77fjJhCp4NfxkVniTEhL8NKkX8/eK4pJZ6hk/AfaNM48JJTm0nf1a5w7NWsBq4nMfXpRr8kAnCakuKTRnLiochv2tW5zSn9uEPLOne1nmkqw14WcO1Eq2I42K93uFnFVf1uwfyUda+ooWVphzSKC+HMVGOtPU3',
    type   => 'rsa',
  }

  # Directory and file config
  $git_dirs = [
               '/srv',
               '/srv/git',
               ]

  file { 
    $git_dirs:
      ensure  => 'directory',
      owner   => 'git',
      group   => 'git';

    '/srv/git/.ssh/':
      ensure => 'directory',
      mode   => 700,
      owner  => 'git',
      group  => 'git';

    '/srv/git/.ssh/authorized_keys':
      mode  => 600,
      owner => 'git',
      group => 'git';
  }

  $django_dirs = [
                  '/srv/www/',
                  '/srv/www/knowledgecommonsdc.org',
                  ]

  file { $django_dirs:
    ensure => 'directory',
    owner  => 'www-data',
    group  => 'git',
  }

  # Mysql config
  class { 'mysql::server':
    config_hash => { 
      'root_password' => 'foo',
    },
  }

  # Git config
  vcsrepo { '/srv/git/kcdc3.git':
    ensure   => bare,
    source   => 'git://github.com/knowledgecommonsdc/kcdc3.git',
    provider => git,
  }

  vcsrepo { '/srv/www/knowledgecommonsdc.org/kcdc':
    source   => '/srv/git/kcdc3.git',
    ensure   => present,
    provider => git,
    user     => 'www-data',
    group    => 'git',
    require  => Vcsrepo['/srv/git/kcdc3.git'],
  }
  
  # Python config
  class { 'python':
    version    => '2.7',
    dev        => true,
    virtualenv => true,
    gunicorn   => true,
  }

  python::virtualenv { '/srv/www/knowledgecommonsdc.org':
    requirements => '/srv/www/knowledgecommonsdc.org/kcdc/requirements.txt',
    owner        => 'www-data',
    group        => 'git',
    require      => Vcsrepo['/srv/www/knowledgecommonsdc.org/kcdc'],
  }

  python::gunicorn { 'vhost':
    virtualenv => '/srv/www/knowledgecommonsdc.org/',
    dir        => '/srv/www/knowledgecommonsdc.org/kcdc/kcdc3',
    mode       => 'django',
    bind       => 'localhost:8080',
    require    => Python::Virtualenv['/srv/www/knowledgecommonsdc.org']
  }

  # Nginx config
  nginx::resource::upstream { 'django_app':
    ensure  => present,
    members => [ 'localhost:8080', ],
  }

  nginx::resource::vhost { 'www.knowledgecommonsdc.org':
    ensure   => present,
    proxy    => 'http://django_app'
  }
}
