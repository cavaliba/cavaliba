## (c) CAVALIBA.COM

### This version

    Version: 3.15.0 - 2025/02

### Getting (quick) started

    git clone https://github.com/cavaliba/cavaliba.git
    
    cp docker-compose.yml.template docker-compose.yml
    cp nginx.conf.template nginx.conf
    cp oa2p.cfg.template oa2p.cfg
    cp env.template .env
    => customize .env (passwords, etc.)

    docker compose up 
    => point your browser to http://localhost[:port]
    => login with admin and .env defined password

### Doc

    see www.cavaliba.com

### LICENSE

    BSD-3 CLAUSE
