module.exports = {
  apps: [{
    name: 'academic-api',
    script: 'venv/bin/python',
    args: 'run.py',
    cwd: '/home/ubuntu/academic-publication-api',
    instances: 1,
    autorestart: true,
    watch: false,
    max_memory_restart: '1G',
    env: {
      NODE_ENV: 'production',
      HOST: '0.0.0.0',
      PORT: 8000
    },
    error_file: 'logs/pm2-error.log',
    out_file: 'logs/pm2-out.log',
    log_file: 'logs/pm2-combined.log',
    time: true
  }]
};