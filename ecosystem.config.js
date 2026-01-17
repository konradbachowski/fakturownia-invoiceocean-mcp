module.exports = {
  apps: [
    {
      name: "fakturownia-mcp",
      script: "/Users/mac/kodziki/mcp/fakturownia-mcp/venv/bin/python3",
      args: "/Users/mac/kodziki/mcp/fakturownia-mcp/main.py",
      cwd: "/Users/mac/kodziki/mcp/fakturownia-mcp",
      env: {
        PYTHONPATH: "/Users/mac/kodziki/mcp/fakturownia-mcp"
      },
      watch: true,
      autorestart: true,
      restart_delay: 4000
    }
  ]
};
